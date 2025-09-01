from typing import Optional, Literal
import httpx
from novalad.api.base import BaseAPIClient
from novalad.api.config import SUPPORTED_FILE_EXTENSIONS, UPLOAD_ENDPOINT, PROCESS_ENDPOINT, STATUS_ENDPOINT, OUTPUT_ENDPOINT
from novalad.utils.io import (
    is_filepath, is_folderpath, get_files_from_folder,
    get_file_extension, get_filename,is_cloud_storage_path,
    is_valid_url, extract_filename_from_url
)
from novalad.api.exception import APIError, InvalidArgumentException, FileFormatNotSupportedException, FileNotUploaded
from novalad.utils.progress import tqdm

class NovaladClient(BaseAPIClient):
    """
    A client for interacting with the Novalad API for file uploads.
    
    Attributes:
        api_key (Optional[str]): API key for authentication.
        file_id (Optional[str]): Stores the file ID after a successful upload.
    """
    
    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initializes the NovaladClient with an optional API key.

        :param api_key: The API key for authentication.
        """
        super().__init__(api_key)

    def _upload_url(self, file_path: str) -> str:
        """
        Retrieves a pre-signed upload URL from the Novalad API.

        :param file_path: Path to the file to be uploaded.
        :return: The pre-signed upload URL.
        :raises FileFormatNotSupportedException: If the file format is not supported.
        :raises APIError: If the API call fails.
        """
        filename = get_filename(file_path)
        file_extension = get_file_extension(filename)

        if file_extension not in SUPPORTED_FILE_EXTENSIONS:
            raise FileFormatNotSupportedException(f"Only supports {SUPPORTED_FILE_EXTENSIONS}")
        
        params = {"filename": filename}
        print(f"DEBUG: Upload request details:")
        print(f"  - Filename: {filename}")
        print(f"  - Full path: {file_path}")
        print(f"  - API endpoint: {UPLOAD_ENDPOINT}")
        print(f"  - Request params: {params}")
        
        response = self._api_call(route=UPLOAD_ENDPOINT, params=params)
        
        print(f"DEBUG: API Response:")
        print(f"  - Response: {response}")
        print(f"  - Response type: {type(response)}")
        if isinstance(response, dict):
            print(f"  - Response keys: {list(response.keys())}")
        
        self.file_id = response.get("fileid")
        upload_url = response.get("upload_url")
        
        print(f"DEBUG: Extracted values:")
        print(f"  - file_id: {self.file_id}")
        print(f"  - upload_url: {upload_url}")

        if not upload_url:
            raise APIError(message="Could not retrieve upload URL from the API.")
        
        return upload_url

    def _upload_to_cloud(self, file_path: str, upload_url: str) -> None:
        """
        Uploads a file to cloud storage using a pre-signed URL.

        :param file_path: Path to the file to be uploaded.
        :param upload_url: The pre-signed upload URL.
        :raises APIError: If the upload fails.
        """
        try:
            with open(file_path, "rb") as file_data:
                response = httpx.put(upload_url, content=file_data)
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(message=f"Upload failed with status {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise APIError(message=f"An error occurred during file upload: {str(e)}")
    
    def upload(self, file_path: Optional[str] = None, folder_path: Optional[str] = None) -> None:
        """
        Uploads a single file or all supported files in a folder.

        :param file_path: Path to a single file to upload.
        :param folder_path: Path to a folder containing multiple files to upload.
        :raises InvalidArgumentException: If both or neither of file_path and folder_path are provided.
        :raises APIError: If the upload process encounters an error.
        """
        if (file_path is None and folder_path is None) or (file_path is not None and folder_path is not None):
            raise InvalidArgumentException("You must provide either 'file_path' or 'folder_path', but not both.")
        
        if file_path and is_filepath(file_path):
            upload_url = self._upload_url(file_path)
            self._upload_to_cloud(file_path, upload_url)
        
        elif folder_path and is_folderpath(folder_path):
            files = get_files_from_folder(folder_path)
            supported_files = [
                f for f in files if get_file_extension(get_filename(f)) in SUPPORTED_FILE_EXTENSIONS
            ]
            
            for file in tqdm(supported_files, desc="Uploading files"):
                upload_url = self._upload_url(file)
                self._upload_to_cloud(file, upload_url)

        else:
            raise InvalidArgumentException("You must provide either 'file_path' or 'folder_path'.")

        if self.file_id is None:
            raise APIError(message="Could not upload file")

    def run(self, url : str = None,
            skip_non_important_images : bool = True,
            skip_image_insights : bool = False,
            skip_header_footer : bool = False,
            ):
        
        payload = {
            "skip_images" : skip_non_important_images,
            "skip_insights" : skip_image_insights,
            "skip_header_footer" : skip_header_footer
        }

        if (self.file_id is None and url is None) or (self.file_id is not None and url is not None):
            raise InvalidArgumentException("You must upload local file or provide 'url', but not both.")

        if (url is not None) and (is_valid_url(url) or is_cloud_storage_path(url)):
            filename = extract_filename_from_url(url)
            file_extension = get_file_extension(filename)

            if file_extension not in SUPPORTED_FILE_EXTENSIONS:
                raise FileFormatNotSupportedException(f"Only supports {SUPPORTED_FILE_EXTENSIONS}")
            
            payload["file_url"] = url

        if (self.file_id is not None):
            payload["file_id"] = self.file_id

        response = self._api_call(route=PROCESS_ENDPOINT,method="post", body=payload)

        self.run_id = response.get("run_id",None)

        if self.run_id is None:
            raise APIError(message="Could not process request")
        

    def status(self):

        if self.run_id is None:
            raise ValueError("Request is not Initiated, Kindly Upload/Process the Document")
        
        params = {"run_id" : self.run_id}

        response = self._api_call(route=STATUS_ENDPOINT,params=params)

        return response
    
    def output(self, format: Literal["json","markdown","document","graph"] = "json"):

        if self.run_id is None:
            raise ValueError("Request is not Initiated, Kindly Upload/Process the Document")
        
        params = {"run_id" : self.run_id , "format" : format}

        response = self._api_call(route=OUTPUT_ENDPOINT,params=params)

        return response








        

        

