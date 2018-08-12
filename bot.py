#!/usr/bin/python3

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.utils.helpers import escape_markdown
import logging
from random import Random

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def keygen(length = 32, alphabet = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789_-`!@#$%^&890-=_+[]{}\\|;\\:",.<>/?'):
  random = Random()
  res = ''
  for i in range(length):
    res += random.choice(alphabet)
  return res

def start(bot, update):
  bot.send_message(chat_id = update.message.chat_id, text = "Let's keygen!",
                   reply_markup = button_markup)

def action(bot, update):
  res = '\n'.join([ '```%s```' % keygen() for i in range(4) ])
  try:
    bot.edit_message_text(res, chat_id = update.callback_query.message.chat.id, 
                          message_id = update.callback_query.message.message_id,
                          reply_markup = button_markup,
                          parse_mode = 'Markdown')
    bot.answer_callback_query(update.callback_query.id, text = 'Done')
  except:
    print(res)
    bot.answer_callback_query(update.callback_query.id, text = 'Error')

updater = Updater(token = open('token', 'rt').read())
dispatcher = updater.dispatcher
button_markup = InlineKeyboardMarkup(build_menu([InlineKeyboardButton('Generate', callback_data = 'generate keys')], n_cols = 1))
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(action))

try:
  updater.start_polling()
except:
  updater.stop()
