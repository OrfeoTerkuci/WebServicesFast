#!/usr/bin/env bash

# Run the API

run_server() {
  echo "Creating a virtual environment"
  python3 -m venv venv

  echo "Activating the virtual environment"
  source venv/bin/activate || . venv/bin/activate

  echo "Installing requirements"
  pip install -r requirements.txt

  echo "Running the API"
  python -m app --api_key "$1"
}

run_server "$1"
