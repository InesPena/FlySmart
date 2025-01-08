from pydantic import BaseModel
from typing import List

class FlightSegment(BaseModel):
    departure: str
    arrival: str
    departure_time: str
    arrival_time: str
    carrier: str
    flight_number: str

class FlightOffer(BaseModel):
    id: str
    price: float
    currency: str
    segments: List[FlightSegment]