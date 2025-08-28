import asyncio
from loader import bot
from service.exchange_rate import exchange_rate_cache
import logging
from datetime import datetime, timedelta, timezone

from config import NEWS_CHANEL_ID, RATE_MESSAGE_ID, RATES_CACHE_TTL, RATE_MESSAGE_TEMPLATE

logger = logging.getLogger(__name__)

async def update_currency_message():
    last_rate = None
    while True:
        rate = await exchange_rate_cache.fetch_exchange_rate()
        new_rate_str = f"{rate:.3f}"

        if new_rate_str != last_rate:
            new_text = RATE_MESSAGE_TEMPLATE.format(rate=new_rate_str, update_ts=exchange_rate_cache.last_update)
            try:
                await bot.edit_message_text(new_text, chat_id=NEWS_CHANEL_ID, message_id=RATE_MESSAGE_ID, parse_mode="HTML")
            except Exception as e:
                logger.warning(f"Ошибка обновления сообщения {e}")
            last_rate = new_rate_str
            logger.info(f"Курс обновлен (rate={new_rate_str})")
        else:
            logger.debug("Курс банка не изменился")

        await asyncio.sleep(RATES_CACHE_TTL)



        # text = (
        #     f"💱 Актуальный курс юаня:\n"
        #     f"🇨🇳→🇧🇾 1 CNY = {rate:.3f} BYN\n\n"
        #     f"(данные обновляются раз в сутки)"
        # )

        # try:
        #     await bot.edit_message_text(text, chat_id=NEWS_CHANEL_ID, message_id=RATE_MESSAGE_ID, parse_mode="HTML")
        #     logger.info(f"Курс обновлен: {rate:.3f}")
        # except Exception as e:
        #     if "message is not modified" in str(e):
        #         logger.info(f"Курс не был обновлен, т.к. совпадает с предыдущим (rate={rate})")
        #     else:
        #         logger.error(f"Не удалось обновить курс{e}", exc_info=True)
        # await asyncio.sleep(RATES_CACHE_TTL)