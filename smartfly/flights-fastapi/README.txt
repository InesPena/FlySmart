Installar dependencias:
pip install fastapi uvicorn httpx

Ejecutar el microservicio:
uvicorn main:app --reload

Endpoint: GET /flights
Permite buscar información de vuelos desde Amadeus API con origen, destino y fecha de salida como parámetros.
Ejemplo de consulta: http://127.0.0.1:8000/flights?origin=JFK&destination=LHR&departure_date=2025-01-25
