from fastapi import FastAPI
import uvicorn
import urllib.request
import json
import os


app = FastAPI()


@app.get('/')
async def get_subdomains(target: str):
    '''
    Retrieve the list of subdomains of "target" from crt.sh and return them
    as a json list
    '''

    protocol = os.environ.get('CRT_SH_PROTO', default='https')
    domain = os.environ.get('CRT_SH_HOST', default='crt.sh')
    port = os.environ.get('CRT_SH_PORT', default='crt.sh')
    response = urllib.request.urlopen(f'{protocol}://{domain}:{port}/?q={target}&output=json')

    if 'application/json' not in response.headers['content-type']:
        return { 'success': False, 'message': 'Failed to retrieve data' }

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

    return { 'success': True, 'subdomains': list(true_subdomains) }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=3000))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
