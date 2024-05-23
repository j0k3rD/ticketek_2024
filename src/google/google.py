from src.database.models import EventBase
import httpx 
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

class GoogleGetLocation():
    def __init__(self, location: str) -> None:
        self.location = location

    async def get_location(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={self.location}&key={API_KEY}")
            response.raise_for_status()
            data = response.json()
            return data['results'][0]['geometry']['location']
