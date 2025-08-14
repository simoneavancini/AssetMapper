from fastapi import Request, FastAPI, HTTPException
import uvicorn
import os
import dns.resolver


resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4'] # Google Public DNS


app = FastAPI()


@app.post('/resolve')
async def resolve_domains(request: Request):
    '''
    Resolve the input domains and return their IP addresses
    '''

    domains = await request.json()
    if type(domains) is not list:
        raise HTTPException(status_code=400, detail='List of domains expected in the request body')

    resolved_domains = list()
    for domain in domains:
        try:
            answers = resolver.resolve(domain, 'A')
            addresses = [rdata.address for rdata in answers]
            resolved_domains.append({
                'domain': domain,
                'ips': addresses
            })
        except dns.resolver.NXDOMAIN:
            resolved_domains.append({
                'domain': domain,
                'ips': []
            })
        except Exception as e:
            print(f"An error occurred: {e}")
            resolved_domains.append({
                'domain': domain,
                'ips': []
            })

    return resolved_domains


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=80))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
