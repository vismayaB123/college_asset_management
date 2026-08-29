from django.contrib import admin
from .models import Category, Department, Asset, Allocation, Maintenance

admin.site.register(Category)
admin.site.register(Department)
admin.site.register(Asset)
admin.site.register(Allocation)
admin.site.register(Maintenance)
