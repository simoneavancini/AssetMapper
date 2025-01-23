from fastapi import FastAPI
import uvicorn
import urllib.request
import json


app = FastAPI()


@app.get("/")
async def get_subdomains(target: str):
    """Local API that lists all of the available song from the folder"""

    response = urllib.request.urlopen(f"https://crt.sh/?q={target}&output=json")

    if 'application/json' not in response.headers['content-type']:
        return { 'success': False, 'message': 'Failed to retrieve data' }

    # Parse response
    data = json.loads(response.decode('utf-8'))
    subdomains = set()

    for item in data:
        name_value = item['name_value'].replace('*.', '')
        common_name = item['common_name'].replace('*.', '')
        subdomains.update(name_value.splitlines())
        subdomains.update(common_name.splitlines())

    return { 'success': True, 'subdomains': list(subdomains) }


if __name__ == "__main__":
    uvicorn.run("main:app", port=3002, log_level="info")
