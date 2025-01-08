from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import httpx
import os

FLIGHTS_SERVICE_URL = os.getenv("FLIGHTS_SERVICE_URL", "http://localhost:8000")
BOOKING_SERVICE_URL = os.getenv("BOOKING_SERVICE_URL", "http://localhost:3000")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Configura las plantillas Jinja2 para que busquen en el directorio 'templates'
templates = Jinja2Templates(directory="templates")

# Configura los archivos estáticos para que se sirvan desde el directorio 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta por defecto
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# HTTPX client for external requests
client = httpx.AsyncClient()

# Flights Service
@app.get("/flights", response_class=HTMLResponse)
async def get_flights(request: Request, origin: str, destination: str, departure_date: str, return_date: str):
    try:
        outbound_response = await client.get(
            f"{FLIGHTS_SERVICE_URL}/flights",
            params={
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
            },
        )
        outbound_flights = outbound_response.json() if outbound_response.status_code == 200 else []

        return_flights = []
        if return_date:
            return_response = await client.get(
                f"{FLIGHTS_SERVICE_URL}/flights",
                params={
                    "origin": destination,
                    "destination": origin,
                    "departure_date": return_date,
                },
            )
        return_flights = return_response.json() if return_response.status_code == 200 else []

        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "outbound_flights": outbound_flights,
                "return_flights": return_flights,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Booking Service
@app.post("/register")
async def register_user(request: Request):
    try:
        payload = await request.json()
        response = await client.post(f"{BOOKING_SERVICE_URL}/auth/register", json=payload)

        if response.status_code == 201:
            return {"message": "User registered successfully"}
        return {"error": response.text}, response.status_code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/login")
async def login_user(request: Request, username: str, password: str):
    try:
        response = await client.get(
            f"{BOOKING_SERVICE_URL}/auth/login",
            params={"username": username, "password": password}
        )

        if response.status_code == 200:
            return response.json()  
        return {"error": response.text}, response.status_code 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bookflight")
async def book_flight(request: Request):
    try:
        payload = await request.json()
        response = await client.post(f"{BOOKING_SERVICE_URL}/book/bookflight", json=payload)

        if response.status_code == 201:
            return {"message": "User registered successfully"}
        return {"error": response.text}, response.status_code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/retrievebookings")
async def login_user(request: Request, email:str):
    try:
        response = await client.get(
            f"{BOOKING_SERVICE_URL}/book/retrievebookings",
            params={"email": email}
        )

        if response.status_code == 200:
            reservations = response.json() 
            return templates.TemplateResponse("bookings.html", {"request": request, "bookings": reservations})
        else:
            return {"error": response.text}, response.status_code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
