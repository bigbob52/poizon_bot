import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("BOT_API_TOKEN")

# --- Курсы юаня ---
EXCHANGE_RATE_API_URL = 'https://api.nbrb.by/ExRates/Rates/CNY?ParamMode=2'
RATES_CACHE_TTL = 24*60*60  # in seconds

# --- TG ---
MANAGER_ID = -1003064929034  # канал с менеджерами
MANAGER_URL = "https://t.me/PoizonBelarusManager"

# --- RATE UPDATER ---
NEWS_CHANEL_ID = -1001146385584
RATE_MESSAGE_ID = 36
RATE_MESSAGE_TEMPLATE = (
    "💱 Актуальный курс юаня:\n\n"
    "<b>🇨🇳 1 CNY → 🇧🇾 {rate} BYN</b>\n\n"
    "<i>⏱️ Обновлено: {update_ts}</i>"
)

# --- ADMIN ---
ADMIN_IDS = [
    817879037, # я
    889218380, # пашок
    894690269, # бебра
]

ADMIN_ALERT_NEW_USER = False

ORDERS_PAGE_SIZE = 5  # кол-во заказов на странице при выводе (пагинация)

STATUS_DISPLAY = {
    "processing":   "В обработке ⌛️",
    "accepted":     "Принят 🟢",
    "cancelled":    "Отклонен ❌",
    "on_the_way":   "В пути 🚚",
    "done":         "Выполнен ✅"
}
