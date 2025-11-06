# Add pending_applications view to applications/views.py
view_code = '''

@login_required
def pending_applications(request):
    """Manager-only view for applications awaiting approval"""
    user = request.user
    
    if not (user.is_admin or user.is_manager):
        messages.error(request, "You don't have permission to view this page.")
        return redirect('dashboard')
    
    # Get applications requiring approval
    pending_apps = Application.objects.filter(
        status__in=['SUBMITTED', 'UNDER_REVIEW']
    ).select_related('client', 'scheme', 'assigned_to').order_by('-created_at')
    
    context = {
        'applications': pending_apps,
        'title': 'Applications Awaiting Approval',
    }
    return render(request, 'applications/pending_applications.html', context)
'''

with open(r'c:\Users\Admin\Desktop\agni\CRM\applications\views.py', 'a', encoding='utf-8') as f:
    f.write(view_code)

print("✅ Added pending_applications view")
