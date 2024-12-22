from params import DEFAULT_LANG
from params import BOT_OWNER
from img import AVAILABLE_PETS
from telebot import types as tele_types
from utils import logger

# =============================== COMMANDS ===============================

privileged_commands = {
    'q'             : 'close bot execution',
    'toggledebug'   : 'toggle debug mode',
    'upload'        : 'upload new pics'
}

offline_commands = {
    'offline'       : 'bot apagado ahora mismo 😴'
}

commands_es = {
    'help'          : 'conocer los comandos disponibles 🤓',
    'eeveehoy'      : 'pedir foto de Eevee un día como hoy',
    'togglemute'    : 'para ignorar mensajes que no entendí 🧐'
}

pet_commands = {
    'es' : 'pedir foto de {} 🙏'
}

commands_langs = {
    'es' : commands_es
}

for lang in commands_langs :
    for pet in AVAILABLE_PETS :
        command = pet_commands[lang].format(pet.capitalize())
        commands_langs[lang].update({pet : command})

privileged_scope = tele_types.BotCommandScopeChat(chat_id=BOT_OWNER)

# ============================== FUNCTIONS ===============================

def commands_get(lang) :
    cmds = commands_langs[lang]
    if not cmds :
        cmds = commands_langs[DEFAULT_LANG]
    return cmds

def commands_list(commands) :
    list = []
    for key in commands:
        list.append(tele_types.BotCommand(key, commands[key]))
    return list
commandsList = commands_list(commands_langs[DEFAULT_LANG])

def set_regular_commands(bot) :
    for lang in commands_langs:
        thisLangCommands = commands_get(lang)
        bot.set_my_commands(commands=commands_list(thisLangCommands), language_code=lang)
    logger.debug('Comandos regulares establecidos')

def delete_regular_commands(bot) :
    for lang in commands_langs:
        bot.delete_my_commands(language_code=lang)
    logger.debug('Comandos regulares eliminados')

def set_privileged_commands(bot) :
    privilegedCommandsList = commandsList+commands_list(privileged_commands)
    bot.set_my_commands(commands=privilegedCommandsList, scope=privileged_scope)
    logger.debug('Comandos privilegiados establecidos')

def delete_privileged_commands(bot) :
    bot.delete_my_commands(scope=privileged_scope)
    logger.debug('Comandos privilegiados eliminados')

def set_commands(bot) :
    bot.set_my_commands(commands=commands_list(commands_langs[DEFAULT_LANG]))
    set_privileged_commands(bot)
    set_regular_commands(bot)

def delete_commands(bot) :
    bot.delete_my_commands()
    delete_privileged_commands(bot)
    delete_regular_commands(bot)

def set_offline(bot) :
    delete_commands(bot)
    bot.set_my_commands(commands=commands_list(offline_commands))
    logger.debug('Comandos seteados offline')