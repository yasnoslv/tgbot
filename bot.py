import os
import logging
import random

from aiogram import Bot, Dispatcher, executor, types

from decouple import config

API_TOKEN = config('TG_BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_keyboard = types.ReplyKeyboardMarkup()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = 'Прівіт, радий тебе бачити!\n\n' \
            'Якщо ти хочеш дізнатися, що я вмію, то напиши /help'
    await message.reply(text, reply_markup=main_keyboard)

    
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Я бот для навчання Python. Поки що я вмію тільки це.")
    

def send_pic(text):
    dic = {'human': 'люд', 'nature': 'природ', 'space': 'космос'}
    names = dic.values()
    for name in names:
        if ('зображ') in text or ('картин') in text:
            if (name) in text:
                folder = [i for i in dic if dic[i]==name][0]
                list_of_photos = os.listdir(f'photos/{folder}')
                # remove .DS_Store
                for i in list_of_photos:
                    if not '.png' in i:
                        list_of_photos.remove(i)
                return f'photos/{folder}/{random.choice(list_of_photos)}'
            

@dp.message_handler()
async def echo(message: types.Message):
    path = send_pic(message.text.lower())
    try:
        await message.answer_photo(types.InputFile(path))
    except:
        pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    