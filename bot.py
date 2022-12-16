import os
import random

import requests
from bs4 import BeautifulSoup
from telebot import TeleBot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
URL = "https://paper-trader.frwd.one"
TIMEFRAME = ["5m", "15m", "1h", "4h", "1d", "1w", "1M"]

bot = TeleBot(BOT_TOKEN)


def get_image(trade_pair):
    payload = {
        "pair": trade_pair,
        "timeframe": random.choice(TIMEFRAME),
        "candles": random.randint(1, 1000),
        "ma": random.randint(1, 50),
        "tp": random.randint(1, 100),
        "sl": random.randint(1, 100)
    }
    page = requests.post(URL, data=payload).text
    soup = BeautifulSoup(page, "html.parser")
    image_url = URL + soup.find("img")["src"][1:]
    return image_url


@bot.message_handler(commands=["start"])
def start(message):
    greeting = ("Hi, i'm paper trading bot, pick one trade pair for begin"
                "(BTCUSDT, BNBUSDT or ETHUSDT)")
    bot.send_message(message.chat.id, greeting, parse_mode="html")


@bot.message_handler()
def get_user_text(message):
    if message.text in ["BTCUSDT", "BNBUSDT", "ETHUSDT"]:
        img = get_image(message.text)
        bot.send_photo(message.chat.id, img)
    else:
        warning = ("Please choose one of this pairs"
                   "(BTCUSDT, BNBUSDT or ETHUSDT)")
        bot.send_message(message.chat.id, warning, parse_mode="html")


bot.polling(none_stop=True)
