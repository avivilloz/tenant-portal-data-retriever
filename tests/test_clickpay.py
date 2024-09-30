import unittest
from unittest.mock import patch, Mock, call
from src.portals.clickpay import ClickPayPortal
from src.config import CLICKPAY_BASE_URL


class TestClickPayPortal(unittest.TestCase):
    @patch("src.portals.clickpay.requests.Session")
    def test_clickpay_retrieve_data_success(self, mock_session):
        # Mock login response
        mock_session().post.return_value.status_code = 200
        mock_session().post.return_value.text = '{"Result": {"Result": "Success"}}'

        # Mock user profile response
        mock_profile_response = Mock()
        mock_profile_response.status_code = 200
        mock_profile_response.text = '{"Result": {"user": {"Email": "test@example.com", "Cellphone": "123-456-7890"}}}}'
        mock_session().post.side_effect = [
            mock_session().post.return_value,
            mock_profile_response,
        ]

        # Mock login status check
        mock_session().get.return_value.text = "Logout"

        portal = ClickPayPortal()
        data = portal.retrieve_data("testuser", "testpass")

        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["phone"], "123-456-7890")

        # Check if correct URLs were called
        mock_session().post.assert_has_calls(
            [
                call(
                    f"{CLICKPAY_BASE_URL}/MobileService/Service.asmx/login",
                    json=unittest.mock.ANY,
                    headers=unittest.mock.ANY,
                ),
                call(
                    f"{CLICKPAY_BASE_URL}/MobileService/Service.asmx/getUserContextJSON",
                    data="NovelPayApp",
                    headers=unittest.mock.ANY,
                ),
            ]
        )
        mock_session().get.assert_called_with(f"{CLICKPAY_BASE_URL}/app#PayNow")

    @patch("src.portals.clickpay.requests.Session")
    def test_clickpay_login_failure(self, mock_session):
        # Mock failed login response
        mock_session().post.return_value.status_code = 401

        portal = ClickPayPortal()
        with self.assertRaises(Exception) as context:
            portal.retrieve_data("testuser", "wrongpassword")

        self.assertTrue("Login failed" in str(context.exception))

    @patch("src.portals.clickpay.requests.Session")
    def test_clickpay_profile_retrieval_failure(self, mock_session):
        # Mock successful login response
        mock_session().post.return_value.status_code = 200
        mock_session().post.return_value.text = '{"Result": {"Result": "Success"}}'

        # Mock failed profile retrieval
        mock_profile_response = Mock()
        mock_profile_response.status_code = 500
        mock_session().post.side_effect = [
            mock_session().post.return_value,
            mock_profile_response,
        ]

        portal = ClickPayPortal()
        with self.assertRaises(Exception) as context:
            portal.retrieve_data("testuser", "testpass")

        self.assertTrue(
            "Failed to retrieve user profile data" in str(context.exception)
        )

    @patch("src.portals.clickpay.requests.Session")
    def test_clickpay_incomplete_profile_data(self, mock_session):
        # Mock login response
        mock_session().post.return_value.status_code = 200
        mock_session().post.return_value.text = '{"Result": {"Result": "Success"}}'

        # Mock incomplete user profile response
        mock_profile_response = Mock()
        mock_profile_response.status_code = 200
        mock_profile_response.text = (
            '{"Result": {"user": {"Email": "test@example.com"}}}}'
        )
        mock_session().post.side_effect = [
            mock_session().post.return_value,
            mock_profile_response,
        ]

        portal = ClickPayPortal()
        with self.assertRaises(Exception) as context:
            portal.retrieve_data("testuser", "testpass")

        self.assertTrue(
            "Failed to retrieve user profile data" in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
