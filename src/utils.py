from telebot import types as tele_types
import logging
import logging.config
from params import BOT_OWNER
from params import LOGGER_CONFIG_PATH
from datetime import datetime
from time import time

logging.config.fileConfig(LOGGER_CONFIG_PATH)
logger = logging.getLogger('EeveeBot')
loggerIgnore = logging.getLogger('Ignore')

ALLSCP = ['audio', 'document', 'video', 'videonote', 'voice', 'location', 'contact', 'sticker', 'photo']

def is_answering_pic(message) :
    if message.reply_to_message:
        ansTo = message.reply_to_message
        if ansTo.photo:
            return True
        return False
    
def sent_secs_ago(message, secs) :
    time_since_mesage = int(time()) - message.date
    return time_since_mesage > secs

def message_date_string(message) :
    return datetime.fromtimestamp(message.date).strftime('%d-%m-%Y %H:%M:%S')

def user_from_message(message) :
    user = message.from_user.username
    if user: return user
    return message.chat.id

def name_from_user(user) :
    name = user.first_name
    if name: return name
    name = user.username
    if name: return name
    return ''

def message_info(message) :
    user = message.from_user
    date = message_date_string(message)
    info = {
        'UserID':    user.id,
        'User':      user.first_name+user.last_name,
        'Username':  user.username,
        'Language':  user.language_code,
        'Message':   message.text,
        'Date':      date
    }
    return info

def message_info_string(message):
    info = message_info(message)
    info_string = ''
    for key in info:
        info_string += f'{key}: {info[key]}\n'
    return info_string

def from_bot_owner(message) :
    return message.from_user.id == BOT_OWNER