import unittest
import os
from src.main import app
from src.libs import Lib

TEST_DB = "test_booking.db"


class TestRoutes(unittest.TestCase):

    def setUp(self):
        '''
        Sets app to testing mode
        Sets DB_NAME for testing database so main database isnot affectde by tests
        Initialises testing database
        '''
        app.config["TESTING"] = True
        Lib.DB_NAME = TEST_DB

        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        Lib.init_db()
        Lib.init_all_data()

        self.client = app.test_client()

    def login_user(self):
        '''
        Helper function setting user_id for access to pages without having to go through login each time
        '''
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1

    # Testing index route
    def test_index_redirects_to_login(self):
        '''
        Tests that navigating to "/" routes user to login
        '''
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing login route
    def test_login_page_loads(self):
        '''
        tests that the login page successfully loads
        '''
        response = self.client.get("/login")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_invalid_login_shows_error(self):
        '''
        Tests that an incorrect login shows an error, doesnt cause a crash, and doesnt redirect user to the dashboard page
        '''
        response = self.client.post(
            "/login",
            data={
                "username": "wrong",
                "password": "wrong"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username or password", response.data)

    def test_valid_login_redirects_to_dashboard(self):
        '''
        Tests that on a successful login the user is redirected to the dashboard page
        '''
        response = self.client.post(
            "/login",
            data={
                "username": "Admin",
                "password": "AdminPowers12"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.location)

    # Testing dashboard route
    def test_dashboard_logged_in(self):
        '''
        Tests that a logged in user can access the dashboard page
        '''
        self.login_user()

        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

    def test_dashboard_redirects_when_not_logged_in(self):
        '''
        Tests that a non logged in user is redirected to login page if they try to access the dashboard
        '''
        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing show_desks page
    def test_show_desks_logged_in(self):
        '''
        Tests that a logged in user can access the show desks page
        '''
        self.login_user()

        response = self.client.get("/show_desks")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Desks", response.data)

    def test_show_desks_contains_seeded_desk(self):
        '''
        Tests that seed data from yaml files is presented ont he show desks page
        '''
        self.login_user()

        response = self.client.get("/show_desks")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"F1D0", response.data)

    # Testing add_desks page
    def test_add_desks_get_logged_in(self):
        '''
        Tests that a logged in user can access the add desks page
        '''
        self.login_user()

        response = self.client.get("/add_desks")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add", response.data)

    def test_add_desks_post_valid(self):
        '''
        Tests that a valid input redirects user to dashboard
        '''
        self.login_user()

        response = self.client.post(
            "/add_desks",
            data={
                "name": "TEST_DESK_1",
                "location": "Manchester",
                "floor": "3"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.location)

    def test_add_desks_post_invalid_location(self):
        '''
        Tests that the user is given an error message when incorrect input is receieved
        '''
        self.login_user()

        response = self.client.post(
            "/add_desks",
            data={
                "name": "TEST_DESK_2",
                "location": "InvalidLocation",
                "floor": "3"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"InvalidLocation is not a valid location", response.data)

    def test_add_desks_redirects_when_not_logged_in(self):
        '''
        Tests that a non logged in user cannot access the add desks page
        '''
        response = self.client.get("/add_desks")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing del_desks page
    def test_del_desks_get_logged_in(self):
        '''
        Tests that a logged in user cn access the delete desks page
        '''
        self.login_user()

        response = self.client.get("/del_desks")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Delete", response.data)

    def test_del_desks_post_valid(self):
        '''
        Tests that on successful deletion, user is redirected back to the dashboard
        '''
        self.login_user()

        response = self.client.post(
            "/del_desks",
            data={
                "name": "F1D0",
                "location": "Manchester",
                "floor": "3"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.location)

    def test_del_desks_redirects_when_not_logged_in(self):
        '''
        Tests that a non logged in user cannot access delete desks page
        '''
        response = self.client.get("/del_desks")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing show_bookings page
    def test_show_bookings_logged_in(self):
        '''
        Tests that a logged in user can access show bookings page
        '''
        self.login_user()

        response = self.client.get("/show_bookings")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Start Date", response.data)

    def test_show_bookings_redirects_when_not_logged_in(self):
        '''
        Tests that a non logged in user cannot access show bookings screen
        '''
        response = self.client.get("/show_bookings")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing make_booking page
    def test_make_booking_get_logged_in(self):
        '''
        Tests that a logged in user can access the make booking page
        '''
        self.login_user()

        response = self.client.get("/make_booking")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Make a Booking", response.data)

    def test_make_booking_post_valid(self):
        '''
        Tests that a logged in user is redirected to the show bookings page when correct input is given
        This is so that the user can view and confirm the booking they just made
        '''
        self.login_user()

        response = self.client.post(
            "/make_booking",
            data={
                "desk_name": "F1D1",
                "start_date": "2099-01-01",
                "end_date": "2099-01-02"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/show_bookings", response.location)

    def test_make_booking_post_invalid_desk(self):
        '''
        Tests that an error message is shown to the user when giving incorrect input
        and that the user stays on the make booking page incase they want to try again
        '''
        self.login_user()

        response = self.client.post(
            "/make_booking",
            data={
                "desk_name": "NOT_A_REAL_DESK",
                "start_date": "2099-01-01",
                "end_date": "2099-01-02"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Desk NOT_A_REAL_DESK does not exist", response.data)

    def test_make_booking_redirects_when_not_logged_in(self):
        '''
        Tests that a non logged in user cannot access the make booking page
        '''
        response = self.client.get("/make_booking")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing del_booking page
    def test_del_booking_get_logged_in(self):
        '''
        Tests that a loged in user can access the delete bookings page
        '''
        self.login_user()

        response = self.client.get("/del_booking")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Delete", response.data)

    def test_del_booking_post_valid(self):
        '''
        Tests that correct input redirects user to show_bookings
        This is so they can confirm the booking they made has been removed
        '''
        self.login_user()

        response = self.client.post(
            "/del_booking",
            data={
                "desk": "F1D0",
                "start_date": "2099-01-01",
                "end_date": "2099-01-02"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/show_bookings", response.location)

    def test_del_booking_redirects_when_not_logged_in(self):
        '''
        Tests that a non logged in user cannot access the delete bookings page
        '''
        response = self.client.get("/del_booking")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing add_user page
    def test_add_user_get_logged_in(self):
        '''
        Tests that a logged in user can access the add user page
        '''
        self.login_user()

        response = self.client.get("/add_user")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User", response.data)

    def test_add_user_post_valid(self):
        '''
        Tests that on valid input the user is redirected to the dashboard
        '''
        self.login_user()

        response = self.client.post(
            "/add_user",
            data={
                "username": "TestUser123",
                "password": "Password123",
                "f_name": "Test",
                "s_name": "User",
                "email": "test.user@example.com"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.location)

    def test_add_user_post_invalid_email(self):
        '''
        Tests that on incorrect user input an error message is shown and the user is kept on the add user page to try again
        '''
        self.login_user()

        response = self.client.post(
            "/add_user",
            data={
                "username": "TestUser123",
                "password": "Password123",
                "f_name": "Test",
                "s_name": "User",
                "email": "invalid-email"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email must contain @ symbol", response.data)

    def test_add_user_redirects_when_not_logged_in(self):
        '''
        Tests that a non logged in user cannot access the add user route
        '''
        response = self.client.get("/add_user")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing del_user page
    def test_del_user_get_logged_in(self):
        '''
        Tests that a logged in user can access the delete users route
        '''
        self.login_user()

        response = self.client.get("/del_user")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Delete", response.data)

    def test_del_user_post_valid(self):
        '''
        Tests that on valid input user is redirected to dashboard
        '''
        self.login_user()

        response = self.client.post(
            "/del_user",
            data={
                "username": "Admin"
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.location)

    def test_del_user_redirects_when_not_logged_in(self):
        '''
        Tests that non logged in user cannot access delete user page
        '''
        response = self.client.get("/del_user")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing logout route
    def test_logout_redirects_to_login(self):
        '''
        Tests that login function redirects user to login page
        '''
        self.login_user()

        response = self.client.get("/logout", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_logout_clears_session(self):
        '''
        Tests that logout route actually removes session id, and forcefully accessing dashboard redirects to login
        '''
        self.login_user()

        self.client.get("/logout")

        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)


if __name__ == "__main__":
    unittest.main()