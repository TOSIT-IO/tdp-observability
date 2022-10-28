# TDP Monitoring

Ansible collection to deploy a monitoring stack on top of a [TDP](https://github.com/TOSIT-IO/TDP) cluster.

For now, relies on [cloudalchemy.prometheus](https://github.com/cloudalchemy/ansible-prometheus) and [cloudalchemy.grafana](https://github.com/cloudalchemy/ansible-grafana) to deploy Prometheus and Grafana.

## Using in tdp-getting-started

```sh
cd /path/to/tdp-getting-started
# Make sure you are in TDP lib venv
source ./venv/bin/activate

# Install collection (SSH example)
git clone git@github.com:alliage-io/tdp-monitoring.git ansible_collections/alliage/tdp_monitoring

# Setup collection
## Destructive setup: this will reset tdp-lib database
./ansible_collections/alliage/tdp_monitoring/scripts/setup.sh -c

# Deploy Prometheus
tdp deploy --targets prometheus_init,grafana_init
```

Optional non-destructive option for the setup:

```sh
# Setup collection
## Non destructive: Manually add extra tdp_cluster variables to tdp_vars
## ON FIRST INSTALL ONLY
cat ansible_collections/alliage/tdp_monitoring/tdp_vars_defaults/tdp_cluster/tdp_cluster.yml |
grep -vP '^[#-]' | grep -P '^\w+' >> inventory/tdp_vars/tdp_cluster/tdp_cluster.yml
cd inventory/tdp_vars/tdp_cluster && git commit -a -m 'feat: add tdp_monitoring vars' && cd -
./ansible_collections/alliage/tdp_monitoring/scripts/setup.sh
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
