import logging
import config
from base.gif_source import GifSource
from base.data import UserStorage
from base.reply import BotReplyKeyboards
from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_API_TOKEN, proxy=config.BOT_PROXY_URL)
dp = Dispatcher(bot)

# User data storage
storage = UserStorage()

# Default keyboard menu
default_keyboard = BotReplyKeyboards.default_reply()
text_render_keyboard = BotReplyKeyboards.text_render_reply()

# Start and help text message
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=config.WELCOME_TETX, reply_markup=default_keyboard)


# 5 cats handler
@dp.message_handler(lambda message: message.text == '5 котиков')
async def multi_cats(message: types.Message):
    for i in range(5):
        url = await GifSource.get_random_cat_url()
        await message.answer_document(document=url, reply_markup=default_keyboard)


# 10 cats handler
@dp.message_handler(lambda message: message.text == '10 котиков')
async def multi_cats_big(message: types.Message):
    for i in range(10):
        url = await GifSource.get_random_cat_url()
        await message.answer_document(document=url, reply_markup=default_keyboard)


# Gif text handler
@dp.message_handler(lambda message: message.text == 'Надпись')
async def text_render(message: types.Message):

    # Set step data
    storage.data_set(message.from_user.id, 'step', 'text_render')
    await bot.send_message(chat_id=message.chat.id, text=config.RENDER_TEXT, reply_markup=text_render_keyboard)


# About bot handler
@dp.message_handler(lambda message: message.text == 'О боте')
async def about_bot(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=config.ABOUT_TEXT, reply_markup=default_keyboard)


# Base handler
@dp.message_handler()
async def cats(message: types.Message):
    if storage.data_get(message.from_user.id, 'step') == 'text_render':

        # Render gif with text from message
        storage.data_set(message.from_user.id, 'step', '')
        await bot.send_message(chat_id=message.chat.id, text=config.RENDER_TEXT_WAIT, reply_markup=text_render_keyboard)
        await message.answer_document(document=config.RENDER_TEXT_URL.replace('{text}', message.text), reply_markup=default_keyboard)
    else:
        url = await GifSource.get_random_cat_url()
        await message.answer_document(document=url, reply_markup=default_keyboard)


# Start bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)