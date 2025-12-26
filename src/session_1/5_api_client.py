"""
API Client Example
Reference: docs/session_1/4_apis_websockets_http.md
"""

import requests
from typing import Optional, Dict, Any

class APIClient:
    """Generic API client for AI services"""
    
    def __init__(self, base_url: str, api_key: str):
        """Initialize API client"""
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()  # Raise error if bad status
        return response.json()
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def stream_post(self, endpoint: str, data: Dict[str, Any]):
        """Stream POST request"""
        url = f"{self.base_url}/{endpoint}"
        data["stream"] = True
        response = requests.post(url, json=data, headers=self.headers, stream=True)
        response.raise_for_status()
        return response


def safe_api_call(url: str, headers: dict, data: dict = None):
    """Safely call API with error handling"""
    try:
        if data:
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        # Check status code
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP Error: {e}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection failed"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {e}"}


# Example usage
if __name__ == "__main__":
    # Initialize client (replace with actual API key)
    # client = APIClient(
    #     base_url="https://api.openai.com/v1",
    #     api_key="YOUR_API_KEY"
    # )
    
    # Example safe call
    result = safe_api_call(
        url="https://api.example.com/data",
        headers={"Authorization": "Bearer token"}
    )
    print(result)

