#!/bin/bash

# Script to delete all __pycache__ folders and their contents

# Find and remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +

find . -type d -name ".pytest_cache" -exec rm -rf {} +

echo "All __pycache__ folders have been deleted."
echo "All .pytest_cache folders have been deleted."