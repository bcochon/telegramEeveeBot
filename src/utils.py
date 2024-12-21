from telebot import types as tele_types
from params import BOT_OWNER
from datetime import datetime
from time import time

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

def print_message(message) :
    user = message.from_user
    date = datetime.fromtimestamp(message.date).strftime('%d-%m-%Y %H:%M:%S')
    print(f'User ID:   {user.id}')
    print(f'User:      {user.first_name} {user.last_name}')
    print(f'Username:  {user.username}')
    print(f'Language:  {user.language_code}')
    print(f'Message:   {message.text}' )
    print(f'Date:      {date}')

def from_bot_owner(message) :
    return message.from_user.id == BOT_OWNER