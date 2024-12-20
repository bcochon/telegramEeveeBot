from telebot import types as tele_types
from user_handler import users
from user_handler import register_user
from params import BOT_OWNER


ALLSCP = ['audio', 'document', 'video', 'videonote', 'voice', 'location', 'contact', 'sticker', 'photo']

def is_answering_pic(message) :
    if message.reply_to_message:
        ansTo = message.reply_to_message
        if ansTo.photo:
            return True
        return False

def print_message(message) :
    user = message.from_user
    print(f'User ID:   {user.id}')
    print(f'User:      {user.first_name} {user.last_name}')
    print(f'Username:  {user.username}')
    print(f'Language:  {user.language_code}')
    print(f'Message:   {message.text}' )

def from_bot_owner(message) :
    return message.from_user.id == BOT_OWNER

def get_user_step(uid):
    if uid not in users:
        register_user(uid)
        print(f"New user {uid} detected, who hasn't used \"/start\" yet")
    return users[uid].step

def set_user_step(uid, step):
    users[uid].step = step