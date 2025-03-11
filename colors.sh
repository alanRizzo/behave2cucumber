#!/usr/bin/env bash
#
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
