from telebot import types as tele_types
from user_handler import users
from user_handler import register_user


ALLSCP = ['audio', 'document', 'video', 'videonote', 'voice', 'location', 'contact', 'sticker', 'photo']

def commands_list(commands) :
    list = []
    for key in commands:
        list.append(tele_types.BotCommand(key, commands[key]))
    return list

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
    print(f'Message:   {message.text}' )

def get_user_step(uid):
    if uid not in users:
        register_user(uid)
        print(f"New user {uid} detected, who hasn't used \"/start\" yet")
    return users[uid].step

def set_user_step(uid, step):
    users[uid].step = step