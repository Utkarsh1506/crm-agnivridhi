from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Scheme
from clients.models import Client

@login_required
def scheme_list(request):
    """List all available schemes"""
    # Filter by status since Scheme has no is_active field
    schemes = Scheme.objects.filter(status='ACTIVE').order_by('name')
    
    # If client, get eligibility for each scheme
    eligible_schemes = []
    if request.user.is_client:
        client = request.user.client_profile
        for scheme in schemes:
            is_eligible, reasons = scheme.check_client_eligibility(client)
            eligible_schemes.append({
                'scheme': scheme,
                'is_eligible': is_eligible,
                'reasons': reasons
            })
        context = {'eligible_schemes': eligible_schemes}
    else:
        context = {'schemes': schemes}
    
    return render(request, 'schemes/scheme_list.html', context)

@login_required
def scheme_detail(request, pk):
    """View scheme details"""
    scheme = get_object_or_404(Scheme, pk=pk)
    
    # Check eligibility if client
    is_eligible = None
    reasons = []
    if request.user.is_client:
        client = request.user.client_profile
        is_eligible, reasons = scheme.check_client_eligibility(client)
    
    context = {
        'scheme': scheme,
        'is_eligible': is_eligible,
        'reasons': reasons,
    }
    return render(request, 'schemes/scheme_detail.html', context)

@login_required
def check_eligibility(request):
    """AJAX endpoint to check eligibility for a scheme"""
    if not request.user.is_client:
        return JsonResponse({'error': 'Only clients can check eligibility'}, status=403)
    
    scheme_id = request.GET.get('scheme_id')
    if not scheme_id:
        return JsonResponse({'error': 'Scheme ID required'}, status=400)
    
    scheme = get_object_or_404(Scheme, pk=scheme_id)
    client = request.user.client_profile
    
    is_eligible, reasons = scheme.check_client_eligibility(client)
    
    return JsonResponse({
        'is_eligible': is_eligible,
        'reasons': reasons,
        'scheme_name': scheme.name,
    })
