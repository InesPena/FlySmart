Installar dependencias:
pip install fastapi uvicorn httpx
pip install jinja2 python-multipart

Ejecutar el microservicio:
uvicorn main:app --reload --port 8080

Página de inicio: http://127.0.0.1:8080

Endpoint: GET /flights
Permite buscar información de vuelos desde Amadeus API con origen, destino y fecha de salida como parámetros.
Ejemplo de consulta: 
http://127.0.0.1:8080/flights?origin=JFK&destination=LHR&departure_date=2024-12-25
http://127.0.0.1:8080/register


