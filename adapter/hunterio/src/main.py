from fastapi import FastAPI, HTTPException
import uvicorn
import os
import requests


app = FastAPI()


@app.get("/emails")
async def get_emails(domain: str):
    """
    Retrieve emails found for a domain using Hunter.io
    """

    api_key = os.environ.get("API_KEY")
    if api_key is None:
        raise HTTPException(status_code=500, detail="API key is not configured")

    url = "https://api.hunter.io/v2/domain-search"

    response = requests.get(url, params={"domain": domain, "api_key": api_key})

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to retrieve data")

    data = response.json()

    # Transform response into a short, simple summary
    emails = data.get("data", {}).get("emails", [])

    emails_info = []
    for e in emails:
        emails_info.append({
            "value": e.get("value"),
            "position": e.get("position")
        })

    return emails_info


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=80))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
