from loader import bot
from telebot.types import Message
from loguru import logger
import database


@bot.message_handler(commands=['history'])
def send_history(message: Message) -> None:
    """
        Обработчик команд, срабатывает на команду /history
        Обращается к базе данных и выдает в чат запросы пользователя
        по отелям.
        : param message : Message
        : return : None
    """
    logger.info(f'Выбрана команда history! User_id: {message.chat.id}')
    user_id = message.chat.id
    queries = database.functions.read_query(user_id)

    if not queries:
        bot.send_message(message.chat.id, "История запросов пуста.")
    else:
        history_message = "История ваших запросов:\n"
        for query in queries:
            history_message += f"Дата и время: {query.date_time}\n" \
                               f"Город назначения: {query.input_city}\n" \
                               f"ID направления: {query.destination_id}\n" \
                               f"Нужны ли фото: {'Да' if query.photo_need else 'Нет'}\n\n"

        bot.send_message(message.chat.id, history_message)
