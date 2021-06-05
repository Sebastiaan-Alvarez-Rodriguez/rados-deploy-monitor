import argparse
import json
import os

import prometheus_grafana_deploy.internal.defaults.start as start_defaults
from prometheus_grafana_deploy.internal.util.printer import *


def basics():
    '''Basic top-level settings for our dashboard.'''
        # 'annotations': {'list': [{'builtIn': 1, 'datasource': 'skyhook', 'enable': True, 'hide': True, 'iconColor': 'rgba(0, 211, 255, 1)', 'name': 'Annotations & Alerts', 'type': 'dashboard'}]},
    return {
        'description': 'Dashboard showing CPU, Disk, and Network utilization of SkyhookDM',
        'editable': True,
        'gnetId': None,
        'graphTooltip': 0,
        'id': 1,
        'iteration': 1619523594477,
        'links': [],
        'panels': [],
        "refresh": "30s",
        "schemaVersion": 27,
        "style": "dark",
        "tags": [],
        "templating": {
            "list": [
              {
                "description": "Hostname of the client node",
                "error": None,
                "hide": 2,
                "label": "Client node",
                "name": "client",
                "query": "ms1243.utah.cloudlab.us",
                "skipUrlSync": False,
                "type": "constant"
              }
            ]
        },
        "time": {"from": "now-30m", "to": "now"},
        "timepicker": {"refresh_intervals": ["5s", "10s", "15s", "30s", "1m", "5m", "15m", "30m", "1h", "2h", "1d"]},
        "timezone": "",
        "title": "SkyhookDM-Arrow",
        "uid": "lxKiCIXMk",
        "version": 15
    }


def _dict_append(d0, d1):
    '''Appends dict `d1` to `d0`'''
    d0.update(d1)


def _panel_axes():
    '''Returns standard panel axis information for both x- and y-axes.'''
    return {
        "xaxis": {"buckets": None, "mode": "time", "name": None, "show": True, "values": []},
        "yaxes": [
          {"$$hashKey": "object:104", "format": "short", "label": None, "logBase": 1, "max": "100", "min": "0", "show": True},
          {"$$hashKey": "object:105", "format": "short", "label": None, "logBase": 1, "max": None, "min": None, "show": True}
        ],
        "yaxis": {"align": False, "alignLevel": None}
    }

def _panel_legend():
    '''Returns standard panel legend information.'''
    return {"legend": {"avg": False, "current": False, "max": False, "min": False, "show": False, "total": False, "values": False}}

def _panel_lines():
    '''Returns standard panel line configuration.'''
    return {"lines": True, "linewidth": 1, "spaceLength": 10, "steppedLine": False,}

def _panel_misc():
    '''Returns standard panel misc configurations.'''
    return {
        "hiddenSeries": False,
        "nullPointMode": "null",
        "options": {"alertThreshold": True},
        "percentage": False,
        "pluginVersion": "7.5.4",
        "pointradius": 2,
        "points": False,
        "renderer": "flot",
        "seriesOverrides": [],
        "stack": True,
        "thresholds": [],
        "type": "graph"}

def _panel_style():
    '''Returns standard panel style.'''
    return {"aliasColors": {}, "bars": False, "dashLength": 10, "dashes": False, "datasource": None, "fieldConfig": {"defaults": {}, "overrides": []}, "fill": 1, "fillGradient": 0}

def _panel_time():
    '''Returns standard panel time configuration.'''
    return {"timeFrom": None, "timeRegions": [], "timeShift": None,}


def _panel_tooltip():
    '''Returns standard panel tooltip.'''
    return {"tooltip": {"shared": True, "sort": 0, "value_type": "individual"}}


def generate_panel_ceph_cpu(config, ceph_nodes, prometheus_port):
    '''Generates a panel displaying CPU utilization in Ceph.'''
    panel_config = {'id': 10, "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}}
    _dict_append(panel_config, _panel_axes())
    _dict_append(panel_config, _panel_legend())
    _dict_append(panel_config, _panel_lines())
    _dict_append(panel_config, _panel_misc())
    _dict_append(panel_config, _panel_style())
    _dict_append(panel_config, _panel_time())
    _dict_append(panel_config, _panel_tooltip())

    hostlist = ['{}:{}'.format(x.ip_public, prometheus_port) for x in ceph_nodes]
    or_expr = '|'.join(host for host in hostlist)
    _dict_append(panel_config, {
        "targets": [
          {
            "exemplar": True,
            "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{{job=\"node\",mode=\"idle\",instance=~\"{}\"}}[1m])) * 100)".format(or_expr),
            "interval": "",
            "legendFormat": "",
            "refId": "Average"
          }
        ],
        "title": "Ceph CPU Usage (%)"
    })
    config['panels'].append(panel_config)


def generate_panel_ceph_storage(config, ceph_nodes, prometheus_port):
    '''Generates a panel displaying Ceph Storage I/O utilization.'''
    panel_config = {'id': 8, "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}}
    _dict_append(panel_config, _panel_axes())
    _dict_append(panel_config, _panel_legend())
    _dict_append(panel_config, _panel_lines())
    _dict_append(panel_config, _panel_misc())
    _dict_append(panel_config, _panel_style())
    _dict_append(panel_config, _panel_time())
    _dict_append(panel_config, _panel_tooltip())

    hostlist = ['{}:{}'.format(x.ip_public, prometheus_port) for x in ceph_nodes]
    or_expr = '|'.join(host for host in hostlist)
    _dict_append(panel_config, {
        "targets": [
          {
            "exemplar": True,
            "expr": "rate(node_disk_read_bytes_total{{device=\"nvme0n1\", instance=~\"{}\"}}[5m])".format(or_expr),
            "interval": "",
            "legendFormat": "",
            "refId": "A"
          }
        ],
        "title": "Storage Disk I/O"
    })
    config['panels'].append(panel_config)


def generate_panel_client_cpu(config, client_nodes, prometheus_port):
    '''Generates a panel displaying Client CPU utilization.'''
    panel_config = {'id': 2, 'gridPos': {'h': 8, 'w': 12, 'x': 0, 'y': 0}}
    _dict_append(panel_config, _panel_axes())
    _dict_append(panel_config, _panel_legend())
    _dict_append(panel_config, _panel_lines())
    _dict_append(panel_config, _panel_misc())
    _dict_append(panel_config, _panel_style())
    _dict_append(panel_config, _panel_time())
    _dict_append(panel_config, _panel_tooltip())

    hostlist = ['{}:{}'.format(x.ip_public, prometheus_port) for x in client_nodes]
    or_expr = '|'.join(host for host in hostlist)
    _dict_append(panel_config, {
        'targets': [
          {
            'exemplar': True,
            'expr': '100 - (avg by (instance) (rate(node_cpu_seconds_total{{job=\"node\",mode=\"idle\",instance=~\"{}\"}}[1m])) * 100)'.format(or_expr),
            'interval': '',
            'legendFormat': '',
            'refId': 'avg'
          }
        ],
        'title': 'Client CPU Usage (%)'
    })
    config['panels'].append(panel_config)


def generate_panel_client_network(config, client_nodes, prometheus_port):
    '''Generates a panel displaying Client network I/O utilization.'''
    panel_config = {'id': 6, 'gridPos': {'h': 8, 'w': 12, 'x': 12, 'y': 8}}
    _dict_append(panel_config, _panel_axes())
    _dict_append(panel_config, _panel_legend())
    _dict_append(panel_config, _panel_lines())
    _dict_append(panel_config, _panel_misc())
    _dict_append(panel_config, _panel_style())
    _dict_append(panel_config, _panel_time())
    _dict_append(panel_config, _panel_tooltip())

    hostlist = ['{}:{}'.format(x.ip_public, prometheus_port) for x in client_nodes]
    or_expr = '|'.join(host for host in hostlist)
    _dict_append(panel_config, {
        "targets": [
          {
            "exemplar": True,
            "expr": "rate(node_network_receive_bytes_total{{device=\"eno1d1\",instance=~\"{}\"}}[5m])".format(or_expr),
            "interval": "",
            "legendFormat": "",
            "refId": "A"
          }
        ],
        "title": "Client Network I/O"
    })
    config['panels'].append(panel_config)


def parse(args):
    parser = argparse.ArgumentParser(prog='...')
    # We have no extra arguments to add here.
    parser.add_argument('--prometheus-port', metavar='number', dest='prometheus_port', type=int, default=start_defaults.prometheus_port(), help='Port to use for Prometheus.')
    args = parser.parse_args(args)
    return True, [], {'prometheus_port': args.prometheus_port}




def generate(reservation, outputloc, *args, **kwargs):
    prometheus_port = kwargs.get('prometheus_port') or start_defaults.prometheus_port()

    config = basics()

    client_nodes = [x for x in reservation.nodes if not 'designations' in x.extra_info]
    ceph_nodes = [x for x in reservation.nodes if 'designations' in x.extra_info]

    generate_panel_ceph_cpu(config, ceph_nodes, prometheus_port)
    generate_panel_ceph_storage(config, ceph_nodes, prometheus_port)
    generate_panel_client_cpu(config, client_nodes, prometheus_port)
    generate_panel_client_network(config, client_nodes, prometheus_port)

    if os.path.isdir(outputloc):
        outputloc = os.path.join(outputloc, 'spark_rados.json')

    if os.path.isfile(outputloc):
        printw('File already exists, overriding: {}'.format(outputloc))

    with open(outputloc, 'w') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    return True