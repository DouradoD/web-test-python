#!/bin/bash
VENV_PATH="venv"
if [[ -d "$VENV_PATH" ]]; then
  echo "A venv already exists at $VENV_PATH. Removing it..."
  rm -r "$VENV_PATH"
fi

echo "Creating virtualenv at $VENV_PATH..."
"python$PYTHON_VERSION" -m venv "$VENV_PATH"
echo "Activating venv..."
source "$VENV_PATH"/bin/activate
echo "Updating venv site packages..."
pip install pip setuptools -U
pip install -r requirements.txt
