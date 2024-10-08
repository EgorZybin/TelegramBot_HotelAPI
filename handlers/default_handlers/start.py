from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    bot.reply_to(message,
                     f"Привет! Я бот-помощник HotelNavigatorBot. Помогу в поиске лучших отелей по всему миру. Чтобы увидеть полный список моих функций, напишите /help.")





