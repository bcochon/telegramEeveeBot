import os
from dotenv import load_dotenv

import telebot
from telebot import types as teletypes

from params import *
from utils import *
import commands
from img import AVAILABLE_PETS, get_img
from user_handler import check_banned, check_spam, get_user_step, set_user_step, use_groupchat, reached_limit

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
bannedUsers = []
debugginMode = False
muteStatus = []

# Definir comandos
commands.set_commands(bot)

logger.info("Bot Online")

# Message handlers
# Ignorar mensajes antiguos
@bot.message_handler(func=lambda msg: sent_secs_ago(msg, 30))
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
@bot.message_handler(commands=['toggledebug'], func=lambda msg: from_bot_owner(msg))
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
    txt = "Bienvenido a <b>EeveeBot</b>. Este bot permite obtener imágenes de Eevee & co de una amplia galería con más de 200 fotos! 😮\n\n"
    txt += "Estos son los comandos que podés usar:\n\n"
    txt += commands.cms_menu(lang)+'\n'
    txt += "Tené en cuenta que si interactuás con el bot en exceso (exceptuando comandos de fotos), serás baneado por 60 segundos.\n\n"
    txt += 'Podés encontrar el <a href="https://github.com/bcochon/telegramEeveeBot">código</a> detrás de este bot acá'
    bot.send_message(cid, txt, parse_mode='HTML', link_preview_options=teletypes.LinkPreviewOptions(is_disabled=True))  # send the generated help page
    check_spam(message.from_user.id)

# Start
@bot.message_handler(commands=['start', 's'])
def command_start(message):
    bot.reply_to(message, "Bienvenido jeje")
    command_help(message)

# Pets commands
@bot.message_handler(commands=['pets'])
def command_pets(message):
    lang = message.from_user.language_code
    buttons = []
    for pet in commands.commands_get(lang).pets :
        buttons.append(teletypes.InlineKeyboardButton(f'{pet}', callback_data=f'cb_pets_{pet}'))
    markup = teletypes.InlineKeyboardMarkup(row_width=2)
    markup.add(*buttons)
    bot.reply_to(message, 'Elegí qué fotos:', reply_markup=markup)
    check_spam(message.from_user.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cb_pets_'))
def callback_query(call : teletypes.CallbackQuery):
    cid = call.message.chat.id
    if call.message.chat.type == 'group':
        uid = call.from_user.id
        if reached_limit(uid, cid):
            bot.send_message(uid, f'Ups... alcanzaste el límite de usos en un chat grupal (vas a poder de nuevo en 12 hs o hasta que se apague el bot). Pero podés seguir usándome por mesajes privados mientras tanto!')
            return 1
        use_groupchat(uid, cid, now_timestamp())
    username = name_from_user(call.from_user)
    command = '/'+call.data.removeprefix('cb_pets_')
    message = bot.send_message(cid, f'{username} pidió una foto a través del menu /pets')
    cm_message = bot.reply_to(message, command)
    command_eevee(cm_message)

# Mute
@bot.message_handler(commands=['togglemute'])
def command_mute(message):
    cid = message.chat.id
    user = user_from_message(message)
    if cid not in muteStatus :
        muteStatus.append(cid)
        bot.reply_to(message, "Muted 🤐")
        this_status = 'muted'
    else :
        muteStatus.remove(cid)
        bot.reply_to(message, "We're so back 🤩")
        this_status = 'unmuted'
    logger.debug(f'El usuario {user} solicitó activar/desactivar muteStatus en el chat {cid} (muteStatus={this_status})')

# Pedir foto
@bot.message_handler(commands=list(AVAILABLE_PETS.keys()))
def command_eevee(message : teletypes.Message):
    cid = message.chat.id
    try :
        if message.chat.type == 'group' and message.from_user.id != bot.bot_id:
            uid = message.from_user.id
            if reached_limit(uid, cid):
                bot.send_message(uid, f'Ups... alcanzaste el límite de usos en un chat grupal (vas a poder de nuevo en 12 hs o hasta que se apague el bot). Pero podés seguir usándome por mesajes privados mientras tanto!')
                return 1
            use_groupchat(uid, cid, now_timestamp())
    except Exception as e:
        log_exception(e)
    user = user_from_message(message)
    mid = message.message_id
    args = message.text.split()
    pet = args[0].removeprefix('/').replace('@EeveeGalleryBot','')
    logger.debug(f'El usuario {user} solicitó una imagen de {pet}')
    try:
        img = None
        if len(args) > 1:
            img = get_img(pet=pet, image_id=args[1])
        else:
            img = get_img(pet)
        bot.send_chat_action(cid, 'upload_photo', timeout=90)
        logger.debug(f'Enviando imagen {img} a usuario {user}...')
        bot.send_photo(cid, img, reply_to_message_id=mid)
    except Exception as e:
        logger.error(f'Error al enviar {img} a usuario {user}')
        log_exception(e)
        bot.reply_to(message, "Ups, hubo un problema 😔")

# # Pedir foto hoy
# @bot.message_handler(commands=['eeveehoy'])
# def command_eeveeToday(message : teletypes.Message):
#     cid = message.chat.id
#     if message.chat.type == 'group' and message.from_user.id != bot.bot_id:
#         uid = message.from_user.id
#         if reached_limit(uid, cid):
#             bot.send_message(uid, f'Ups... alcanzaste el límite de usos en un chat grupal (vas a poder de nuevo en 12 hs o hasta que se apague el bot). Pero podés seguir usándome por mesajes privados mientras tanto!')
#             return 1
#         use_groupchat(uid, cid, now_timestamp())
#     user = user_from_message(message)
#     mid = message.message_id
#     img = get_today_img()
#     logger.debug(f'El usuario {user} solicitó una imagen de Eevee un día como hoy')
#     if img:
#         try:
#             bot.send_chat_action(cid, 'upload_photo', timeout=90)
#             logger.debug(f'Enviando imagen {img[0]} a usuario {user}...')
#             bot.send_photo(cid, open(img[0],'rb'), caption=f'Un día como hoy en {img[1]}...', reply_to_message_id=mid)
#         except Exception as e:
#             logger.error(f'Error al enviar {img[0]} a usuario {user}')
#             bot.reply_to(message, "Ups, hubo un problema 😔")
#     else:
#         bot.reply_to(message, "No hay una foto de Eevee un día como hoy en el calendario 😔")

# # Subir foto
# @bot.message_handler(commands=['upload'], func=lambda msg: from_bot_owner(msg))
# def command_upload(message):
#     cid = message.chat.id
#     uid = message.from_user.id
#     bot.send_message(cid, "Envía la imagen a añadir a la galería")
#     set_user_step(uid, 1)

# @bot.message_handler(content_types=ALLSCP, func=lambda msg:  get_user_step(msg.from_user.id) == 1)
# def command_uploaded(message):
#     cid = message.chat.id
#     bot.send_chat_action(cid, 'typing', timeout=90)
#     uid = message.from_user.id
#     if message.photo:
#         result = try_download_pic(message.photo, bot)
#     elif message.document:
#         result = try_download(message.document, bot)
#     else:
#         result = "Creo que eso no es una foto... cancelando operación"
#     bot.reply_to(message, result)
#     set_user_step(uid, 0)

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
        except Exception as e:
            logger.error("No se pudo finalizar la ejecución")
    else:
        bot.reply_to(message, "Finalización de ejecución cancelada")

# Hola
@bot.message_handler(func=lambda msg: msg.text.lower() == 'hola')
def command_hola(message):
    username = name_from_user(message.from_user) 
    bot.reply_to(message, f"Hola 🤙")
    check_spam(message.from_user.id)

# Default
@bot.message_handler(func=lambda msg: (not is_answering_pic(msg)) and (not muteStatus))
def command_default_msg(message):
    bot.reply_to(message, "No sé qué dijiste jeje ni idea. Usa /help para saber qué preguntarme 🤩")
    check_spam(message.from_user.id)

# Default (no texto)
@bot.message_handler(content_types=ALLSCP, func=lambda msg: (not is_answering_pic(msg)) and (not muteStatus))
def command_default(message):
    bot.reply_to(message, "Qué me mandaba (?")
    check_spam(message.from_user.id)


bot.infinity_polling()
logger.info("Ejecución finalizada")
commands.set_offline(bot)