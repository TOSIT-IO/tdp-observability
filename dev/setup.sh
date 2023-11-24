#!/usr/bin/env bash
# Copyright 2022 TOSIT.IO
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

readonly PYTHON_BIN=${PYTHON_BIN:-python3}
readonly PYTHON_VENV=${PYTHON_VENV:-venv}

setup_python_venv() {
  if [[ ! -d "$PYTHON_VENV" ]]; then
    echo "Create python venv with '${PYTHON_BIN}' to '${PYTHON_VENV}' and update pip to latest version"
    "$PYTHON_BIN" -m venv "$PYTHON_VENV"
    (
      source "${PYTHON_VENV}/bin/activate"
      pip install -U pip
    )
  else
    echo "Python venv '${PYTHON_VENV}' already exists, nothing to do"
  fi
  echo "Install python dependencies"
  (
    source "${PYTHON_VENV}/bin/activate"
    pip install -r dev/requirements.txt
    ansible-galaxy collection install community.general
  )
  return 0
}

main() {
  setup_python_venv
  echo
  echo "=========================================================================================="
  echo "Done installing venv."
  echo
  echo "To run ansible-lint localy you should :"
  echo " - export ANSIBLE_COLLECTIONS_PATH to a path containing 'ansible_collections/tosit/<tdp-collection>"
  echo "   suggestion : export ANSIBLE_COLLECTIONS_PATH="$(realpath $(pwd)/../../..)
  echo " - activate new python venv by running 'source venv/bin/activate'"
  echo " - run ansible-lint"
  echo "=========================================================================================="
}

main "$@"
