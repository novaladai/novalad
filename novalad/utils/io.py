import os
from typing import List
import re
from urllib.parse import urlparse

def isdir(path : str) -> bool:
    return os.path.isdir(path)

def get_filename(path: str) -> str:
    """
    Extracts and returns the filename (including extension) from the given file path.
    
    Handles cases like:
    - Hidden files (e.g., ".gitignore")
    - Files with multiple dots (e.g., "archive.tar.gz")
    - Paths with or without directories
    
    :param path: The file path as a string
    :return: The filename including the extension
    """
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Invalid file path provided")
    
    return os.path.basename(path)  # Extracts and returns the full filename

def get_file_extension(path: str) -> str:
    """
    Extracts and returns the file extension from the given file path.
    
    Handles cases like:
    - Hidden files with no extension (e.g., ".gitignore")
    - Files with multiple dots (e.g., "archive.tar.gz")
    - Paths with or without directories
    - No extension cases
    
    :param path: The file path as a string
    :return: The file extension including the dot (e.g., ".txt") or an empty string if no extension exists
    """
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Invalid file path provided")
    
    filename = os.path.basename(path)  # Extracts the filename from path
    
    if filename.startswith('.') and filename.count('.') == 1:
        return ''  # Hidden files without an extension (e.g., .gitignore)
    
    _, ext = os.path.splitext(filename)  # Extracts the extension
    
    return ext.replace(".","") if ext else ''  # Return empty string if no extension

def get_filename_without_extension(path: str) -> str:
    """
    Extracts and returns the filename (without extension) from the given file path.
    
    Handles cases like:
    - Hidden files (e.g., ".gitignore")
    - Files with multiple dots (e.g., "archive.tar.gz")
    - Paths with or without directories
    
    :param path: The file path as a string
    :return: The filename without extension
    """
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Invalid file path provided")
    
    filename = os.path.basename(path)  # Extracts the filename from path
    name, _ = os.path.splitext(filename)  # Extracts the filename without extension
    
    return name

def is_filepath(file_path: str) -> bool:
    """
    Checks if the given path is a valid file path.
    
    :param file_path: The file path as a string
    :return: True if it is a file, False otherwise
    """
    if not isinstance(file_path, str) or not file_path.strip():
        return False
    return os.path.isfile(file_path)

def is_folderpath(folder_path: str) -> bool:
    """
    Checks if the given path is a valid directory path.
    
    :param folder_path: The folder path as a string
    :return: True if it is a directory, False otherwise
    """
    if not isinstance(folder_path, str) or not folder_path.strip():
        return False
    return os.path.isdir(folder_path)

def get_files_from_folder(folder_path: str) -> List[str]:
    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.abspath(os.path.join(root, file))  # Get the absolute full path
            file_list.append(full_path)

    return file_list

def is_valid_url(string) -> bool:
    # Regular expression to match URLs
    url_regex = re.compile(
        r'^(https?://)?'  # http:// or https:// (optional)
        r'([a-zA-Z0-9.-]+)?'  # Domain name
        r'(\.[a-zA-Z]{2,})'  # Top-level domain
        r'(:\d+)?'  # Port (optional)
        r'(/[^\s]*)?$',  # Path (optional)
        re.IGNORECASE
    )
    return bool(url_regex.match(string))

def is_cloud_storage_path(path: str) -> bool:
    """
    Check if the provided path corresponds to a cloud provider (S3, Azure Blob, or GCS).

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path corresponds to a cloud provider (S3, Azure, or GCS), 
              False otherwise.
    """
    # Check for S3 path (s3://)
    if path.lower().startswith("s3://"):
        return True
    
    # Check for Azure Blob path (https://<account_name>.blob.core.windows.net/ or azure://)
    elif re.match(r"^https://[a-zA-Z0-9\-]+\.blob\.core\.windows\.net/", path):
        return True
    elif path.lower().startswith("azure://"):
        return True
    
    # Check for GCS path (gs://)
    elif path.lower().startswith("gs://"):
        return True
    
    # If no match, return False
    return False

def extract_filename_from_url(url: str) -> str:
    """
    Extracts the filename from an AWS S3 presigned URL.

    Args:
        url (str): The S3 presigned URL.

    Returns:
        str: The extracted filename.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # The filename is typically the last part of the path
    filename = os.path.basename(parsed_url.path)
    
    return filename