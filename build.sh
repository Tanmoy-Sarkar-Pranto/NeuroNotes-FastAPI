#!/usr/bin/env bash
# build.sh

set -o errexit  # exit on error

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo "Build completed successfully!"
