#!/usr/bin/env bash

set -e

COLOR_RESET="\033[0m"
COLOR_INFO="\033[1;34m"
COLOR_SUCCESS="\033[1;32m"
COLOR_FAIL="\033[1;31m"

info_message() {
  echo -e "${COLOR_INFO}[INFO] $1${COLOR_RESET}"
}

success_message() {
  echo -e "${COLOR_SUCCESS}[SUCCESS] $1${COLOR_RESET}"
}

fail_message() {
  echo -e "${COLOR_FAIL}[FAIL] $1${COLOR_RESET}"
}

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
if ! uv build --verbose; then
  fail_message "Build process failed"
  exit 1
fi

success_message "Build Done!"
