from fastapi import FastAPI
import uvicorn
import json
import os


app = FastAPI()


@app.get('/')
async def scan():
    '''
    Simulate the crt.sh service
    '''
    with open('./src/crt_sh.txt', 'r') as f:
        data = json.loads(f.read())

    return data


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=3000))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')

