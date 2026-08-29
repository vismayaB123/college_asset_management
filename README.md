# College Asset Management System

## Project Overview
The College Asset Management System is a robust web-based application designed to digitally track and manage physical assets across a college or university campus. It empowers administrators to maintain an accurate inventory, track department allocations in real-time, log maintenance costs, and generate comprehensive analytics and exportable reports.

## Main Features
- **Dashboard**: Real-time summary metrics, status breakdowns, and recent activity logs.
- **Categories Management**: Group assets by logical categories (e.g., Electronics, Furniture).
- **Departments Management**: Manage campus departments and physical locations.
- **Asset Management**: Full CRUD capabilities for asset inventory, tracking total vs. available quantities, and condition statuses.
- **Asset Allocation**: Assign specific quantities of assets to departments or individuals, ensuring stock boundaries are strictly enforced.
- **Asset Returns**: Log actual return dates and dynamically restore available asset quantities.
- **Maintenance Management**: Track asset repairs, technician assignments, and incurred costs while automatically toggling the asset's availability status.
- **User Profile**: Edit personal details and manage your account.
- **Profile Picture Upload**: Supports localized image uploads for avatars.
- **Change Password**: Secure authentication logic for password resets.
- **Settings**: System and user preference center.
- **Notification Preferences**: Opt-in/out of low stock, overdue allocation, and maintenance alerts.
- **Low Stock Threshold**: Admin-only configurable threshold for triggering low inventory warnings.
- **Light/Dark/System Appearance**: Persistent, responsive theme switching utilizing LocalStorage and dynamic UI matching.
- **Dynamic Notifications**: A custom context processor injecting real-time alerts across all pages based on the user's active preferences.
- **Reports & Analytics**: A dedicated analytics hub featuring dynamic summary metric calculations.
- **Chart.js Visualizations**: 5 distinct, animated charts (Assets by Category, Assets by Status, Condition, Allocations by Department, Maintenance Costs).
- **Detailed Report Filtering**: Granular GET-based table filtering by date range, department, and status.
- **CSV Export**: `utf-8-sig` encoded raw data exports compatible with Microsoft Excel.
- **Excel Export**: Formatted `.xlsx` generation using `openpyxl`, featuring frozen headers and localized Indian Rupee (`[$₹-en-IN]`) formatting.
- **PDF Export**: Print-ready landscape PDF generation using `reportlab`, featuring alternating row colors and repeating table headers.

## Technology Stack
- **Python** (Backend Core)
- **Django** (Web Framework, ORM, Auth)
- **MySQL** (Relational Database)
- **Bootstrap 5** (Responsive CSS Framework)
- **Bootstrap Icons** (Vector Icons)
- **JavaScript** (Vanilla JS for DOM manipulation)
- **Chart.js** (Data Visualization)
- **Pillow** (Image Processing for Profiles)
- **openpyxl** (Excel Generation)
- **reportlab** (PDF Generation)

## Installation Guide

The following commands are optimized for Windows PowerShell.

1. **Clone the repository (or download the project folder):**
   ```powershell
   git clone <repository-url>
   cd college_asset_management
   ```

2. **Create a virtual environment:**
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the development server:**
   ```powershell
   python manage.py runserver
   ```

## Required Dependencies
The project requires the dependencies listed in `requirements.txt`. They include core libraries like Django, Pillow, openpyxl, reportlab, and mysqlclient (if using the MySQL backend).

## Database Setup
Ensure that your database server (e.g. MySQL via XAMPP) is running.
Run the following commands to initialize the database schema:
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Running the Application
To run the application locally, execute:
```powershell
python manage.py runserver
```
The application will be accessible at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Default/Admin Account
To manage global system settings (such as the Low Stock Threshold), you will need an Administrator account. Create one by running:
```powershell
python manage.py createsuperuser
```
Follow the prompts to configure your username, email, and password. Log in through the application to access admin-only UI elements on the Settings page.

## Project Structure
```text
college_asset_management/
│
├── config/                 # Core Django project settings and root URLs
├── assets/                 # Main Django application
│   ├── models.py           # Database schemas
│   ├── views.py            # Business logic and export generators
│   ├── urls.py             # App routing
│   ├── context_processors.py # Global notification injector
│   └── templates/          # HTML templates
├── media/                  # Uploaded profile pictures
├── static/                 # CSS, JavaScript, and static assets
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
└── manage.py               # Django execution script
```

## Reports & Exports
The application provides a powerful analytics suite under the **Reports** tab:
- **Analytics Charts**: Visualizes stock and maintenance trends. Includes custom staggered load animations and dynamically responds to Dark Mode changes.
- **Filtering**: Tabular data can be narrowed down by custom date ranges and statuses.
- **Filter-Preserving Exports**: The CSV, Excel, and PDF buttons automatically inherit your active GET parameters, ensuring the downloaded document exactly matches the on-screen table.

## Settings & Notifications
The **Settings** page is broken down into User and System configurations:
- **Notification Preferences**: Users can individually toggle alerts for Low Stock, Overdue Allocations, and Active Maintenance.
- **Appearance Preferences**: Users can toggle Light, Dark, or System Default themes.
- **Administrator Restrictions**: Only `request.user.is_staff` or `is_superuser` accounts can modify the **Low Stock Threshold**. Standard users will see a read-only display.

## Data Integrity
Strict backend checks ensure mathematical impossibility of corrupt asset states:
- **Asset Quantities**: Available quantity is dynamically calculated from the total quantity minus currently deployed allocations.
- **Allocation Limits**: The system restricts allocation edits (both increases and decreases) from exceeding the total physical stock.
- **Asset Returns**: Returning an asset automatically replenishes the pool up to, but never exceeding, the physical total.
- **Protected Deletion**: Django's `ProtectedError` is caught to prevent the deletion of Categories, Departments, or Assets that have active historical records tied to them.
- **Maintenance Status**: The asset's status dynamically toggles to "Under Maintenance" and back to "Available/Allocated" based on real-time task statuses.

## Production / Deployment Notes
This project is configured for **Development**. Before deploying to a production server, the server administrator must configure `config/settings.py`:
- `DEBUG` must be set to `False`.
- `SECRET_KEY` should be securely loaded via environment variables (`os.environ.get()`).
- `ALLOWED_HOSTS` must contain the production domain/IP.
- `STATIC_ROOT` must be configured and `python manage.py collectstatic` executed.
- A production-ready database (such as PostgreSQL or MySQL) is currently expected.

## Future Improvements
The foundation is built for massive scalability. Future considerations include:
- Pagination on data-heavy lists
- Granular Role-based Permissions (e.g., Department Heads)
- Comprehensive Audit Trail & Activity Logs
- QR / Barcode tag generation and scanning support
- Advanced Search with Elasticsearch
- Email Notifications & Scheduled reminders via Celery
