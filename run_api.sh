#!/usr/bin/env bash

# Run the API

cleanup() {
  # Get the PID of the Python process
  local pid=$(ps -ef | grep '[p]ython -m app' | awk '{print $2}')

  # If the process is running, kill it
  if [[ -n $pid ]]; then
    echo "Stopping the API"
    kill $pid
  fi

  echo "Deactivating the virtual environment"
  deactivate

  echo "Cleaning up the virtual environment"
  rm -rf venv

  echo "Exiting the script"
}

run_server() {
  echo "Creating a virtual environment"
  python3 -m venv venv

  echo "Activating the virtual environment"
  source venv/bin/activate || . venv/bin/activate

  # Trap SIGINT and SIGTERM signals and cleanup before exiting
  trap cleanup SIGINT SIGTERM EXIT

  echo "Installing requirements"
  pip install -r requirements.txt

  echo "Running the API"
  
  # Check if the API key is provided
  if [[ -z $1 ]]; then
    echo "API key is missing"
    exit 1
  fi
  
  python -m app --api_key "$1"
}

run_server "$1"

exit 0