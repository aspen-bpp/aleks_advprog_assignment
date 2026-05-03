import unittest
import os
from src.main import app
from src.libs import Lib

TEST_DB = "test_booking.db"


class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        Lib.DB_NAME = TEST_DB

        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        Lib.init_db()
        Lib.init_all_data()

        self.client = app.test_client()

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def login_user(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1

    # Testing index route
    def test_index_redirects_to_login(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing login route
    def test_login_page_loads(self):
        response = self.client.get("/login")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_invalid_login_shows_error(self):
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
        self.login_user()

        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

    def test_dashboard_redirects_when_not_logged_in(self):
        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing show_desks page
    def test_show_desks_logged_in(self):
        self.login_user()

        response = self.client.get("/show_desks")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Desks", response.data)

    def test_show_desks_contains_seeded_desk(self):
        self.login_user()

        response = self.client.get("/show_desks")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"F1D0", response.data)

    # Testing add_desks page
    def test_add_desks_get_logged_in(self):
        self.login_user()

        response = self.client.get("/add_desks")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add", response.data)

    def test_add_desks_post_valid(self):
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
        response = self.client.get("/add_desks")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing del_desks page
    def test_del_desks_get_logged_in(self):
        self.login_user()

        response = self.client.get("/del_desks")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Delete", response.data)

    def test_del_desks_post_valid(self):
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
        response = self.client.get("/del_desks")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing show_bookings page
    def test_show_bookings_logged_in(self):
        self.login_user()

        response = self.client.get("/show_bookings")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Start Date", response.data)

    def test_show_bookings_redirects_when_not_logged_in(self):
        response = self.client.get("/show_bookings")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing make_booking page
    def test_make_booking_get_logged_in(self):
        self.login_user()

        response = self.client.get("/make_booking")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Make a Booking", response.data)

    def test_make_booking_post_valid(self):
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
        response = self.client.get("/make_booking")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing del_booking page
    def test_del_booking_get_logged_in(self):
        self.login_user()

        response = self.client.get("/del_booking")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Delete", response.data)

    def test_del_booking_post_valid(self):
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
        response = self.client.get("/del_booking")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing add_user page
    def test_add_user_get_logged_in(self):
        self.login_user()

        response = self.client.get("/add_user")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User", response.data)

    def test_add_user_post_valid(self):
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
        response = self.client.get("/add_user")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing del_user page
    def test_del_user_get_logged_in(self):
        self.login_user()

        response = self.client.get("/del_user")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Delete", response.data)

    def test_del_user_post_valid(self):
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
        response = self.client.get("/del_user")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    # Testing logout route
    def test_logout_redirects_to_login(self):
        self.login_user()

        response = self.client.get("/logout", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_logout_clears_session(self):
        self.login_user()

        self.client.get("/logout")

        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)


if __name__ == "__main__":
    unittest.main()