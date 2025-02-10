from fastapi import FastAPI
import uvicorn
import urllib.request
import json
import os
import sys
from services import *


app = FastAPI()


@app.get('/')
async def scan(target: str):
    '''
    Find subdomains and assets of a given domain
    '''
    domains = [target]

    # Call search adapter
    google_domains = google_search_adapter(target)

    # Call crt.sh adapter
    crt_sh_domains = crt_sh_adapter(target)

    # Remove duplicates
    domains = sorted(set(domains + google_domains + crt_sh_domains))

    # Call DNS adapter
    resolved_domains = dns_adapter(domains)

    # Extract ips
    all_ips = set()
    for domain in resolved_domains:
        ips = domain['ips']
        all_ips.update(ips)
    ips = list(all_ips)

    # Call ipinfo adapter
    ips_info = ipinfo_adapter(ips)

    return { 'success': True, 'attack_surface': {
        'domains': resolved_domains,
        'ips': ips_info
    }}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=3000))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
