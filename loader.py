from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import os

from config import API_TOKEN  # TODO: сделать в .env

BOT_TOKEN = API_TOKEN

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML', link_preview_is_disabled=True))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)