#!/bin/bash

# Install system dependencies for WeasyPrint
apt-get update
apt-get install -y libpango-1.0-0 libcairo2 libgobject-2.0-0

# Start the Gunicorn server
gunicorn app:app