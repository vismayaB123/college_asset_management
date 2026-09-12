from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def is_system_admin(user):
    if not user.is_authenticated:
        return False
    if hasattr(user, 'profile') and user.profile.role == 'SYSTEM_ADMIN':
        return True
    raise PermissionDenied

def is_technician_or_admin(user):
    if not user.is_authenticated:
        return False
    if hasattr(user, 'profile') and user.profile.role in ['SYSTEM_ADMIN', 'TECHNICIAN']:
        return True
    raise PermissionDenied

def is_normal_user_or_above(user):
    if not user.is_authenticated:
        return False
    if hasattr(user, 'profile') and user.profile.role in ['SYSTEM_ADMIN', 'TECHNICIAN', 'NORMAL_USER']:
        return True
    raise PermissionDenied

def system_admin_required(function=None, login_url=None):
    actual_decorator = user_passes_test(
        is_system_admin,
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def technician_required(function=None, login_url=None):
    actual_decorator = user_passes_test(
        is_technician_or_admin,
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def normal_user_required(function=None, login_url=None):
    actual_decorator = user_passes_test(
        is_normal_user_or_above,
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
