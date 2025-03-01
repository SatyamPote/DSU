#!/bin/bash

# Change directory to the project root (if needed)
cd ..  # Remove this line

# Install requirements
pip install -r requirements.txt

# Set the PYTHONPATH to include the project root
export PYTHONPATH=/opt/render/project/src:$PYTHONPATH

# Print the PYTHONPATH for debugging
echo "PYTHONPATH: $PYTHONPATH"

# Run Gunicorn
gunicorn --bind 0.0.0.0:${PORT:-8000} CST.wsgi