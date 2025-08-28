import aiohttp
from config import EXCHANGE_RATE_API_URL, RATES_CACHE_TTL
from async_lru import alru_cache
from datetime import datetime, timedelta, timezone


class ExchangeRateCache:
    def __init__(self):
        self.last_update = None

    @alru_cache(ttl=RATES_CACHE_TTL)
    async def fetch_exchange_rate(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(EXCHANGE_RATE_API_URL) as resp:
                data = await resp.json()
                rate = data["Cur_OfficialRate"]/10
                self.last_update = datetime.now(timezone(timedelta(hours=3))).strftime("%H:%M:%S %d.%m.%Y")
                return rate

exchange_rate_cache = ExchangeRateCache()