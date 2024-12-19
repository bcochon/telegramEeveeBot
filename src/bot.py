import os

from dotenv import load_dotenv

import telebot

import params as ps
import utils
from img import get_img
from img import try_download_pic
from img import try_download
from user_handler import check_banned
from user_handler import check_spam

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

commands = {
    'start'         : 'Saludo amigable 🤩',
    'help'          : 'Conocer los comandos disponibles 🤓',
    'eevee'         : 'Para lo que vinimos 🙏',
    'togglemute'    : 'Para activar/desactivar las respuestas si no entiendo un mensaje 🧐'
}

# Test
@bot.message_handler(commands=['test'])
def test(message):
    utils.print_message(message)

# Control de spam
@bot.message_handler(func=lambda msg: check_banned(msg.from_user.id))
def warn_ban(message):
    cid = message.from_user.id
    bot.send_message(cid, text="Enviaste muchos mensajes en poco tiempo 🤡, estás baneado por 60 segundos 🙃")
    bot.send_message(cid, text="Para más info, escribí /help")

# Modo Debug
@bot.message_handler(func=lambda msg: ps.debugginMode and msg.from_user.username != ps.botOwner)
def warn_debug(message):
    bot.reply_to(message, "El bot se encuentra en mantenimiento ahora mismo 😬. Intentá de nuevo más tarde 😔")
    check_spam(message.from_user.id)

# Toggle Modo Debug
@bot.message_handler(commands=['toggleDebug'], func=lambda msg: msg.from_user.username == ps.botOwner)
def command_debug(message):
    ps.debugginMode = not ps.debugginMode
    if ps.debugginMode :
        bot.reply_to(message, "Modo debug activado")
    else :
        bot.reply_to(message, "Modo debug desactivado")

# Usuarios baneados
@bot.message_handler(func=lambda msg: msg.from_user.id in ps.bannedUsers)
def reject_user(message):
    cid = message.chat.id
    username = message.from_user.username
    bot.send_message(cid, f'El usuario {username} está baneadísimo ETERNAMENTE. Imposible que le dirija la palabra ❌')

# Help
@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    help_text = "Estos son los comandos que podés usar: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    ban_info = "Tené en cuenta que si interactuás con el bot en exceso \\(exceptuando comando /eevee\\), serás baneado por 60 segundos"
    bot.send_message(
        cid, 
        telebot.formatting.format_text(
            help_text,
            ban_info,
            separator="\n" # separator separates all strings
        ),
        parse_mode='MarkdownV2'
    )  # send the generated help page
    check_spam(message.from_user.id)

# Start
@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, "Bienvenido jeje")
    command_help(message)

# Mute
@bot.message_handler(commands=['togglemute'])
def command_mute(message):
    ps.muteStatus = not ps.muteStatus
    if ps.muteStatus :
        bot.reply_to(message, "🤐")
    else :
        bot.reply_to(message, "We're so back 🤩")

# Pedir foto
@bot.message_handler(commands=['eevee'])
def command_eevee(message):
    cid = message.chat.id
    args = message.text.split()
    if len(args) > 1:
        img = get_img(args[1])
    else:
        img = get_img('')
    bot.send_photo(cid, open(img,'rb'))

# Subir foto
@bot.message_handler(commands=['upload'], func=lambda msg: msg.from_user.username == ps.botOwner)
def command_upload(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot.send_message(cid, "Envía la imagen a añadir a la galería")
    utils.set_user_step(uid, 1)

@bot.message_handler(content_types=utils.ALLSCP, func=lambda msg:  utils.get_user_step(msg.from_user.id) == 1)
def command_uploaded(message):
    cid = message.chat.id
    uid = message.from_user.id
    if message.photo:
        result = try_download_pic(message.photo, bot)
    elif message.document:
        result = try_download(message.document, bot)
    else:
        result = "Creo que eso no es una foto... cancelando operación"
    bot.reply_to(message, result)
    utils.set_user_step(uid, 0)

# Default
@bot.message_handler(func=lambda msg: (not utils.is_answering_pic(msg)) and (not ps.muteStatus))
def command_default(message):
    bot.reply_to(message, "No sé qué dijiste jeje ni idea. Usa /help para saber qué preguntarme 🤩")
    check_spam(message.from_user.id)

# Default (no texto)
@bot.message_handler(content_types=utils.ALLSCP, func=lambda msg: (not utils.is_answering_pic(msg)) and (not ps.muteStatus))
def command_default(message):
    bot.reply_to(message, "Qué me mandaba \\(?")
    check_spam(message.from_user.id)



bot.infinity_polling()