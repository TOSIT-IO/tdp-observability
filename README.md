# TDP Monitoring

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
tdp deploy --targets prometheus_start
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

## Roadmap

**Grafana dashboards:**

- HDFS:
  - [ ] 1 HDFS service dashboard:
    - [ ] %|Number of NameNode|DataNode|JournalNode Live
    - [ ] NameNode Heap Usage
    - [ ] HDFS Space Utilization
    - [ ] HDFS Disk Usage
    - [ ] HDFS Total Number of Blocks
    - [ ] HDFS Blocks Under-replicated or Corrupted
  - [ ] 1 HDFS NameNode dashboard
    - [ ] NameNode RPC Latency
    - [ ] NameNode Connection Load
    - [ ] NameNode GC Time
  - [ ] 1 HDFS DataNode dashboard
    - [ ] DataNode RPC Latency
    - [ ] NameNode Connection Load
    - [ ] NameNode GC Time
