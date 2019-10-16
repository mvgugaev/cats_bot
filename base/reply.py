from aiogram import types


class BotReplyKeyboards:

    @staticmethod
    def default_reply():
        menu_markup = types.reply_keyboard.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        menu_markup.row(types.reply_keyboard.KeyboardButton('5 котиков'), types.reply_keyboard.KeyboardButton('10 котиков'))
        menu_markup.row(types.reply_keyboard.KeyboardButton('Надпись'), types.reply_keyboard.KeyboardButton('О боте'))

        return menu_markup


    @staticmethod
    def text_render_reply():
        menu_markup = types.reply_keyboard.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        menu_markup.add(types.reply_keyboard.KeyboardButton('Отмена'))

        return menu_markup

