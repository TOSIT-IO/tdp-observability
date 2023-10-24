#!/bin/bash
# Copyright 2022 TOSIT.IO
# SPDX-License-Identifier: Apache-2.0

CLEAN="false"

parse_cmdline() {
  local OPTIND
  while getopts 'c' options; do
    case "$options" in
    c) CLEAN="true" ;;
    *) return 1 ;;
    esac
  done
  shift $((OPTIND - 1))
  return 0
}

create_symlink_if_needed() {
  local target=$1
  local link_name=$2
  if [[ "$CLEAN" == "true" ]]; then
    echo "Remove '${link_name}'"
    rm -rf "$link_name"
  fi
  if [[ -e "$link_name" ]] || [[ -L "$link_name" ]]; then
    echo "File '${link_name}' exists, nothing to do"
    return 0
  fi
  echo "Create symlink '${link_name}'"
  ln -s "$target" "$link_name"
}

init_collection() {
  if [[ "$CLEAN" == "true" ]]; then
    echo "Delete sqlite.db if exists"
    rm -f sqlite.db
    echo "Delete tdp_vars/tdp-cluster"
    rm -rf inventory/tdp_vars/tdp-cluster
    echo "Delete tdp_vars/gafana"
    rm -rf inventory/tdp_vars/grafana
    echo "Delete tdp_vars/prometheus"
    rm -rf inventory/tdp_vars/prometheus
  fi
  tdp init --overrides tdp_vars_overrides
}

parse_cmdline "$@"

tdp_observability_path='ansible_collections/tosit/tdp_observability'

# Add tdp_observability topology to inventory
create_symlink_if_needed "../../$tdp_observability_path/topology.ini" "inventory/topologies/observability"

# Install Python packages
pip install -r "ansible_collections/tosit/tdp_observability/requirements.txt"

# Add tdp_observability path to TDP_COLLECTION_PATH
sed -ri "s|TDP_COLLECTION_PATH=((ansible_collections/tosit/tdp)(:?ansible_collections/tosit/\w*)*)(:$tdp_observability_path)?$|TDP_COLLECTION_PATH=\1:$tdp_observability_path|" .env

# Init collection (delete sqlite.db if needed)
init_collection
