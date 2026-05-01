# aleks_advprog_assignment
---
# App Purpose :thinking:
This is a flask application with an SQLite database, that allows users to book desks for their work day.

It uses 3 main tables: 
- Desks
- Users
- Bookings

Users can add and delete from all three tables using the webapp ui.

---

# Technologies Used :computer:

- Python 3
- Flask
- SQLite
- unittest (testing framework)
- coverage (test coverage)
- YAML (initial data seeding)

---

# How It Works :gear:

1. User logs in via the login page
2. User is redirected to the dashboard
3. User selects actions (add desk, make booking, etc.)
4. Input is validated before being stored in the database
5. Data is retrieved and displayed via Flask templates

---

# Features :sparkles:

- User login system using sessions
- Add, view, and delete desks
- Add, view, and delete bookings
- Add and delete users
- Input validation for all forms
- Prevention of double-booking
- SQLite database integration
- Unit testing and coverage reporting

---

# Validation & Error Handling :warning:

The application includes validation for:

- Required fields
- Valid locations
- Valid email format
- Valid date formats
- End date after start date
- Duplicate desks and users
- Booking conflicts (prevents overlapping bookings)

Errors are displayed to the user through the UI.

---

# Project Structure :file_folder:

- src/
  - main.py (Flask routes)
  - libs.py (database logic)
  - validators.py (input validation)
- tests/
  - test_validators.py
  - test_routes.py
- Data/
  - YAML files for initial data
- bookings.db (SQLite database)

---

# Setup Instructions :wrench:

1. Pull the repository to your local machine
2. pip install the requirements.txt file
```bash
pip install -r requirements.txt
```
3. Setup any initial data using the yaml files in the Data directory, this could be user accounts, or desks
4. Run main.py from your terminal and paste the IP address output to your terminal window
5. Log in and enjoy :blush:

---

# Running Tests :test_tube:

## To run the unit tests:

```bash
python -m unittest discover tests
```

## To run tests with coverage:

```bash
python -m coverage run --source=src -m unittest discover tests
python -m coverage report
python -m coverage html
```

---

# Known Limitations :warning:

- Passwords are stored in plain text (no hashing implemented)
- No role-based access control (all users have same permissions)
- SQLite used instead of a scalable database

---

# Future Improvements :rocket:

- Implement password hashing for security
- Add user roles and permissions
- Improve UI/UX design
- Add REST API endpoints
- Implement more comprehensive route testing
- Use a production-ready database (e.g. PostgreSQL)

---


