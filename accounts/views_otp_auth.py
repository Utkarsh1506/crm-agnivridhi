"""
Client authentication views using OTP via email
"""
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from accounts.clerk_auth import clerk_service
from clients.models import Client
import json


class ClientEmailLoginView(View):
    """
    Step 1: Client enters email address
    """
    template_name = 'accounts/client_email_login.html'
    
    def get(self, request):
        context = {}
        # Check if email was passed from login redirect
        if 'client_login_email' in request.session:
            context['email'] = request.session.pop('client_login_email')
        return render(request, self.template_name, context)
    
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, self.template_name)
        
        # Check if client exists with this email and is approved
        try:
            client = Client.objects.get(contact_email=email)
            
            if not client.is_approved:
                messages.error(request, 'Your account is not yet approved. Please contact support.')
                return render(request, self.template_name)
            
            # Send OTP
            otp_result = clerk_service.send_otp(email)
            
            if not otp_result['success']:
                messages.error(request, 'Failed to send OTP. Please try again.')
                return render(request, self.template_name)
            
            messages.success(request, f'OTP sent to {email}')
            
            # Store email in session temporarily
            request.session['login_email'] = email
            request.session['otp_attempts'] = 0
            
            return redirect('client_verify_otp')
        
        except Client.DoesNotExist:
            messages.error(request, 'No account found with this email. Please contact support.')
            return render(request, self.template_name)


class ClientVerifyOTPView(View):
    """
    Step 2: Client verifies OTP
    """
    template_name = 'accounts/client_verify_otp.html'
    
    def get(self, request):
        email = request.session.get('login_email')
        
        if not email:
            messages.error(request, 'Session expired. Please login again.')
            return redirect('client_email_login')
        
        return render(request, self.template_name, {'email': email})
    
    def post(self, request):
        email = request.session.get('login_email')
        otp = request.POST.get('otp', '').strip()
        
        if not email:
            messages.error(request, 'Session expired. Please login again.')
            return redirect('client_email_login')
        
        if not otp:
            messages.error(request, 'Please enter the OTP.')
            return render(request, self.template_name, {'email': email})
        
        # Check OTP attempts
        attempts = request.session.get('otp_attempts', 0)
        if attempts >= 3:
            messages.error(request, 'Too many failed attempts. Please request a new OTP.')
            del request.session['login_email']
            return redirect('client_email_login')
        
        # Verify OTP
        otp_result = clerk_service.verify_otp(email, otp)
        
        if not otp_result['success']:
            request.session['otp_attempts'] = attempts + 1
            messages.error(request, otp_result['message'])
            return render(request, self.template_name, {'email': email})
        
        if not otp_result['is_valid']:
            request.session['otp_attempts'] = attempts + 1
            messages.error(request, otp_result['message'])
            return render(request, self.template_name, {'email': email})
        
        # OTP verified successfully
        try:
            client = Client.objects.get(contact_email=email)
            user = client.user
            
            # Create session without requiring password
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Clear session data
            del request.session['login_email']
            if 'otp_attempts' in request.session:
                del request.session['otp_attempts']
            
            messages.success(request, f'Welcome back, {client.company_name}!')
            
            # Redirect to client dashboard or referrer
            next_url = request.GET.get('next', 'client_dashboard')
            return redirect(next_url)
        
        except Client.DoesNotExist:
            messages.error(request, 'Client account not found.')
            return redirect('client_email_login')


class ClientLogoutView(View):
    """
    Logout client
    """
    @method_decorator(login_required(login_url='client_email_login'))
    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('client_email_login')


# API endpoints for AJAX requests

@csrf_exempt
def send_otp_api(request):
    """API endpoint to send OTP"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required'})
        
        # Check if client exists and is approved
        try:
            client = Client.objects.get(contact_email=email)
            if not client.is_approved:
                return JsonResponse({
                    'success': False, 
                    'message': 'Your account is not yet approved'
                })
        except Client.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'No account found with this email'
            })
        
        # Send OTP
        result = clerk_service.send_otp(email)
        return JsonResponse(result)
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def verify_otp_api(request):
    """API endpoint to verify OTP"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        otp = data.get('otp', '').strip()
        
        if not email or not otp:
            return JsonResponse({'success': False, 'message': 'Email and OTP are required'})
        
        # Verify OTP
        result = clerk_service.verify_otp(email, otp)
        
        if result['is_valid']:
            # Create session
            try:
                client = Client.objects.get(contact_email=email)
                user = client.user
                
                # Create token for API authentication
                from rest_framework.authtoken.models import Token
                token, created = Token.objects.get_or_create(user=user)
                
                return JsonResponse({
                    'success': True,
                    'message': 'OTP verified',
                    'token': token.key,
                    'user_id': user.id,
                    'client_id': client.id
                })
            except Client.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Client not found'})
        else:
            return JsonResponse({'success': False, 'message': result['message']})
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
