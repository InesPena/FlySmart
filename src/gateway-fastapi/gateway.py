from fastapi import FastAPI, Request, HTTPException
import httpx

app = FastAPI()

# Definir la URL del microservicio de vuelos
FLIGHTS_SERVICE_URL = "http://localhost:8000"
BOOKING_SERVICE_URL = "http://localhost:3000"

# Cliente HTTP asíncrono
client = httpx.AsyncClient()

@app.api_route("/flights/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def flights_service_proxy(path: str, request: Request):
    """Proxy inverso para el servicio de vuelos"""
    return await proxy_request(request, FLIGHTS_SERVICE_URL)

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user_service_proxy(path: str, request: Request):
    return await proxy_request(request, BOOKING_SERVICE_URL)

@app.api_route("/book/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user_service_proxy(path: str, request: Request):
    return await proxy_request(request, BOOKING_SERVICE_URL)

async def proxy_request(request: Request, service_url: str):
    """Reenvía la solicitud al microservicio correspondiente"""
    method = request.method
    url = f"{service_url}/{request.url.path}"
    headers = dict(request.headers)
    content = await request.body()

    try:
        response = await client.request(method, url, headers=headers, content=content)
        return response.content, response.status_code, response.headers.items()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gateway:app", host="0.0.0.0", port=8080, reload=True)
