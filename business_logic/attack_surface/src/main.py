from fastapi import FastAPI
import uvicorn
import requests
import json
import os
import sys


app = FastAPI()


class GoogleSearchAdapter():
    def __init__(self, url: str):
        self.base_url = url

    def get_subdomains(self, target: str) -> list:
        response = requests.get(f'{self.base_url}/subdomains?target={target}')
        if response.status_code != 200:
            print(f'Request to "{self.base_url}" failed', file=sys.stderr)
            return list()
        return response.json()

class CrtShAdapter():
    def __init__(self, url: str):
        self.base_url = url

    def get_subdomains(self, target: str) -> list:
        response = requests.get(f'{self.base_url}/subdomains?target={target}')
        if response.status_code != 200:
            print(f'Request to "{self.base_url}" failed', file=sys.stderr)
            return list()
        return response.json()

class DnsAdapter():
    def __init__(self, url: str):
        self.base_url = url

    def resolve(self, domains: list) -> list:
        response = requests.post(f'{self.base_url}/resolve', json=domains)
        if response.status_code != 200:
            print(f'Request to "{self.base_url}" failed', file=sys.stderr)
            return list()
        return response.json()

class IPinfoAdapter():
    def __init__(self, url: str):
        self.base_url = url

    def info(self, ips: list) -> list:
        response = requests.post(f'{self.base_url}/info', json=ips)
        if response.status_code != 200:
            print(f'Request to "{self.base_url}" failed', file=sys.stderr)
            return list()
        return response.json()


@app.get('/')
async def scan(target: str):
    '''
    Find subdomains and assets of a given domain
    '''
    domains = [target]

    # Adapters
    google_adapter = GoogleSearchAdapter(url=os.environ.get(f'GOOGLE_SEARCH_ADAPTER'))
    crt_sh_adapter = CrtShAdapter(url=os.environ.get(f'CRT_SH_ADAPTER'))
    dns_adapter = DnsAdapter(url=os.environ.get(f'DNS_ADAPTER'))
    ipinfo_adapter = IPinfoAdapter(url=os.environ.get(f'IPINFO_ADAPTER'))

    google_domains = google_adapter.get_subdomains(target)
    crt_sh_domains = crt_sh_adapter.get_subdomains(target)

    # Remove duplicates
    domains = sorted(set(domains + google_domains + crt_sh_domains))

    # Call DNS adapter
    resolved_domains = dns_adapter.resolve(domains)

    # Extract ips
    all_ips = set()
    for domain in resolved_domains:
        ips = domain['ips']
        all_ips.update(ips)
    ips = list(all_ips)

    # Call ipinfo adapter
    ips_info = ipinfo_adapter.info(ips)

    return {
        'domains': resolved_domains,
        'ips': ips_info
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=3000))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
