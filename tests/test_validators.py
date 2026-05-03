import unittest
import os
from src.libs import Lib
from src import validators

TEST_DB = "test_booking.db"

class TestValidators(unittest.TestCase):

    def setUp(self):
        Lib.DB_NAME = TEST_DB

        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        
        Lib.init_db()
        Lib.init_all_data()

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    # Desk validation

    def test_valid_desk_input(self):
        errors = validators.validate_desk_data("F1D999", "Manchester", "3")
        self.assertEqual(errors, [])

    # Empty input tests
    def test_empty_desk_name(self):
        errors = validators.validate_desk_data("", "Manchester", "3")
        self.assertIn("Desk name is required", errors)

    def test_empty_desk_location(self):
        errors = validators.validate_desk_data("F1D999", "", "3")
        self.assertIn("Desk location is required", errors)
    
    def test_empty_desk_floor(self):
        errors = validators.validate_desk_data("F1D999", "Manchester", "")
        self.assertIn("Desk floor is required", errors)

    # Invalid inputs
    def test_invalid_desk_location(self):
        errors = validators.validate_desk_data("F1D999", "TT", "3")
        self.assertIn("TT is not a valid location", errors)

    def test_invalid_desk_floor_text(self):
        errors = validators.validate_desk_data("F1D999", "Manchester", "Three")
        self.assertIn("Floor must be a positive integer", errors)

    def test_invalid_desk_floor_zero(self):
        errors = validators.validate_desk_data("F1D999", "Manchester", "0")
        self.assertIn("Floor must be a positive integer", errors)


    def test_duplicate_desk(self):
        errors = validators.validate_desk_data("F1D0", "Manchester", "3")
        self.assertIn("Desk already logged in the system", errors)

    # User validation

    def test_valid_user_input(self):
        errors = validators.validate_users_data(
            "TonyFelps",
            "Password123",
            "Tony",
            "Felps",
            "Tony.Felps@coolmail.com"
        )
        self.assertEqual(errors, [])
    
    # Empty input tests

    def test_empty_username(self):
        errors = validators.validate_users_data(
            "",
            "Password123",
            "Tony",
            "Felps",
            "Tony.Felps@coolmail.com"
        )
        self.assertIn("Username is required", errors)

    def test_empty_password(self):
        errors = validators.validate_users_data(
            "TonyFelps",
            "",
            "Tony",
            "Felps",
            "Tony.Felps@coolmail.com"
        )
        self.assertIn("Password is required", errors)

    def test_empty_first_name(self):
        errors = validators.validate_users_data(
            "TonyFelps",
            "Password123",
            "",
            "Felps",
            "Tony.Felps@coolmail.com"
        )
        self.assertIn("First name is required", errors)

    def test_empty_last_name(self):
        errors = validators.validate_users_data(
            "TonyFelps",
            "Password123",
            "Tony",
            "",
            "Tony.Felps@coolmail.com"
        )
        self.assertIn("Last name is required", errors)

    def test_empty_email(self):
        errors = validators.validate_users_data(
            "TonyFelps",
            "Password123",
            "Tony",
            "Felps",
            ""
        )
        self.assertIn("Email is required", errors)


    def test_invalid_email(self):
        errors = validators.validate_users_data(
            "TonyFelps",
            "Password123",
            "Tony",
            "Felps",
            "invalid-email"
        )
        self.assertIn("Email must contain @ symbol", errors)

    def test_duplicate_user(self):
        errors = validators.validate_users_data(
            "Admin",
            "AdminPowers12",
            "Admin",
            "Account",
            "Admin.Admin@adminmail.com"
        )
        self.assertIn("User with those credentials already exists", errors)

    # Booking validation

    def test_valid_booking_input(self):
        errors = validators.validate_booking_data(
            "F1D0",
            "2099-01-01",
            "2099-01-02"
        )
        self.assertEqual(errors, [])

    # Empty input tests

    def test_empty_booking_desk(self):
        errors = validators.validate_booking_data(
            "",
            "2099-01-01",
            "2099-01-02"
        )
        self.assertIn("Desk name is required", errors)
    
    def test_empty_start_date(self):
        errors = validators.validate_booking_data(
            "F1D0",
            "",
            "2099-01-02"
        )
        self.assertIn("Booking start date is required", errors)
    
    def test_empty_end_date(self):
        errors = validators.validate_booking_data(
            "F1D0",
            "2099-01-01",
            ""
        )
        self.assertIn("Booking end date is required", errors)


    def test_booking_desk_does_not_exist(self):
        errors = validators.validate_booking_data(
            "NOT_A_REAL_DESK",
            "2099-01-01",
            "2099-01-02"
        )
        self.assertIn("Desk NOT_A_REAL_DESK does not exist", errors)

    def test_invalid_start_date(self):
        errors = validators.validate_booking_data(
            "F1D0",
            "bad-date",
            "2099-01-02"
        )
        self.assertIn("bad-date is not a valid date", errors)

    def test_invalid_end_date(self):
        errors = validators.validate_booking_data(
            "F1D0",
            "2099-01-01",
            "bad-date"
        )
        self.assertIn("bad-date is not a valid date", errors)

    def test_end_date_before_start_date(self):
        errors = validators.validate_booking_data(
            "F1D0",
            "2099-01-10",
            "2099-01-01"
        )
        self.assertIn("End date cannot be before start date", errors)

    def test_desk_already_booked(self):
        db = Lib.get_db_connection()

        desk_id = Lib.get_desk_id("F1D0")

        with db:
            db.execute(
                """
                INSERT INTO Bookings (user_id, desk_id, start_date, end_date, created)
                VALUES (?, ?, ?, ?, ?)
                """,
                (1, desk_id, "2099-02-01", "2099-02-05", "2099-01-01")
            )

        db.close()

        errors = validators.validate_booking_data(
            "F1D0",
            "2099-02-03",
            "2099-02-04"
        )

        self.assertIn("Desk F1D0 is already booked in that period", errors)

    # Validation helper functions testing

    def test_is_required_true(self):
        self.assertTrue(validators.is_required("hello"))

    def test_is_required_false_empty(self):
        self.assertFalse(validators.is_required(""))

    def test_is_required_false_none(self):
        self.assertFalse(validators.is_required(None))

    def test_is_positive_int_true(self):
        self.assertTrue(validators.is_positive_int("5"))

    def test_is_positive_int_false_text(self):
        self.assertFalse(validators.is_positive_int("five"))

    def test_is_valid_email_true(self):
        self.assertTrue(validators.is_valid_email("test@example.com"))

    def test_is_valid_email_false(self):
        self.assertFalse(validators.is_valid_email("testexample.com"))

    def test_is_valid_location_true(self):
        self.assertTrue(validators.is_valid_location("Manchester"))

    def test_is_valid_location_false(self):
        self.assertFalse(validators.is_valid_location("London"))

    def test_is_valid_date_true(self):
        self.assertTrue(validators.is_valid_date("2099-01-01"))

    def test_is_valid_date_false(self):
        self.assertFalse(validators.is_valid_date("01-01-2099"))

    def test_end_date_after_start_date_true(self):
        self.assertTrue(
            validators.end_date_before_start_date("2099-01-02", "2099-01-01")
        )

    def test_end_date_after_start_date_false(self):
        self.assertFalse(
            validators.end_date_before_start_date("2099-01-01", "2099-01-02")
        )


if __name__ == "__main__":
    unittest.main()