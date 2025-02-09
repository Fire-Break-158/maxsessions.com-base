#!/bin/bash

# Check if .env file exists and load it
if [ -f .ENV ]; then
    export $(grep -v '^#' .ENV | xargs)
    echo "Loaded environment variables from .env"
    echo "Running in production mode with Gunicorn..."
    exec gunicorn --workers=$WORKERS --bind=$BIND_ADDRESS $MODULE_NAME
elif [ -f DEVENV ]; then
    export $(grep -v '^#' DEVENV | xargs)
    echo "Loaded environment variables from DEVENV"
    echo "Running in development mode with python..."
    exec python -m $MODULE_NAME
else
    echo ".env file not found. Shutting down."
fi