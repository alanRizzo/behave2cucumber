#!/usr/bin/env bash

set -e
source ./colors.sh

if ! command -v twine &>/dev/null; then
  fail_message "twine is not installed. Run 'uv pip install twine' or 'pip install twine' first."
  exit 1
fi

info_message "Twine current version: $(uv pip show twine | grep Version)"

echo -n "Are you sure you want to upload the distribution? (y/N): "
read -r CONFIRM
if [[ "$CONFIRM" != "y" ]]; then
  info_message "Upload canceled."
  exit 0
fi

info_message "Uploading dist/* using twine..."
if twine upload dist/*; then
  success_message "Upload completed successfully."
else
  fail_message "Upload failed. Check your setup and try again."
  exit 1
fi
