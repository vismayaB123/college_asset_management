from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"{self.name} ({self.asset_code})"

class Allocation(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Partially Returned', 'Partially Returned'),
        ('Returned', 'Returned'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    assigned_to = models.CharField(max_length=150, blank=True)
    quantity = models.PositiveIntegerField()
    allocation_date = models.DateField()
    expected_return_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    purpose = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.asset.name} allocated to {self.department.name}"

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

    def __str__(self):
        return f"Maintenance for {self.asset.name} on {self.maintenance_date}"

class Profile(models.Model):
    ROLE_CHOICES = (
        ('SYSTEM_ADMIN', 'System Administrator'),
    )
    
    ACCOUNT_STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DISABLED', 'Disabled'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='SYSTEM_ADMIN')
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS_CHOICES, default='PENDING')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    low_stock_notifications = models.BooleanField(default=True)
    overdue_allocation_notifications = models.BooleanField(default=True)
    maintenance_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} Profile ({self.get_role_display()})"

class SystemSettings(models.Model):
    low_stock_threshold = models.PositiveIntegerField(default=2)

    def __str__(self):
        return "System Settings"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
