Smart POS/
│
├─ main.py                 # Entry point of the application
├─ requirements.txt        # Python dependencies (PyQt5, SQLite3/SQLAlchemy, etc.)
│
├─ database/
│   ├─ __init__.py
│   ├─ db_setup.py         # Database connection and initialization
│   ├─ models.py           # SQLAlchemy or SQLite table models
│   └─ queries.py          # Common DB queries and functions
│
├─ ui/
│   ├─ __init__.py
│   ├─ login_ui.py          # Login page UI
│   ├─ admin_dashboard.py   # Admin dashboard UI
│   ├─ sales_ui.py          # Sales/POS interface UI
│   ├─ stock_ui.py          # Stock management UI
│   ├─ reports_ui.py        # Reports and analytics UI
│   └─ dialogs.py           # Reusable dialogs (alerts, confirmation, first-time setup)
│
├─ controllers/
│   ├─ login_controller.py      # Handles login
│   ├─ admin_controller.py      # Admin logic, manage users, reports
│   ├─ sales_controller.py      # Handle POS transactions and real-time stock update
│   └─ stock_controller.py      # Add/edit/delete stock items
│
├─ assets/
│   ├─ styles/                  # QSS or CSS styles for PyQt widgets
│   ├─ icons/                   # App icons and button icons
│   └─ images/                  # Images used in the UI
│
├─ utils/
│   ├─ __init__.py
│   ├─ animations.py           # Fade-in/out, tab switch animations
│   ├─ helpers.py              # Misc helper functions
│   └─ validators.py           # Input validation functions