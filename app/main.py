import asyncio
from typing import Dict, List
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

service_one_url = "http://upstream_service_one_python:8080/info"
service_two_url = "http://upstream_service_two_python:8080/info"

http_client = httpx.AsyncClient(
    timeout=5.0,
    limits=httpx.Limits(max_connections=2000, max_keepalive_connections=10),
)


class InfoResponse(BaseModel):
    random_string: str


async def fetch_info(url: str) -> InfoResponse:
    try:
        response = await http_client.get(url)
        response.raise_for_status()
        return InfoResponse(**response.json())
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.get("/{name}", response_model=Dict[str, List | str])
async def hello(name: str) -> Dict[str, List | str]:
    results = await asyncio.gather(fetch_info(service_one_url), fetch_info(service_two_url))
    return {"hello": name, "result": results}


if __name__ == "__main__":
    uvicorn.run("main:app", workers=20, host="0.0.0.0", port=8123, log_level="error")
