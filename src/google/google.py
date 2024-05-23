from src.database.models import EventBase
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


class GoogleGetLocation:

    async def get_location(self, address: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
            )
            response.raise_for_status()
            data = response.json()

            # Converti a un json de latitud y longitud
            location = data["results"][0]["geometry"]["location"]
            return location
