#!/bin/bash

# Install system dependencies for WeasyPrint using the correct package names
apt-get update
apt-get install -y libgobject2.0-dev libcairo2-dev libpango1.0-dev pkg-config

# Start the Gunicorn server
gunicorn app:app