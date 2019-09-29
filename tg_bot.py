import os

import dotenv
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

dotenv.load_dotenv()
chat_id = os.environ['chat_id']


def main():
    dotenv.load_dotenv()
    token_tg = os.environ["token_tg"]
    run_tg_bot(token_tg)


def run_tg_bot(token_tg):
    updater = Updater(token_tg)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, dialog))

    updater.start_polling()

    updater.idle()


def start(bot, update):
    update.message.reply_text('Привет! Я бот для викторин')


def dialog(bot, update):
    custom_keyboard = [['Новый вопрос'], ['Сдаться']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=chat_id, text="Custom Keyboard Test", reply_markup=reply_markup)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


if __name__ == '__main__':
    main()
