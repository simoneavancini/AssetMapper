from fastapi import FastAPI, Depends, HTTPException, Header
import uvicorn
import requests
import jwt
from jwt import InvalidTokenError
from typing import Optional
import os

SCAN_DB_ADAPTER = os.environ.get("SCAN_DB_ADAPTER")
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = "HS256"

app = FastAPI()

# JWT Authorization
def verify_jwt(authorization: Optional[str] = Header(None)):
    """
    Verifies JWT from Authorization header
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid JWT: {str(e)}")

# Endpoints
@app.post("/scans")
def store_object(obj: dict, payload=Depends(verify_jwt)):
    """
    Store a JSON object in the DB adapter
    """
    try:
        response = requests.post(f"{SCAN_DB_ADAPTER}/scans", json=obj)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"DB adapter error: {str(e)}")


@app.get("/scans/{obj_id}")
def get_object(obj_id: str, payload=Depends(verify_jwt)):
    """
    Retrieve a JSON object by ID
    """
    try:
        response = requests.get(f"{SCAN_DB_ADAPTER}/scans/{obj_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"DB adapter error: {str(e)}")


@app.get("/scans")
def list_objects(payload=Depends(verify_jwt)):
    """
    List all objects from DB adapter
    """
    try:
        response = requests.get(f"{SCAN_DB_ADAPTER}/scans")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"DB adapter error: {str(e)}")


@app.delete("/scans/{obj_id}")
def delete_object(obj_id: str, payload=Depends(verify_jwt)):
    """
    Delete a JSON object by ID
    """
    try:
        response = requests.delete(f"{SCAN_DB_ADAPTER}/scans/{obj_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Object not found")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"DB adapter error: {str(e)}")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', default=80))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
