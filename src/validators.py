from src.libs import Lib
from datetime import datetime

def validate_desk_data(name, location, floor):
    '''
    Validating user input for adding to the desk table
    '''
    errors = []
    # Name valiation
    # Format + existence checks
    if not is_required(name):
        errors.append("Desk name is required")

    # location validation
    if not is_required(location):
        errors.append("Desk location is required")
    elif not is_valid_location(location):
        errors.append(f"{location} is not a valid location")

    # floor validation
    if not is_required(floor):
        errors.append("Desk floor is required")
    elif not is_positive_int(floor):
        errors.append("Floor must be a positive integer")
    
    if errors:
        return errors
    
    # Logical checks only ran after Format + existence checks
    if not is_new_desk(name, location, floor):
        errors.append("Desk already logged in the system")

    return errors
    

def validate_users_data(username, password, f_name, s_name, email):
    '''
    Validating user input for adding to the user table
    '''
    errors = []
    # Format + existence checks
    # Username validation
    if not is_required(username):
        errors.append("Username is required")

    # Password validation
    if not is_required(password):
        errors.append("Password is required")

    # first name validation
    if not is_required(f_name):
        errors.append("First name is required")

    # surname validation
    if not is_required(s_name):
        errors.append("Last name is required")

    # email validation
    if not is_required(email):
        errors.append("Email is required")
    elif not is_valid_email(email):
        errors.append("Email must contain @ symbol")
    
    if errors:
        return errors
    # Logical checks ran after Format + existence checks
    if not is_new_user(username, f_name, s_name, email):
        errors.append("User with those credentials already exists")

    return errors

def validate_booking_data(desk, start_date, end_date):
    '''
    Validating user input for adding a booking 
    '''
    errors = []
    # Format and existence checks 
    # Desk validation
    if not is_required(desk):
        errors.append("Desk name is required")
    elif not desk_exists(desk):
        errors.append(f"Desk {desk} does not exist")

    # start_date validation
    if not is_required(start_date):
        errors.append("Booking start date is required")
    elif not is_valid_date(start_date):
        errors.append(f"{start_date} is not a valid date")

    # end_date validation
    if not is_required(end_date):
        errors.append("Booking end date is required")
    elif not is_valid_date(end_date):
        errors.append(f"{end_date} is not a valid date")
    
    if errors:
        return errors

    # Logical checks only ran after format and existence checks
    if not end_date_before_start_date(end_date, start_date):
        errors.append("End date cannot be before start date")

    if not is_desk_available(desk, start_date, end_date):
        errors.append(f"Desk {desk} is already booked in that period")

    return errors

def is_desk_available(desk, start_date, end_date):
    '''
    Validating if a desk has already been booked
    '''

    desk_id = Lib.get_desk_id(desk)

    db = Lib.get_db_connection()

    desk = db.execute(
        """
        SELECT * FROM Bookings WHERE desk_id = ? 
        AND start_date <= ?
        AND end_date >= ?

        """,
        (desk_id, end_date, start_date,)
    ).fetchone()
    db.close()

    if desk is not None:
        return False
    else:
        return True

def desk_exists(desk):
    desk_id = Lib.get_desk_id(desk)

    if desk_id is None:
        return False
    else:
        return True

def is_required(value):
    return value is not None and str(value).strip() != ""

def is_positive_int(value):
    return str(value).isdigit() and int(value) > 0

def is_valid_email(value):
    return isinstance(value, str) and '@' in value

def is_valid_location(value):
    locations = ['Manchester', 'Cambridge', 'Sheffield', 'Bristol']

    if value in locations:
        return True
    else:
        return False
    
def is_valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def end_date_before_start_date(end_date, start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return end >= start

def is_new_desk(name, location, floor):
    db = Lib.get_db_connection()

    desk = db.execute(
        """
        SELECT * FROM Desks WHERE name = ? 
        AND location = ?
        AND floor = ?
        """,
        (name, location, floor,)
    ).fetchone()
    db.close()

    if desk is not None:
        return False
    else:
        return True

def is_new_user(username, f_name, s_name, email):
    db = Lib.get_db_connection()

    user = db.execute(
        """
        SELECT * FROM Users WHERE username = ? 
        AND f_name = ?
        AND s_name = ?
        AND email = ?
        """,
        (username, f_name, s_name, email)
    ).fetchone()
    db.close()

    if user is not None:
        return False
    else:
        return True