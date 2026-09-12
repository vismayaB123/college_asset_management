from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def active_quantity(self):
        return self.quantity - self.returned_quantity

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def active_quantity(self):
        return self.quantity - self.returned_quantity

    def __str__(self):
        return f"{self.name} ({self.code})"

class Asset(models.Model):
    CONDITION_CHOICES = [
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Damaged', 'Damaged'),
        ('Not Working', 'Not Working'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Partially Allocated', 'Partially Allocated'),
        ('Fully Allocated', 'Fully Allocated'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Retired', 'Retired'),
    ]

    asset_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=150, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='Good')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def active_quantity(self):
        return self.quantity - self.returned_quantity

    def __str__(self):
        return f"{self.name} ({self.asset_code})"

class Allocation(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Partially Returned', 'Partially Returned'),
        ('Returned', 'Returned'),
    ]

    ALLOCATION_TYPE_CHOICES = [
        ('FULL', 'Full Allocation'),
        ('PARTIAL', 'Partial Allocation'),
        ('PERMANENT', 'Permanent Allocation'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    assigned_to = models.CharField(max_length=150, blank=True)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='allocations')
    allocation_type = models.CharField(max_length=20, choices=ALLOCATION_TYPE_CHOICES, default='PERMANENT')
    quantity = models.PositiveIntegerField()
    returned_quantity = models.PositiveIntegerField(default=0)
    allocation_date = models.DateField()
    expected_return_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    purpose = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def active_quantity(self):
        return self.quantity - self.returned_quantity

    def __str__(self):
        active_qty = self.quantity - self.returned_quantity
        return f"{active_qty} x {self.asset.name} allocated to {self.department.name} ({self.get_allocation_type_display()})"

class Maintenance(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    description = models.TextField()
    maintenance_date = models.DateField()
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    technician = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def active_quantity(self):
        return self.quantity - self.returned_quantity

    def __str__(self):
        return f"Maintenance for {self.asset.name} on {self.maintenance_date}"

class Profile(models.Model):
    ROLE_CHOICES = (
        ('SYSTEM_ADMIN', 'System Administrator'),
        ('TECHNICIAN', 'Technician'),
        ('NORMAL_USER', 'Normal User'),
    )
    
    ACCOUNT_STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DISABLED', 'Disabled'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='NORMAL_USER')
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS_CHOICES, default='PENDING')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    low_stock_notifications = models.BooleanField(default=True)
    overdue_allocation_notifications = models.BooleanField(default=True)
    maintenance_notifications = models.BooleanField(default=True)

    @property
    def active_quantity(self):
        return self.quantity - self.returned_quantity

    def __str__(self):
        return f"{self.user.username} Profile ({self.get_role_display()})"

class SystemSettings(models.Model):
    low_stock_threshold = models.PositiveIntegerField(default=2)

    @property
    def active_quantity(self):
        return self.quantity - self.returned_quantity

    def __str__(self):
        return "System Settings"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class DamagedEquipment(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('UNDER_REVIEW', 'Under Review'),
        ('UNDER_REPAIR', 'Under Repair'),
        ('RESOLVED', 'Resolved'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='damage_reports')
    reported_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reported_damage')
    damage_date = models.DateField()
    damage_description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='LOW')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REPORTED')
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_damage_reports')
    resolution = models.TextField(blank=True)
    resolved_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Damage Report for {self.asset.name} ({self.get_status_display()})"

class UserRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('Damage Report', 'Damage Report'),
        ('Repair Request', 'Repair Request'),
        ('Technical Support', 'Technical Support'),
        ('Equipment Problem', 'Equipment Problem'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ASSIGNED', 'Assigned'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='support_requests')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='support_requests')
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_support_requests')
    technician_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request: {self.subject} ({self.get_status_display()})"

class UserFeedback(models.Model):
    request = models.OneToOneField(UserRequest, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.request.subject} ({self.rating}/5)"
