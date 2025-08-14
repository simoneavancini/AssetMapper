from fastapi import Request, FastAPI, HTTPException
import uvicorn
import sys
import os
import ipinfo


app = FastAPI()
access_token = os.environ.get('API_KEY')
handler = ipinfo.getHandler(access_token)


@app.post('/info')
async def ip_info(request: Request):
    '''
    Return info about the target IP
    '''

    ips = await request.json()
    if type(ips) is not list:
        raise HTTPException(status_code=400, detail='List of ips expected in the request body')

    ips_info = list()
    for ip in ips:
        try:
            details = handler.getDetails(ip)
            ips_info.append({
                'ip': ip,
                'org': details.details.get('org'),
                'loc': details.details.get('loc')
            })
        except Exception as e:
            print(e, file=sys.stderr)
            ips_info.append({
                'ip': ip
            })

    return ips_info


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=80))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
