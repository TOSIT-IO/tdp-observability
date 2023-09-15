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

