from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import ApprovalAuthenticationForm

app_name = "assets"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="assets/login.html", authentication_form=ApprovalAuthenticationForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="assets:home"), name="logout"),
    path("register/", views.register, name="register"),
    path("register/success/", views.register_success, name="register_success"),
    path("admin-management/", views.admin_management, name="admin_management"),
    path("admin-management/<str:action>/<int:user_id>/", views.admin_management_action, name="admin_management_action"),
    path("about/", views.about, name="about"),
    path("help/", views.help_page, name="help"),
    path("reports/", views.reports, name="reports"),
    
    # Exports
    path("reports/assets/export/csv/", views.export_assets_csv, name="export_assets_csv"),
    path("reports/assets/export/excel/", views.export_assets_excel, name="export_assets_excel"),
    path("reports/assets/export/pdf/", views.export_assets_pdf, name="export_assets_pdf"),
    
    path("reports/allocations/export/csv/", views.export_allocations_csv, name="export_allocations_csv"),
    path("reports/allocations/export/excel/", views.export_allocations_excel, name="export_allocations_excel"),
    path("reports/allocations/export/pdf/", views.export_allocations_pdf, name="export_allocations_pdf"),
    
    path("reports/maintenance/export/csv/", views.export_maintenance_csv, name="export_maintenance_csv"),
    path("reports/maintenance/export/excel/", views.export_maintenance_excel, name="export_maintenance_excel"),
    path("reports/maintenance/export/pdf/", views.export_maintenance_pdf, name="export_maintenance_pdf"),
    
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings_view, name="settings"),
    path("profile/change-password/", views.change_password, name="change_password"),
    path("assets/", views.asset_list, name="asset_list"),
    path("assets/add/", views.asset_add, name="asset_add"),
    path("assets/edit/<int:pk>/", views.asset_edit, name="asset_edit"),
    path("assets/delete/<int:pk>/", views.asset_delete, name="asset_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_add, name="category_add"),
    path("categories/edit/<int:pk>/", views.category_edit, name="category_edit"),
    path("categories/delete/<int:pk>/", views.category_delete, name="category_delete"),
    path("departments/", views.department_list, name="department_list"),
    path("departments/add/", views.department_add, name="department_add"),
    path("departments/edit/<int:pk>/", views.department_edit, name="department_edit"),
    path("departments/delete/<int:pk>/", views.department_delete, name="department_delete"),
    path("allocations/", views.allocation_list, name="allocation_list"),
    path("allocations/add/", views.allocation_add, name="allocation_add"),
    path("allocations/edit/<int:pk>/", views.allocation_edit, name="allocation_edit"),
    path("allocations/return/<int:pk>/", views.allocation_return, name="allocation_return"),
    path("allocations/delete/<int:pk>/", views.allocation_delete, name="allocation_delete"),
    path("maintenance/", views.maintenance_list, name="maintenance_list"),
    path("maintenance/add/", views.maintenance_add, name="maintenance_add"),
    path("maintenance/edit/<int:pk>/", views.maintenance_edit, name="maintenance_edit"),
    path("maintenance/delete/<int:pk>/", views.maintenance_delete, name="maintenance_delete"),

    # Phase 3: Damaged Equipment
    path('damaged-equipment/', views.damaged_equipment_list, name='damaged_equipment_list'),
    path('damaged-equipment/<int:pk>/update/', views.damaged_equipment_update, name='damaged_equipment_update'),
    
    # Phase 4: User Requests
    path('requests/', views.user_requests, name='user_requests'),
    path('technician-requests/', views.technician_requests, name='technician_requests'),
    path('requests/<int:pk>/update/', views.request_update, name='request_update'),
    
    # Phase 5: Feedback
    path('requests/<int:pk>/feedback/', views.submit_feedback, name='submit_feedback'),

    # Phase 6: Admin People & Feedback
    path('users/', views.user_list, name='user_list'),
    path('technicians/', views.technician_list, name='technician_list'),
    path('user-action/<str:action>/<int:user_id>/', views.user_action, name='user_action'),
    path('technician-action/<str:action>/<int:user_id>/', views.technician_action, name='technician_action'),
    path('feedback/', views.feedback_list, name='feedback_list'),
]
