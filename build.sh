#!/usr/bin/env bash

set -e
source ./colors.sh

info_message "Cleaning up previous build artifacts"
find . -type d -name "__pycache__" -exec rm -r {} + || true
rm -rf dist pepyno.log src/*.egg-info || true

info_message "Installing dependencies"
uv sync || fail_message "Dependency installation failed"

if ! command -v pre-commit &>/dev/null; then
  info_message "Installing pre-commit"
  pre-commit install || fail_message "Failed to install pre-commit"
else
  info_message "pre-commit is already installed"
fi

info_message "Running Unit Tests"
if ! pytest; then
  fail_message "One or more unit tests failed"
  exit 1
fi

info_message "Building package"
if ! uv build --quiet; then
  fail_message "Build process failed"
  exit 1
fi

success_message "Build Done!"
