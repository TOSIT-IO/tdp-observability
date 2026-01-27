# TDP Monitoring

Ansible collection to deploy a monitoring stack on top of a [TDP](https://github.com/TOSIT-IO/TDP) cluster.

## Available Roles

- tosit.alloy.agent
- tosit.exporter.node
- tosit.grafana.server
- tosit.loki.server
- tosit.prometheus.alertmanager
- tosit.prometheus.server

## Prerequisites

A python requirements files is provided with the collection. Install it on your venv with the following command
```
pip install -r requirements.txt
```

## Download binaries

Binaries must be present inside `files` directory located next to launched playbooks. They can be found here:

- Grafana : https://github.com/grafana/grafana/releases
- Prometheus: https://github.com/prometheus/prometheus/releases
- Loki : https://github.com/grafana/loki/releases/latest
- Node exporter : https://github.com/prometheus/node_exporter/releases
- Alloy : https://github.com/grafana/alloy/releases

## Web UI links

- Prometheus targets: https://master-01.tdp:9090/targets

  - Username: `admin`
  - Password: `PrometheusAdmin123`

- Grafana: https://master-01.tdp:3000
  - Username: `admin`
  - Password: `GrafanaAdmin123`

