# TDP Monitoring

Ansible collection to deploy a monitoring stack on top of a [TDP](https://github.com/TOSIT-IO/TDP) cluster.

## Download binaries

Binaries must be present inside `files` directory located next to launched playbooks. They can be found here:

- Prometheus: https://github.com/prometheus/prometheus/releases

## Using in tdp-getting-started

```sh
cd /path/to/tdp-getting-started
# Make sure you are in TDP lib venv
source ./venv/bin/activate

# Install collection (SSH example)
git clone git@github.com:TOSIT-IO/tdp-observability.git \
  ansible_collections/tosit/tdp_observability \
  --recurse-submodules

# Setup collection
## Destructive setup: this will reset tdp-lib database
./ansible_collections/tosit/tdp_observability/scripts/setup.sh -c

# Configure deployment plan for Prometheus and grafana
tdp plan dag --target prometheus_init --target grafana_init

# Deploy Prometheus and grafana
tdp deploy
```

Optional non-destructive option for the setup:

```sh
# Setup collection
## Non destructive: Manually add extra tdp_cluster variables to tdp_vars
## ON FIRST INSTALL ONLY
cat ansible_collections/tosit/tdp_observability/tdp_vars_defaults/tdp_cluster/tdp_cluster.yml |
grep -vP '^[#-]' | grep -P '^\w+' >> inventory/tdp_vars/tdp_cluster/tdp_cluster.yml
cd inventory/tdp_vars/tdp_cluster && git commit -a -m 'feat: add tdp_observability vars' && cd -
./ansible_collections/tosit/tdp_monitoring/scripts/setup.sh
```

## Web UI links

- Prometheus targets: https://master-01.tdp:9090/targets

  - Username: `admin`
  - Password: `PrometheusAdmin123`

- Grafana: https://master-01.tdp:3000
  - Username: `admin`
  - Password: `GrafanaAdmin123`

## Roadmap

- Grafana:
  - [ ] Use cluster PostgreSQL as back-end database
