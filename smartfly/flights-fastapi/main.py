from fastapi import FastAPI, HTTPException
from typing import List
from amadeusClient import get_access_token, fetch_flights
from models import FlightOffer

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/flights", response_model=List[FlightOffer])
async def get_flights(origin: str, destination: str, departure_date: str):
    try:
        token = await get_access_token()
        flights = await fetch_flights(origin, destination, departure_date, token)
        return flights
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


