import unittest
from src.main import app
from src.libs import Lib


class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        Lib.init_db()
        Lib.init_all_data()

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

    def test_dashboard_redirects_when_not_logged_in(self):
        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

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