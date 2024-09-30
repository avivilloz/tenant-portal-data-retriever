import requests
import json
from .base import TenantPortal
from ..logger import logger
from ..config import CLICKPAY_BASE_URL


class ClickPayPortal(TenantPortal):
    """Implementation of the TenantPortal for ClickPay using requests."""

    def __init__(self):
        self.session = requests.Session()
        self.base_url = CLICKPAY_BASE_URL
        self.username = None
        self.password = None

    def retrieve_data(self, username, password):
        try:
            self._login(username, password)

            # Check if we're still logged in
            if not self._check_login_status():
                logger.error("User is not logged in after login attempt")
                raise Exception("Login failed")

            user_data = self._get_user_profile()

            return {
                "email": user_data["email"],
                "phone": user_data["phone"],
            }
        except Exception as e:
            logger.error(f"Failed to retrieve data from ClickPay: {str(e)}")
            raise
        finally:
            self._logout()

    def _login(self, username, password):
        self.username = username
        self.password = password
        login_data = {
            "username": username,
            "password": password,
            "validateUsername": True,
        }

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }
        login_url = f"{self.base_url}/MobileService/Service.asmx/login"
        response = self.session.post(login_url, json=login_data, headers=headers)

        if response.status_code != 200:
            logger.error(f"Login failed. Response content: {response.text[:500]}...")
            raise Exception("Login failed")

        try:
            first_json, _ = response.text.split('{"d":null}')
            login_result = json.loads(first_json)

            if login_result.get("Result", {}).get("Result") != "Success":
                logger.error(f"Login failed. Response content: {login_result}")
                raise Exception("Login failed")
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse login response. Error: {str(e)}")
            raise Exception("Login failed")

        logger.info("Login successful")

    def _get_user_profile(self):
        profile_url = f"{self.base_url}/MobileService/Service.asmx/getUserContextJSON"
        payload = "NovelPayApp"  # Send as plain text
        headers = {
            "Content-Type": "text/plain;charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }

        response = self.session.post(profile_url, data=payload, headers=headers)
        if response.status_code != 200:
            logger.error(
                f"Failed to retrieve user profile. Response content: {response.text[:500]}..."
            )
            raise Exception("Failed to retrieve user profile data")

        try:
            profile_data = json.loads(response.text)
            logger.debug(f"Parsed profile data:\n{json.dumps(profile_data, indent=2)}")

            result = profile_data.get("Result", {})
            user_data = result.get("user", {})

            logger.debug(f"User data:\n{json.dumps(user_data, indent=2)}")

            email = user_data.get("Email")
            phone = user_data.get("Cellphone")

            if not email or not phone:
                logger.error(
                    f"Email or phone not found in profile data. User data:\n{json.dumps(user_data, indent=2)}"
                )
                raise Exception("Failed to retrieve user profile data")

            return {"email": email, "phone": phone}

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse user profile JSON. Error: {str(e)}")
            raise Exception("Failed to retrieve user profile data")

    def _logout(self):
        logout_url = f"{self.base_url}/app#PayNow"
        self.session.get(logout_url)
        logger.info("Logout successful")

    def _check_login_status(self):
        check_url = f"{self.base_url}/app#UserProfile"
        response = self.session.get(check_url)
        return "Logout" in response.text
