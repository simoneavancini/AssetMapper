from fastapi import Request, FastAPI
import uvicorn
import sys
import os
import ipinfo


app = FastAPI()
access_token = os.environ.get('API_KEY')
handler = ipinfo.getHandler(access_token)


@app.post('/')
async def ip_info(request: Request):
    '''
    Return info about the target IP
    '''
    ips = await request.json()
    if type(ips) is not list:
        return { 'success': False, 'message': 'list of ips expected in the request body' }

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

    return { 'success': True, 'data': ips_info }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=3000))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
