from django.utils import timezone
from .models import Asset, Allocation, Maintenance, Profile, SystemSettings

def notifications(request):
    if not request.user.is_authenticated:
        return {'notifications': [], 'notification_count': 0}
        
    profile, _ = Profile.objects.get_or_create(user=request.user)
    sys_settings, _ = SystemSettings.objects.get_or_create(id=1)
    
    notifications_list = []
    
    # 1. Low Stock Assets (available_quantity > 0 and available_quantity <= threshold)
    if profile.low_stock_notifications:
        low_stock = Asset.objects.filter(available_quantity__gt=0, available_quantity__lte=sys_settings.low_stock_threshold).order_by('name')
        for asset in low_stock:
            notifications_list.append({
                'type': 'low_stock',
                'title': 'Low Stock',
                'message': f"{asset.name} ({asset.asset_code}) has only {asset.available_quantity} units remaining.",
                'icon_class': 'bi-exclamation-triangle',
                'text_class': 'text-warning',
                'url_name': 'assets:asset_list'
            })
        
    # 2. Overdue Allocations (expected_return_date < today and not Returned)
    if profile.overdue_allocation_notifications:
        today = timezone.now().date()
        overdue_allocs = Allocation.objects.select_related('asset').filter(
            expected_return_date__lt=today
        ).exclude(status='Returned').order_by('expected_return_date')
        
        for alloc in overdue_allocs:
            assigned_text = alloc.assigned_to if alloc.assigned_to else "someone"
            notifications_list.append({
                'type': 'overdue',
                'title': 'Overdue Allocation',
                'message': f"{alloc.asset.name} assigned to {assigned_text} is overdue.",
                'icon_class': 'bi-clock-history',
                'text_class': 'text-danger',
                'url_name': 'assets:allocation_list'
            })
        
    # 3. Active Maintenance (Pending or In Progress)
    if profile.maintenance_notifications:
        active_maint = Maintenance.objects.select_related('asset').filter(
            status__in=['Pending', 'In Progress']
        ).order_by('maintenance_date')
        
        for maint in active_maint:
            notifications_list.append({
                'type': 'maintenance',
                'title': 'Maintenance',
                'message': f"{maint.asset.name} is currently under maintenance.",
                'icon_class': 'bi-tools',
                'text_class': 'text-primary',
                'url_name': 'assets:maintenance_list'
            })
        
    if request.user.is_superuser:
        pending_admins = Profile.objects.filter(account_status='PENDING').count()
        if pending_admins > 0:
            notifications_list.append({
                'type': 'admin_approval',
                'title': 'Pending Approval',
                'message': f"{pending_admins} administrator account(s) are awaiting approval.",
                'icon_class': 'bi-person-check',
                'text_class': 'text-warning',
                'url_name': 'assets:admin_management'
            })
            
    return {
        'notifications': notifications_list,
        'notification_count': len(notifications_list)
    }
