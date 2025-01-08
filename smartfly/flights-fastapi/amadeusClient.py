import httpx
from fastapi import HTTPException
from typing import List
from models import FlightSegment, FlightOffer

# Configuración de credenciales y URLs
API_TEST_KEY = "jvBSSGUWm7mf1v1NcOA04DAfqfQ66CSK"
API_TEST_SECRET = "WTATPJCONQACxNVx"
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHTS_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

# Obtener el token de acceso desde Amadeus
async def get_access_token() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": API_TEST_KEY,
                "client_secret": API_TEST_SECRET,
            },
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener el token")
        return response.json()["access_token"]

# Obtener vuelos desde Amadeus API
async def fetch_flights(origin: str, destination: str, departure_date: str, token: str) -> List[FlightOffer]:
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": 1,
    }
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(FLIGHTS_URL, params=params, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        data = response.json()
        offers = []
        for offer in data.get("data", []):
            segments = [
                FlightSegment(
                    departure=segment["departure"]["iataCode"],
                    arrival=segment["arrival"]["iataCode"],
                    departure_time=segment["departure"]["at"],
                    arrival_time=segment["arrival"]["at"],
                    carrier=segment["carrierCode"],
                    flight_number=segment["number"],
                )
                for segment in offer["itineraries"][0]["segments"]
            ]
            offers.append(
                FlightOffer(
                    id=offer["id"],
                    price=offer["price"]["total"],
                    currency=offer["price"]["currency"],
                    segments=segments,
                )
            )
        return offers