import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
URL = "https://api.binance.com/api/v3/ticker/price?symbol="


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hello world")


@bot.message_handler(func=lambda message: True)
def show_price(message):
    symbol = message.text.upper()
    response = requests.get(URL + symbol)
    if response.status_code == 400:
        bot.send_message(message.chat.id, text=f"there is no token named {message.text}, please try again")
    elif response.status_code == 200:
        data = response.json()
        bot.send_message(message.chat.id, text=f"{data['symbol']} price is {data['price']}")
    else:
        bot.send_message(message.chat.id, text=f"some thing is wrong, please try again later")


bot.infinity_polling()
