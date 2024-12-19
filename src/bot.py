import os

from dotenv import load_dotenv, dotenv_values
import telebot

from parameters import bannedUsers
from img import getRandomImg

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

commands = {
    'start'     : 'Saludo amigable',
    'help'      : 'Conocer los comandos disponibles',
    'eevee'     : 'Para lo que vinimos 🙏'
}


# Usuarios baneados
@bot.message_handler(func=lambda msg: msg.from_user.username in bannedUsers)
def reject_user(message):
    cid = message.chat.id
    username = message.from_user.username
    bot.send_message(cid, f'El usuario {username} está baneadísimo. Imposible que le dirija la palabra ❌')

# Help
@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    help_text = "Estos son los comandos que podés usar: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

# Start
@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, "Bienvenido jeje")
    command_help(message)

# Pedir foto
@bot.message_handler(commands=['eevee'])
def command_start(message):
    cid = message.chat.id
    img = getRandomImg()
    bot.send_photo(cid, open(img,'rb'))

# Default
@bot.message_handler(func=lambda msg: True)
def command_default(message):
    bot.reply_to(message, "No sé qué dijiste jeje ni idea. Usa /help para saber qué preguntarme 🤩")

bot.infinity_polling()