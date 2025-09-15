# Copyright 2022 TOSIT.IO
# SPDX-License-Identifier: Apache-2.0
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    module: tosit.tdp_observability.observability_data
    short_description: Extract data from 'observability_tdp_targets' variable in various forms
    description:
      - This lookup plugin parses the C(observability_tdp_targets) variable ans returns various data
    options:
      _terms:
        description:
          - The type of information wanted.
        choices:
          - installed_services
          - prometheus_jobs
          - alloy_unix_groups
          - alloy_jobs
        type: string
        required: yes
"""

EXAMPLES = """
- name: find all services used in this cluster
  ansible.builtin.set_fact:
    services: "{{ lookup('tosit.tdp_observability.observability_data','installed_services', wantlist = True) }}"

- name: Print all prometheus job ports
  ansible.builtin.debug:
    msg: "'{{ job.job_name }}' port is {{ job.port_num }}"
  loop: "{{ lookup('tosit.tdp_observability.observability_data','prometheus') }}"
  loop_control:
    loop_var: job
    label: "{{ job.job_name }}"
"""

RETURN = """
  _raw:
    description:
      - Depends on option used.
    type: list
"""

from typing import Dict, List, Any
from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError
from ansible_collections.tosit.tdp.plugins.module_utils.access_fqdn import access_fqdn

reserved_kw = [ 'labels', 'unix_group' ]
allowed_targets = [ 'prometheus_jobs', 'alloy_jobs', 'installed_services', 'alloy_unix_groups']

class LookupModule(LookupBase):

    def get_labels(self, service, component, job, additional_labels) :
        """
        builds labels dictionnary from various label sources
        """
        common_labels    = self.vars['observability_common_labels']
        service_labels   = service.get('labels', {})
        component_labels = component.get('labels', {})
        job_labels       = job.get('labels', {})

        return common_labels | service_labels | component_labels | job_labels | additional_labels

    def check_uniqueness(self, job_name):
        """
        Checks for uniqueness of job_name
        """
        if job_name in self.all_jobs :
            raise AnsibleError(f"Duplicate job : {job_name}")
        self.all_jobs.append(job_name)

    def alloy_unix_group(self, service, service_name, component_name): # pylint: disable=unused-arguments
        """
        returns the 'unix_group' defined at component or service level if
        <service_component> has alloy jobs configured, else returns None
        """
        component_has_alloy_jobs = False
        for job in service[component_name]['jobs']:
            if job.get('enabled', True) and job.get('log_file') is not None:
                component_has_alloy_jobs = True
                break
        if component_has_alloy_jobs:
            unix_group = service[component_name].get('unix_group', service.get('unix_group'))
            if unix_group is None:
                msg = "{service_name}_{component_name} does not have a unix_group defined."
                raise AnsibleError(msg)
            return unix_group
        return None

    def alloy_job(self, job_name, job):
        """
        Builds data associated with a log file to be scraped by grafana alloy
        """
        log_file = job.get('log_file', None)
        if job.get('enabled', True) and log_file is not None:
            job_data = {}
            pipeline = job.get('alloy_pipeline', 'default')
            if isinstance(pipeline, str):
                job_data['pipeline'] = pipeline
            else:
                job_data['custom_pipeline'] = job['alloy_pipeline']
                job_data['pipeline'] = job_name
            job_data['labels'] = {
                'instance': self.vars['inventory_hostname'],
                '__path__': log_file,
            }
        else:
            job_data = None
        return job_data

    def prometheus_job(self, job, group_name):
        """
        Builds data associated with a prometheus job
        """
        prom_port = int(job.get('exporter_port', 0))
        if job.get('enabled', True) and prom_port > 0:
            job_data = {}
            job_data['port_num'] = prom_port
            host_list=[]
            for host in self.vars['groups'][group_name]:
                host_list.append(access_fqdn(host, self.vars['hostvars']))
            job_data['host_list'] = host_list
            job_data['scrape_options'] = job.get('prometheus_scrape_options', {})
        else:
            job_data = None
        return job_data

    def build_response(self, service, service_name, component_name):
        """
        build response item for this service/component
        """
        component = service[component_name]
        group_name = component.get('group', f"{service_name}_{component_name}")
        # skip groups that are not in topology
        if group_name not in self.vars['groups']:
            return None
        # all components should have jobs
        if 'jobs' not in component:
            raise AnsibleError(f"No jobs for : {service_name}_{component_name}")
        #
        # For "installed_services" target we just want active services names
        #
        if self.target == 'installed_services':
            return service_name
        #
        # For "alloy_unix_groups" target we want the unix_group key
        # for service with alloy jobs that are installed on current host
        #
        if self.target == 'alloy_unix_groups':
            if group_name in self.vars['group_names']:
                return self.alloy_unix_group(service, service_name, component_name)
            return None
        #
        # For other targets, build a list of jobs, with associated job data
        #
        job_list = []
        for job in component['jobs']:
            job_name = f"{service_name}_{component_name}"
            if 'name_suffix' in job:
                job_name = f"{job_name}_{job['name_suffix']}"
            job_data = None
            #
            # get job_data for specific targets.
            #
            if self.target == 'prometheus_jobs':
                # prometheus_jobs are all configured on prometheus host.
                # Do not filter on local groups : we want data for all clients
                job_data = self.prometheus_job(job, group_name)
            elif self.target == 'alloy_jobs':
                # alloy_jobs are configured on each client, return only
                # data if group_name is in current host groups
                if group_name in self.vars['group_names']:
                    job_data = self.alloy_job(job_name, job)
                else:
                    job_data = None
            if job_data is not None:
                self.check_uniqueness(job_name)
                # complete with common data and append to list
                job_data['job_name'] = job_name
                topo_labels = {
                    'service': service_name,
                    'component' : component_name,
                }
                standard_labels = self.get_labels(service, component, job, topo_labels)
                job_data['labels'] = job_data.get('labels', {}) | standard_labels
                job_list.append(job_data)
        return job_list

    def __init__(self, **kwargs):
        super().__init__()
        self.vars     : Dict[str, Any] = {}
        self.target   : str = ''
        self.all_jobs : List[str] = []

    def run(self, terms, variables, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        self.vars = variables['vars']
        self.target = terms[0]

        if self.target not in allowed_targets:
            raise AnsibleError(f"Unknown target : {self.target} (allowed targets are {','.join(allowed_targets)})"  )
        resp = []
        for service_name, service in variables['vars']['observability_tdp_targets'].items():
            for component_name in list(set(service.keys()) - set(reserved_kw)):
                item = self.build_response(service, service_name, component_name)
                if item is None:
                    continue
                if isinstance(item, str) and item not in resp:
                    resp.append(item)
                elif isinstance(item, list):
                    resp.extend(item)
        # to ensure idempotence, allways return results in the same order
        if self.target in ['prometheus_jobs', 'alloy_jobs']:
            resp = sorted(resp, key=lambda d: d['job_name'])
        else:
            resp.sort()
        return resp
