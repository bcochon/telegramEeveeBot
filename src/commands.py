from params import DEFAULT_LANG
from params import BOT_OWNER
from telebot import types as tele_types

# =============================== COMMANDS ===============================
privileged_commands = {
    'q'             : 'close bot execution',
    'toggledebug'   : 'toggle debug mode'
}

commands_es = {
    'start'         : 'Empezar a usar el bot 🤩',
    'help'          : 'Conocer los comandos disponibles 🤓',
    'eevee'         : 'Pedir foto de Eevee 🙏',
    'eeveehoy'      : 'Pedir foto de Eevee un día como hoy',
    'togglemute'    : 'Para activar/desactivar las respuestas si no entiendo un mensaje 🧐'
}

commands_langs = {
    'es' : commands_es
}

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

def set_privileged_commands(bot) :
    privileged_scope = tele_types.BotCommandScopeChat(chat_id=BOT_OWNER)
    privilegedCommandsList = commandsList+commands_list(privileged_commands)
    bot.set_my_commands(commands=privilegedCommandsList, scope=privileged_scope)

def set_commands(bot) :
    set_privileged_commands(bot)
    set_regular_commands(bot)