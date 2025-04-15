import fitz  # PyMuPDF
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import random

from novalad.api.config import SUPPORTED_FILE_EXTENSIONS
from novalad.api.exception import FileFormatNotSupportedException
from novalad.utils.io import isdir, is_filepath, get_file_extension


# Define all known element types that should have distinct colors
ELEMENT_TYPES = [
    "image", "image_caption", "list_item", "page_footer", "page_header",
    "section", "table", "table_caption", "table_of_content", "text", "title"
]

def _generate_random_color(seed_str: str) -> tuple:
    """
    Generates a consistent dark RGB color based on a seed string.

    Args:
        seed_str (str): A string to seed the random generator for consistent colors.

    Returns:
        tuple: A tuple of (R, G, B) values representing a dark color.
    """
    random.seed(seed_str)
    return tuple(random.randint(0, 100) for _ in range(3))  # Lower range for dark shades

# Assign random colors to element types
element_colors = {etype: _generate_random_color(etype) for etype in ELEMENT_TYPES}
element_colors["group"] = (255, 255, 0)  # Fixed color for groups
element_colors["skipped"] = (128, 128, 128)  # Optional fallback for skipped visuals


def render_elements(file_path: str, output: dict, save_dir: str = None) -> None:
    """
    Renders and visualizes extracted elements on top of PDF page images.
    Each element type is color-coded with consistent random colors.
    
    Args:
        file_path (str): Path to the input PDF file.
        output (dict): Dictionary containing extracted layout data.
        save_dir (str, optional): Directory to save annotated images.
    
    Raises:
        FileExistsError: If the file path does not exist.
        FileFormatNotSupportedException: If file extension is not supported.
        ValueError: If unsupported format like PPT is passed.

    Returns:
        None
    """
    
    if not is_filepath(file_path):
        raise FileExistsError("File Not Found")
    
    file_ext = get_file_extension(file_path)

    if file_ext not in SUPPORTED_FILE_EXTENSIONS:
        raise FileFormatNotSupportedException(f"Only supports {SUPPORTED_FILE_EXTENSIONS}")

    if file_ext == "pdf":
        pdf_document = fitz.open(file_path)
        
        for page_data in output["data"]["extraction"]:
            page_number = page_data["page_number"] - 1
            page = pdf_document[page_number]

            # Convert page to image
            pix = page.get_pixmap()
            img = np.array(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            # Skipped images
            for skip_id in page_data["skipped_images"]:
                element = page_data["elements"].get(skip_id)
                if element:
                    bbox = element["pixel_coordinates"]
                    left, top, right, bottom = map(int, [bbox["left"], bbox["top"], bbox["right"], bbox["bottom"]])
                    label = element["type"]
                    color = element_colors.get(label, element_colors["skipped"])
                    cv2.rectangle(img, (left, top), (right, bottom), color, 2)
                    cv2.line(img, (left, top), (right, bottom), color, 2)
                    cv2.line(img, (left, bottom), (right, top), color, 2)
                    cv2.putText(img, "skipped", (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Groups
            for group in page_data["groups"]:
                min_left = float('inf')
                min_top = float('inf')
                max_right = float('-inf')
                max_bottom = float('-inf')

                for element_id in group["ids"]:
                    coords = page_data["elements"].get(element_id)
                    if coords:
                        bbox = coords["pixel_coordinates"]
                        min_left = min(min_left, bbox["left"])
                        min_top = min(min_top, bbox["top"])
                        max_right = max(max_right, bbox["right"])
                        max_bottom = max(max_bottom, bbox["bottom"])

                if all(val != float('inf') and val != float('-inf') for val in [min_left, min_top, max_right, max_bottom]):
                    label = group["type"]
                    color = element_colors.get(label, element_colors["group"])
                    cv2.rectangle(
                        img, 
                        (int(min_left) - 5, int(min_top) - 5), 
                        (int(max_right) + 5, int(max_bottom) + 5), 
                        color, 
                        2
                    )
                    cv2.putText(img, label, (int(min_left), int(min_top) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # All individual elements
            for element_id, element in page_data["elements"].items():
                bbox = element["pixel_coordinates"]
                left, top, right, bottom = map(int, [bbox["left"], bbox["top"], bbox["right"], bbox["bottom"]])
                label = element["type"]
                color = element_colors.get(label, (0, 255, 155))
                cv2.rectangle(img, (left, top), (right, bottom), color, 1)
                cv2.putText(img, label, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Convert and save/show
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            if save_dir is not None and isdir(save_dir):
                output_path = os.path.join(save_dir, f"{page_number}.jpg")
                cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

            # Display inline
            plt.figure(figsize=(10, 10))
            plt.imshow(img)
            plt.axis("off")
            plt.show()

    elif file_ext in ["ppt", "pptx"]:
        raise ValueError("Unsupported file format. Please provide a PDF")
    else:
        raise ValueError("Unsupported file format. Please provide a PDF")
