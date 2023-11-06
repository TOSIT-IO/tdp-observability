# Roles
## Prometheus/server

Based on role prometheus from [prometheus-community/ansible](https://github.com/prometheus-community/ansible.git) 0.7.0
List of adaptations :
| file                                       | comments                                                                                     |
| ------------------------------------------ | -------------------------------------------------------------------------------------------- |
| tdp_vars_default/prometheus/prometheus.yml | adapted from `default/main.yml` community file                                               | 
| handlers/main.yml                          | completely changed. Only one handler for `systemctl daemon-reload`                           |
| tasks/config.yml                           | new - runs some tdp specific adaptations and calls `configure.yml` (see bellow)              |
| tasks/configure.yml                        | adapted from community file : <br>- get rid of notifies<br>- use `prometheus_group` variable instead of hardcoded value  |
| tasks/config_set_web_config.yml            | new - set web_config in an idempotent way, to feed it to community tasks in `configure.yml`  |
| tasks/install.yml                          | complete rewrite to install from local tar.gz (air gap)                                      |
| tasks/preflight.yml                        | copied from community file                                                                   |
| templates/alert.rules.j2                   | copied from community file                                                                   |
| templates/prometheus.service.j2            | adapted from community : <br>- variable max_procs, user, group and server restart. <br>- no proxy option |
| templates/alert.rules.j2                   | copied from community file                                                                   |
| templates/file_sd.j2                       | new - file_sd targets for TDP components                                                     |

## Prometheus/alertmanager
Based on role alertmanager from [prometheus-community/ansible](https://github.com/prometheus-community/ansible.git) 0.7.0
List of common adaptations :
- get rid of notifies
- use `alertmanager_user` and `alertmanager_group` variables instead of hardcoded values

Specific adaptations
| file                                         | comments                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------- |
| tdp_vars_default/prometheus/alertmanager.yml | adapted from `default/main.yml` community file                                               |
| handlers/main.yml                            | completely changed. Only one handler for `systemctl daemon-reload`                           |
| tasks/config.yml                             | new - runs some tdp specific adaptations and calls `selinux.yml` and `configure.yml`         |
| tasks/selinux.yml                            | adapted from community file                                                                  |
| tasks/configure.yml                          | adapted from community file                                                                  |
| tasks/config_set_web_config.yml              | new - set web_config in an idempotent way, to feed it to community tasks in `configure.yml`  |
| tasks/install.yml                            | complete rewrite to install from local tar.gz (air gap)                                      |
| tasks/preflight.yml                          | copied from community file                                                                   |
| templates/alertmanager.yml.j2                | copied from community file                                                                   |
| templates/alertmanager.service.j2            | adapted from community file                                                                  |
| templates/amtool.j2                         | copied from community file                                                                   |

## Grafana/server
Based on role grafana from [cloudalchemy/ansible-grafana](https://github.com/cloudalchemy/ansible-grafana) last version (b77b256)
### List of adaptations :
- get rid of notifies
- use `grafana_group` and `grafana_user` variables instead of hardcoded value
- fix all ansible-lint issues

| file                                       | comments                                                                                     |
| ------------------------------------------ | -------------------------------------------------------------------------------------------- |
| tdp_vars_default/prometheus/prometheus.yml | adapted from `default/main.yml` community file                                               | 
| handlers/main.yml                          | completely changed. Only one handler for `systemctl daemon-reload`                           |
| tasks/config.yml                           | new - runs some tdp specific adaptations and calls `configure.yml` (see bellow)              |
| tasks/configure.yml                        | adapted from community file : removed `Grafana systemd unit' step (handled by install.yml)   |
| tasks/install.yml                          | complete rewrite to install from local tar.gz (air gap)                                      |
| tasks/preflight.yml                        | adapted from community file                                                                  |
| tasks/dashboards.yml                       | adapted from community file : Only keep 'provisioning' installation                          |
| tasks/datasources.yml                      | adapted from community file : Only keep 'provisioning' installation                          |
| tasks/notifications.yml                    | adapted from community file                                                                  |
| tasks/plugins.yml                          | adapted from community file                                                                  |
| templates/grafana.ini.j2                   | adapted from community file                                                                  |
| templates/ldap.toml.j2                     | adapted from community file                                                                  |
| templates/tmpfiles.j2                      | adapted from community file                                                                  |

**Note**: community role is licensed under an MIT License. Original license file has been copied at the root of the grafana/server role
