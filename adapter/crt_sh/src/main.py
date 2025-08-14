from fastapi import FastAPI
import uvicorn
import urllib.request
import json
import os


app = FastAPI()


@app.get('/subdomains')
async def get_subdomains(target: str, test: bool):
    '''
    Retrieve the list of subdomains of "target" from crt.sh and return them
    as a json list
    '''

    # Sometime crt.sh can be very slow, so this can be use to test this srvice
    if test:
        return ['subdomain.example.com', 'blog.example.com']

    response = urllib.request.urlopen(f'https://crt.sh/?q={target}&output=json')

    if 'application/json' not in response.headers['content-type']:
        raise HTTPException(status_code=500, detail='Failed to retrieve data')

    # Parse response
    data = json.loads(response.read())
    subdomains = set()

    for item in data:
        name_value = item['name_value'].replace('*.', '')
        common_name = item['common_name'].replace('*.', '')
        subdomains.update(name_value.splitlines())
        subdomains.update(common_name.splitlines())

    # Check that the subdomains are of the right target
    true_subdomains = [sub for sub in subdomains if sub.endswith('.' + target) or sub == target]

    return list(true_subdomains)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=80))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
