#!/usr/bin/env bash

# Define color codes for messages
COLOR_RESET="\033[0m"
COLOR_INFO="\033[1;34m"
COLOR_SUCCESS="\033[1;32m"
COLOR_FAIL="\033[1;31m"
COLOR_WARNING="\033[1;33m"

# Functions for messages with colors
info_message() {
  echo -e "${COLOR_INFO}[INFO] $1${COLOR_RESET}"
}

success_message() {
  echo -e "${COLOR_SUCCESS}[SUCCESS] $1${COLOR_RESET}"
}

fail_message() {
  echo -e "${COLOR_FAIL}[FAIL] $1${COLOR_RESET}"
}

warning_message() {
  echo -e "${COLOR_WARNING}[WARNING] $1${COLOR_RESET}"
}

# Install dependencies
info_message "Installing dependencies"
uv sync

# Check if pre-commit is installed
if ! command -v pre-commit &>/dev/null; then
  info_message "Installing pre-commit"
  pre-commit install
else
  info_message "pre-commit is already installed"
fi

# Run unit tests
info_message "Running Unit Tests"
if ! pytest; then
  fail_message "One or more unit tests failed"
  exit 1
fi

success_message "Build Done!"
