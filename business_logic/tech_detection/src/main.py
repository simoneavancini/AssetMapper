from fastapi import FastAPI, Request
import uvicorn
import requests
import json
import os
import sys


app = FastAPI()


class BuiltwithAdapter():
    def __init__(self, url: str):
        self.base_url = url

    def get_tech(self, target: str) -> dict:
        response = requests.get(f'{self.base_url}/tech?target={target}')
        if response.status_code != 200:
            print(f'Request to "{self.base_url}" failed', file=sys.stderr)
            return {}
        return response.json()


@app.get('/')
async def scan(target: str):
    '''
    Return technologies detected in the provided domains
    '''

    # Adapters
    builtwith_adapter = BuiltwithAdapter(url=os.environ.get(f'BUILTWITH_ADAPTER'))

    detected = builtwith_adapter.get_tech(target)

    return detected


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=3000))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
