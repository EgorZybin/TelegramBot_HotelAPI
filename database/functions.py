from loguru import logger
from database.models import *


def add_user(chat_id, username, full_name) -> None:
    try:
        User.create(chat_id=chat_id, username=username, full_name=full_name)
        logger.info('Добавлен новый пользователь.')
    except IntegrityError:
        logger.info('Данный пользователь уже существует')


def add_query(query_data) -> None:
    user, created = User.get_or_create(chat_id=query_data['chat_id'])
    Query.create(user_id=user, input_city=query_data['input_city'],
                 photo_need=query_data['photo_need'], destination_id=query_data['destination_id'],
                 date_time=query_data['date_time'])
    logger.info('Добавлен в БД новый запрос.')
    # Ограничение хранения последних 5 записей
    if Query.select().where(Query.user_id == user).count() > 5:
        old_query = Query.select().where(Query.user_id == user).order_by(Query.date_time.asc()).get()
        old_query.delete_instance()


def add_response(search_result) -> None:
    for item in search_result.items():
        query = Query.get(Query.date_time == item[1]['date_time'])
        response = Response.create(query_id=query, hotel_id=item[0], name=item[1]['name'],
                                   address=item[1]['address'], price=item[1]['price'], distance=item[1]['distance'])
        logger.info('Добавлены в БД данные отеля.')
        for link in item[1]['images']:
            Image.create(hotel_id=response, link=link)
        logger.info('Добавлены в БД ссылки на фотографии отеля.')


def read_query(user_id):
    logger.info(f'Читаем таблицу query. User_id: {user_id}')
    user_queries = (Query
                    .select()
                    .join(User)
                    .where(User.chat_id == user_id)
                    .order_by(Query.date_time.desc()))

    return user_queries
