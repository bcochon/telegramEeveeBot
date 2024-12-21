import os
from dotenv import load_dotenv

import telebot

from params import *
from utils import *
import commands
from img import get_img
from img import get_today_img
from img import try_download_pic
from img import try_download
from user_handler import check_banned
from user_handler import check_spam
from user_handler import get_user_step
from user_handler import set_user_step

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

# Definir comandos
commands.set_commands(bot)

logger.info("Bot Online")


# Message handlers
# Ignorar mensajes antiguos
@bot.message_handler(func=lambda msg: sent_secs_ago(msg, 10))
def ignore(message):
    user = user_from_message(message)
    date = message_date_string(message)
    logger.debug(f"Ignorado mensaje de usuario {user} del {date}")
    loggerIgnore.debug('\n'+message_info_string(message))

# Test
@bot.message_handler(commands=['test', 't'])
def test(message):
    info = message_info_string(message)
    print(info)

# Modo Debug
@bot.message_handler(func=lambda msg: debugginMode and not from_bot_owner(msg))
def warn_debug(message):
    bot.reply_to(message, "El bot se encuentra en mantenimiento ahora mismo 😬. Intentá de nuevo más tarde 😔")
    check_spam(message.from_user.id)

# Toggle Modo Debug
@bot.message_handler(commands=['toggleDebug'], func=lambda msg: from_bot_owner(msg))
def command_debug(message):
    debugginMode = not debugginMode
    if debugginMode :
        bot.reply_to(message, "Modo debug activado")
    else :
        bot.reply_to(message, "Modo debug desactivado")

# Usuarios baneados
@bot.message_handler(func=lambda msg: msg.from_user.id in bannedUsers)
def reject_user(message):
    cid = message.chat.id
    user = user_from_message(message)
    bot.send_message(cid, f'El usuario {user} está baneadísimo ETERNAMENTE. Imposible que le dirija la palabra ❌')

# Control de spam
@bot.message_handler(func=lambda msg: check_banned(msg.from_user.id))
def warn_ban(message):
    cid = message.from_user.id
    bot.send_message(cid, text="Enviaste muchos mensajes en poco tiempo 🤡, estás baneado por 60 segundos 🙃")
    bot.send_message(cid, text="Para más info, escribí /help")

# Help
@bot.message_handler(commands=['help', 'h'])
def command_help(message):
    cid = message.chat.id
    lang = message.from_user.language_code
    cms = commands.commands_langs[lang]
    help_text = "Estos son los comandos que podés usar: \n"
    for key in cms:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + " — "
        help_text += cms[key] + "\n"
    bot.send_message(
        cid, 
        telebot.formatting.format_text(
            "Bienvenido a *EeveeBot*\\. Este bot permite obtener imágenes de Eevee de una amplia galería con más de 100 fotos\\! 😮\n",
            help_text,
            "Tené en cuenta que si interactuás con el bot en exceso \\(exceptuando comando /eevee\\), serás baneado por 60 segundos\\.\n",
            "Podés encontrar el [código](https://github.com/bcochon/telegramEeveeBot) detrás de este bot acá",
            separator="\n" # separator separates all strings
        ),
        parse_mode='MarkdownV2',
        link_preview_options=tele_types.LinkPreviewOptions(is_disabled=True)
    )  # send the generated help page
    check_spam(message.from_user.id)

# Start
@bot.message_handler(commands=['start', 's'])
def command_start(message):
    bot.reply_to(message, "Bienvenido jeje")
    command_help(message)

# Mute
@bot.message_handler(commands=['togglemute'])
def command_mute(message):
    muteStatus = not muteStatus
    if muteStatus :
        bot.reply_to(message, "🤐")
    else :
        bot.reply_to(message, "We're so back 🤩")

# Pedir foto
@bot.message_handler(commands=['eevee'])
def command_eevee(message):
    cid = message.chat.id
    mid = message.message_id
    args = message.text.split()
    if len(args) > 1:
        img = get_img(args[1])
    else:
        img = get_img('')
    try:
        bot.send_chat_action(cid, 'upload_photo', timeout=90)
        logger.debug(f'Enviando imagen {img} a usuario {cid}...')
        bot.send_photo(cid, open(img,'rb'), reply_to_message_id=mid)
    except:
        logger.error(f'Error al enviar {img} a usuario {cid}...')
        bot.reply_to(message, "Ups, hubo un problema 😔")

# Pedir foto hoy
@bot.message_handler(commands=['eeveehoy'])
def command_eeveeToday(message):
    cid = message.chat.id
    mid = message.message_id
    img = get_today_img()
    if img:
        try:
            bot.send_chat_action(cid, 'upload_photo', timeout=90)
            logger.debug(f'Enviando imagen {img} a usuario {cid}...')
            bot.send_photo(cid, open(img[0],'rb'), caption=f'Un día como hoy en {img[1]}...', reply_to_message_id=mid)
        except:
            logger.error('Error al enviar {img} a usuario {cid}...')
            bot.reply_to(message, "Ups, hubo un problema 😔")
    else:
        bot.reply_to(message, "No hay una foto de Eevee un día como hoy en el calendario 😔")

# Subir foto
@bot.message_handler(commands=['upload'], func=lambda msg: from_bot_owner(msg))
def command_upload(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot.send_message(cid, "Envía la imagen a añadir a la galería")
    set_user_step(uid, 1)

@bot.message_handler(content_types=ALLSCP, func=lambda msg:  get_user_step(msg.from_user.id) == 1)
def command_uploaded(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing', timeout=90)
    uid = message.from_user.id
    if message.photo:
        result = try_download_pic(message.photo, bot)
    elif message.document:
        result = try_download(message.document, bot)
    else:
        result = "Creo que eso no es una foto... cancelando operación"
    bot.reply_to(message, result)
    set_user_step(uid, 0)

# Finalizar ejecución
@bot.message_handler(commands=['q'], func=lambda msg: from_bot_owner(msg))
def command_quit(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot.send_message(cid, "Envía /confirm para finalizar")
    set_user_step(uid, 2)

@bot.message_handler(func=lambda msg:  get_user_step(msg.from_user.id) == 2)
def command_quitted(message):
    cid = message.chat.id
    uid = message.from_user.id
    set_user_step(uid, 0)
    if message.text.lower() == '/confirm':
        try:
            bot.send_message(cid, "Finalizando ejecución...")
            bot.stop_bot()
            logger.debug("Finalizando ejecución...")
        except:
            logger.error("No se pudo finalizar la ejecución")
    else:
        bot.reply_to(message, "Finalización de ejecución cancelada")

# Hola
@bot.message_handler(func=lambda msg: msg.text.lower() == 'hola')
def command_hola(message):
    username = name_from_user(message.from_user) 
    bot.reply_to(message, f"Hola {username} 🤙")
    check_spam(message.from_user.id)

# Default
@bot.message_handler(func=lambda msg: (not is_answering_pic(msg)) and (not muteStatus))
def command_default_msg(message):
    bot.reply_to(message, "No sé qué dijiste jeje ni idea. Usa /help para saber qué preguntarme 🤩")
    check_spam(message.from_user.id)

# Default (no texto)
@bot.message_handler(content_types=ALLSCP, func=lambda msg: (not is_answering_pic(msg)) and (not muteStatus))
def command_default(message):
    bot.reply_to(message, "Qué me mandaba \\(?")
    check_spam(message.from_user.id)


bot.infinity_polling()
logger.info("Ejecución finalizada")
commands.set_offline(bot)