import unittest
from src.libs import Lib
from src import validators

Lib.init_db()
Lib.init_all_data()

class TestValidators(unittest.TestCase):

    # Desk validation
    def test_valid_desk_input(self):
        errors = validators.validate_desk_data("F1D12", "Manchester", 3)
        self.assertEqual(errors, [])

    # User validation

    # Booking balidation

if __name__ == "__main__":
    unittest.main()