from aiogram import Bot, Dispatcher, executor, types
import os
import sqlite3


def create_db():
    connect = sqlite3.connect('kitchenBOT.db')
    cursor = connect.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users_info('
        'id integer primary key autoincrement, '
        'first_name text, '
        'last_name text,'
        'nickname text,'
        'user_id integer key)')
    connect.commit()


def add_new_user(user_data, user):
    connect = sqlite3.connect('kitchenBOT.db')
    cursor = connect.cursor()
    user_id = user
    cursor.execute(f'SELECT user_id FROM users_info WHERE user_id = {user_id}')
    exam = cursor.fetchone()
    if exam is None:
        req = 'INSERT INTO users_info(' \
              'first_name, last_name, nickname, user_id' \
              ')VALUES('

        for i in user_data:
            req += f'"{i}", '
        req = req[:-2] + ');'
        cursor.execute(req)
        connect.commit()


create_db()

TOKEN = os.environ['token']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}


@dp.message_handler()
async def echo(message: types.Message):
    user_data = [message.from_user.first_name, message.from_user.last_name,
                 message.from_user.username, message.from_user.id]
    add_new_user(user_data, message.from_user.id)
    print(message.from_user.id, ' - ', message.from_user.first_name, ' - ', message.text)
    users.update({message.from_user.id: message.from_user.first_name})
    text = f'Пользователь {message.from_user.first_name} написал {message.text}'
    for i in users.keys():
        if i != message.from_user.id:
            await bot.send_message(chat_id=i,
                                   text=text)


if __name__ == '__main__':
    executor.start_polling(dp)
