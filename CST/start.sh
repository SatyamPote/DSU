#!/bin/bash

# Change directory to the project root (if needed)
cd ..

# Install requirements
pip install -r requirements.txt

# Set the PYTHONPATH to include the project root
export PYTHONPATH=$PYTHONPATH:/opt/render/project/src

# Print the PYTHONPATH for debugging
echo "PYTHONPATH: $PYTHONPATH"

# Run Gunicorn
gunicorn CST.wsgi