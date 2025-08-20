from fastapi import FastAPI, Request
import uvicorn
import requests
import json
import os
import sys


app = FastAPI()


class HunterioAdapter():
    def __init__(self, url: str):
        self.base_url = url

    def get_emails(self, target: str) -> list:
        response = requests.get(f'{self.base_url}/emails?domain={target}')
        if response.status_code != 200:
            print(f'Request to "{self.base_url}" failed', file=sys.stderr)
            return []
        return response.json()

# Adapters
hunterio_adapter = HunterioAdapter(url=os.environ.get(f'HUNTERIO_ADAPTER'))


@app.get('/')
async def scan(domain: str):
    '''
    Retrieve public emails for a domain
    '''

    emails_data = hunterio_adapter.get_emails(domain)

    # Filtering
    emails = []
    for e in emails_data:
        if e.get("confidence", 0) >= 80:
            emails.append({
                "value": e.get("value"),
                "position": e.get("position")
            })

    return {
        "domain": domain,
        "emails": emails
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=3000))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
