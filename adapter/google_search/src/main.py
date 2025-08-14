from fastapi import FastAPI, HTTPException
import uvicorn
from googlesearch import search
import os
import re
import requests


app = FastAPI()


@app.get('/subdomains')
async def get_subdomains(target: str):
    '''
    Retrieve the list of subdomains of "target" using Google search and return them
    as a json list
    '''

    query = f"site:{target}"
    subdomains = set()

    # Perform Google search
    try:
        for url in search(query, num_results=100):
            # Extract subdomains using regex
            subdomain_match = re.search(r'(https?://)?([a-zA-Z0-9-]+\.)*' + re.escape(target), url)
            if subdomain_match:
                subdomain = subdomain_match.group(2)
                if subdomain:
                    subdomains.add(subdomain + target)
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=500, detail='HTTP Exception')

    return list(subdomains)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=80))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
