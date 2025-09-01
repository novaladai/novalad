from novalad.api.config import API_BASE_URL,DEFAULT_TIMEOUT, UPLOAD_ENDPOINT, STATUS_ENDPOINT, OUTPUT_ENDPOINT, PROCESS_ENDPOINT
from novalad.api.exception import APIError,AuthenticationError, APITimeoutError
from typing import Optional, Literal
import os
import httpx

class BaseAPIClient:
    """
    Base API client for interacting with Novalad API.

    This class handles API authentication using an API key and sets up
    necessary headers for API requests.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initializes the BaseAPIClient with the given API key.
        
        Args:
            api_key (Optional[str]): The API key for authentication. If not provided,
                                     it attempts to retrieve it from the environment variable.
        
        Raises:
            AuthenticationError: If no API key is provided or found in environment variables.
        """
        self.base_api_url: str = API_BASE_URL
        self.upload_endpoint = UPLOAD_ENDPOINT
        self.status_endpoint = STATUS_ENDPOINT
        self.output_endpoint = OUTPUT_ENDPOINT
        self.process_endpoint = PROCESS_ENDPOINT
        self.file_id = None
        self.run_id = None
        if self._api_key_present(api_key):
            self.api_key: str = api_key  # Store the API key
            self.headers: dict = {"X-API-KEY": self.api_key,"Content-Type":"application/json"}  # Set request headers

    def _api_key_present(self, api_key: Optional[str]) -> bool:
        """
        Checks if the API key is provided, either directly or via environment variable.
        
        Args:
            api_key (Optional[str]): The API key to check.
        
        Returns:
            bool: True if the API key is present, otherwise raises AuthenticationError.
        
        Raises:
            AuthenticationError: If the API key is missing.
        """
        api_key = os.getenv("NOVALAD_API_KEY", api_key)
        if api_key is None:
            raise AuthenticationError(message="Missing/Invalid API Key")
        return True
    
    def _api_call(self,route : str, method : Literal["get","post"] = "get", params : dict = {}, body : dict = {}):
        try:
            if method.lower() == "get":
                response = httpx.get(f"{API_BASE_URL}{route}",
                                    params=params,
                                    headers=self.headers,
                                    timeout=DEFAULT_TIMEOUT)
            elif method.lower() == "post":
                response = httpx.post(f"{API_BASE_URL}{route}",
                                        headers=self.headers,
                                        json=body,
                                        timeout=DEFAULT_TIMEOUT)

            else:
                raise APIError(message="Invalid API Request",request=httpx.Request)
            
            response.raise_for_status()  # Raise an error for HTTP 4xx/5xx responses
            return response.json()
        except httpx.TimeoutException:
            raise APITimeoutError(request=httpx.Request)

        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise APIError(message=f"HTTP Error {e.response.status_code}: {e.response.text}")

        except httpx.RequestError as e:
            print("Network error occurred!")
            raise APIError(message=f"Network error: {str(e)}")
        
        # If we reach here, something unexpected happened
        raise APIError(message="Unexpected error in API call")