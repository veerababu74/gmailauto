"""
Updated API Client for Gmail Automation
This replaces your existing utils/api_client.py to use the new backend APIs
"""

import requests
import json
from typing import Dict, List, Any, Optional


class APIClient:
    """
    Enhanced API Client for Gmail Automation Backend
    Provides all configuration needed by the automation system
    """

    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {}

    # MAIN AUTOMATION METHODS (Compatible with existing code)

    def get_settings(self) -> Dict[str, Any]:
        """
        Get all automation settings (main API method for existing code)
        Returns a dictionary compatible with your current settings.py
        """
        return self._make_request("GET", "/automation/automation-config")

    def get_connectivity_config_with_fallback(self) -> Dict[str, Any]:
        """
        Get connectivity configuration (for existing connectivity code)
        """
        return self._make_request("GET", "/automation/automation-config/connectivity")

    # DEFAULT SENDERS METHODS

    def get_default_senders(self) -> List[str]:
        """Get list of default sender email addresses"""
        response = self._make_request(
            "GET", "/automation/automation-config/default-senders"
        )
        return response.get("DEFAULT_SENDERS", [])

    def add_default_sender(self, email: str, description: str = "") -> Dict[str, Any]:
        """Add a new default sender"""
        data = {"email": email, "description": description, "is_active": True}
        return self._make_request("POST", "/default-senders/", data)

    def update_default_sender(self, sender_id: int, **kwargs) -> Dict[str, Any]:
        """Update a default sender"""
        return self._make_request("PUT", f"/default-senders/{sender_id}", kwargs)

    def delete_default_sender(self, sender_id: int) -> Dict[str, Any]:
        """Delete a default sender"""
        return self._make_request("DELETE", f"/default-senders/{sender_id}")

    def get_all_default_senders(self) -> List[Dict[str, Any]]:
        """Get all default senders with metadata"""
        return self._make_request("GET", "/default-senders/active")

    # RANDOM URLS METHODS

    def get_random_urls(self) -> List[str]:
        """Get list of random URLs"""
        response = self._make_request(
            "GET", "/automation/automation-config/random-urls"
        )
        return response.get("RANDOM_URLS", [])

    def get_random_urls_by_category(self, category: str) -> List[str]:
        """Get random URLs filtered by category"""
        response = self._make_request("GET", f"/random-urls/by-category/{category}")
        return [url["url"] for url in response.get("urls", [])]

    def get_shuffled_random_urls(
        self, limit: int = 10, category: Optional[str] = None
    ) -> List[str]:
        """Get shuffled random URLs for automation"""
        endpoint = f"/random-urls/random?limit={limit}"
        if category:
            endpoint += f"&category={category}"
        response = self._make_request("GET", endpoint)
        return [url["url"] for url in response] if isinstance(response, list) else []

    def add_random_url(
        self, url: str, description: str = "", category: str = "other"
    ) -> Dict[str, Any]:
        """Add a new random URL"""
        data = {
            "url": url,
            "description": description,
            "category": category,
            "is_active": True,
        }
        return self._make_request("POST", "/random-urls/", data)

    def get_url_categories(self) -> List[str]:
        """Get all available URL categories"""
        return self._make_request("GET", "/random-urls/categories")

    # RANDOM WEBSITE SETTINGS METHODS

    def get_random_website_settings(self) -> Dict[str, Any]:
        """Get random website settings"""
        return self._make_request("GET", "/random-website-settings/config")

    def update_random_website_setting(
        self, setting_name: str, value: Any
    ) -> Dict[str, Any]:
        """Update a specific random website setting"""
        return self._make_request(
            "PUT",
            f"/random-website-settings/by-name/{setting_name}?setting_value={value}",
        )

    def bulk_update_random_website_settings(
        self, settings: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Bulk update random website settings"""
        data = {"settings": settings}
        return self._make_request("PUT", "/random-website-settings/bulk/update", data)

    def enable_random_websites(self, enabled: bool = True) -> Dict[str, Any]:
        """Enable or disable random website feature"""
        return self.update_random_website_setting(
            "ENABLE_RANDOM_WEBSITES", str(enabled).lower()
        )

    # CONNECTIVITY SETTINGS METHODS

    def get_connectivity_settings(self) -> Dict[str, Any]:
        """Get connectivity settings"""
        return self._make_request("GET", "/connectivity-settings/config")

    def update_connectivity_setting(
        self, setting_name: str, value: Any
    ) -> Dict[str, Any]:
        """Update a specific connectivity setting"""
        return self._make_request(
            "PUT",
            f"/connectivity-settings/by-name/{setting_name}?setting_value={value}",
        )

    def get_connectivity_test_urls(self) -> List[str]:
        """Get connectivity test URLs"""
        return self._make_request("GET", "/connectivity-settings/test-urls")

    def add_connectivity_test_url(self, url: str) -> Dict[str, Any]:
        """Add a new connectivity test URL"""
        data = {"url": url}
        return self._make_request("POST", "/connectivity-settings/test-urls", data)

    def update_connectivity_test_urls(self, urls: List[str]) -> Dict[str, Any]:
        """Update all connectivity test URLs"""
        data = {"urls": urls}
        return self._make_request(
            "PUT", "/connectivity-settings/test-urls/update", data
        )

    def enable_connectivity_manager(self, enabled: bool = True) -> Dict[str, Any]:
        """Enable or disable connectivity manager"""
        return self.update_connectivity_setting(
            "ENABLE_CONNECTIVITY_MANAGER", str(enabled).lower()
        )

    # UTILITY METHODS

    def initialize_default_settings(self) -> Dict[str, Any]:
        """Initialize all default settings"""
        return self._make_request("POST", "/automation/automation-config/initialize")

    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        return self._make_request("GET", "/automation/health")

    def is_api_available(self) -> bool:
        """Check if API is available"""
        try:
            response = self.health_check()
            return response.get("status") == "healthy"
        except:
            return False


# Example usage and integration with existing code
if __name__ == "__main__":
    # Initialize API client
    api_client = APIClient()

    # Test connectivity
    if api_client.is_api_available():
        print("✅ API is available")

        # Get all settings (compatible with existing settings.py)
        settings = api_client.get_settings()
        print(f"📋 Loaded {len(settings)} settings")

        # Example: Get specific configurations
        default_senders = api_client.get_default_senders()
        random_urls = api_client.get_random_urls()

        print(f"📧 Default senders: {len(default_senders)}")
        print(f"🌐 Random URLs: {len(random_urls)}")

        # Example: Update a setting
        result = api_client.enable_random_websites(True)
        print(f"🔧 Updated random websites setting: {result.get('setting_value')}")

    else:
        print("❌ API is not available")
        print("Please ensure the backend server is running on http://localhost:8000")
