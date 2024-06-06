import aiohttp
import asyncio
from datetime import datetime, timedelta

class CurrencyService:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={}"

    async def fetch_rate(self, session, date: str):
        url = self.BASE_URL.format(date)
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch data: {response.status}")
            return await response.json()

    async def get_exchange_rates(self, days: int):
        today = datetime.today()
        results = {}
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(days):
                date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
                tasks.append(self.fetch_rate(session, date))
            responses = await asyncio.gather(*tasks)
            for response in responses:
                date = response['date']
                rates = {
                    "EUR": next((item.get('saleRate', None) for item in response['exchangeRate'] if item.get('currency') == 'EUR'), None),
                    "USD": next((item.get('saleRate', None) for item in response['exchangeRate'] if item.get('currency') == 'USD'), None)
                }
                results[date] = rates
        return results
