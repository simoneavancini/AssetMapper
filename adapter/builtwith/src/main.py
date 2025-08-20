from fastapi import FastAPI, HTTPException
import uvicorn
import os
import requests


app = FastAPI()


@app.get('/tech')
async def get_subdomains(target: str):
    '''
    Retrieve technologies used by the target domain
    '''

    key = os.environ.get('API_KEY')

    response = requests.get('https://api.builtwith.com/free1/api.json', params={'KEY': key, 'LOOKUP': target})

    if response.status_code != 200 or 'application/json' not in response.headers.get('content-type', ''):
        raise HTTPException(status_code=500, detail='Failed to retrieve data')

    data = response.json()

    # Build a short summary: group name + live technologies count
    summary = {group.get('name'): group.get('live', 0) for group in data.get('groups', [])}

    return {'domain': data.get('domain'), 'technologies': summary}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=80))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
