"""
progress.py

A utility module for handling progress bars in both Jupyter environments 
(Jupyter Notebook, JupyterLab, Kaggle, Deepnote, Google Colab, etc.) and 
standard console/terminal execution.

This module dynamically selects the best tqdm implementation based on the 
current environment.

Usage:
    from your_package_name.progress import tqdm

    for i in tqdm(range(100), desc="Processing"):
        # Your loop code here
        pass
"""

from tqdm import tqdm as std_tqdm
from tqdm.auto import tqdm as auto_tqdm
from typing import Any


def is_notebook() -> bool:
    """
    Detect if the code is running inside a Jupyter-like environment.

    This function checks if the script is running in:
    - Jupyter Notebook
    - JupyterLab
    - Google Colab
    - Kaggle Notebooks
    - Deepnote
    - VS Code with Jupyter Extension

    Returns:
        bool: True if running in a Jupyter environment, False otherwise.

    Example:
        >>> is_notebook()
        True  # If running in a Jupyter Notebook
        False # If running in a terminal or script
    """
    try:
        from IPython import get_ipython
        shell: str = get_ipython().__class__.__name__

        if shell in ("ZMQInteractiveShell", "GoogleColabShell"):
            return True  # Running in a Jupyter-like environment
    except (NameError, ImportError):
        pass

    return False


# Dynamically select the appropriate tqdm version based on the environment
tqdm: Any = auto_tqdm if is_notebook() else std_tqdm

# Define what is available for import when using `from progress import *`
__all__ = ["tqdm"]
