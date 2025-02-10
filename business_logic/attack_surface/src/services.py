import os
import sys
import urllib.request
import json


def google_search_adapter(target: str) -> list():
    # Get host and port from environment variables
    host = os.environ.get(f'GOOGLE_SEARCH_ADAPTER_HOST')
    port = os.environ.get(f'GOOGLE_SEARCH_ADAPTER_PORT')
    if host is None:
        print(f'GOOGLE_SEARCH_ADAPTER_HOST not defined', file=sys.stderr)
        return list()
    if port is None:
        print(f'GOOGLE_SEARCH_ADAPTER_PORT not defined', file=sys.stderr)
        return list()

    # Request to the adapter service
    response = urllib.request.urlopen(f'http://{host}:{port}/?target={target}')
    data = json.loads(response.read())

    if data['success']:
        return data['subdomains']
    return []


def crt_sh_adapter(target: str) -> list():
    # Get host and port from environment variables
    host = os.environ.get(f'CRT_SH_ADAPTER_HOST')
    port = os.environ.get(f'CRT_SH_ADAPTER_PORT')
    if host is None:
        print(f'CRT_SH_ADAPTER_HOST not defined', file=sys.stderr)
        return list()
    if port is None:
        print(f'CRT_SH_ADAPTER_PORT not defined', file=sys.stderr)
        return list()

    # Request to the adapter service
    response = urllib.request.urlopen(f'http://{host}:{port}/?target={target}')
    data = json.loads(response.read())

    if data['success']:
        return data['subdomains']
    return []


def dns_adapter(target: list) -> list():
    # Get host and port from environment variables
    host = os.environ.get(f'DNS_ADAPTER_HOST')
    port = os.environ.get(f'DNS_ADAPTER_PORT')
    if host is None:
        print(f'CRT_SH_ADAPTER_HOST not defined', file=sys.stderr)
        return list()
    if port is None:
        print(f'CRT_SH_ADAPTER_PORT not defined', file=sys.stderr)
        return list()

    # Request to the adapter service
    headers = {'Content-Type':'application/json'}
    bindata = json.dumps(target).encode('utf-8')
    req = urllib.request.Request(f'http://{host}:{port}/', bindata, headers)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())

    if data['success']:
        return data['domains']
    return []


def ipinfo_adapter(target: list) -> list():
    # Get host and port from environment variables
    host = os.environ.get(f'IPINFO_ADAPTER_HOST')
    port = os.environ.get(f'IPINFO_ADAPTER_PORT')
    if host is None:
        print(f'IPINFO_ADAPTER_HOST not defined', file=sys.stderr)
        return list()
    if port is None:
        print(f'IPINFO_ADAPTER_PORT not defined', file=sys.stderr)
        return list()

    # Request to the adapter service
    headers = {'Content-Type':'application/json'}
    bindata = json.dumps(target).encode('utf-8')
    req = urllib.request.Request(f'http://{host}:{port}/', bindata, headers)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())

    if data['success']:
        return data['data']
    return []
