Smart POS/
│
├─ main.py                 # Entry point of the application
├─ requirements.txt        # Python dependencies (PyQt5, SQLite3/SQLAlchemy, etc.)
│
├─ database/
│   ├─ db_setup.py         # Database connection and initialization
│   ├─ models.py           # SQLAlchemy or SQLite table models
│   └─ queries.py          # Common DB queries and functions
├─ ui/
│   ├─ login_ui.py          # Login page UI
│   ├─ dashboard.py         # dashboard UI 
├─ controllers/
│   ├─ login_controller.py      # Handles login
│   ├─ admin_controller.py      # Admin logic, manage users, reports
│
├─ assets/
│   ├─ styles/                  # QSS or CSS styles for PyQt widgets
│   ├─ icons/                   # App icons and button icons
│   └─ images/                  # Images used in the UI
│
├─ style/
│   ├─ .qss 
