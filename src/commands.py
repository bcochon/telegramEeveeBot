from params import DEFAULT_LANG
from params import BOT_OWNER
from img import AVAILABLE_PETS
from telebot import types as tele_types
from utils import logger

# =============================== COMMANDS ===============================

commands_langs = {}

class CommandsByLanguage :
    def __init__(self, language, privileged, offline, menu, extra, pet_format) :
        self.language = language
        self.privileged = privileged
        self.offline = offline
        self.menu = menu
        self.extra = extra
        self.pets = {}
        for pet in AVAILABLE_PETS :
            command = pet_format.format(pet.replace('_',' ').capitalize())
            self.pets.update({pet : command})
        commands_langs.update({language : self})

    def get_regular(self) :
        return self.menu|self.pets|self.extra
    
    def get_privileged(self) :
        return self.get_regular()|self.privileged

commands_es = CommandsByLanguage(
    language = 'es',
    privileged = {
        'q'             : 'close bot execution',
        'toggledebug'   : 'toggle debug mode',
    },
    offline = {
        'offline'       : 'bot apagado ahora mismo 😴'
    },
    menu = {
        'help'          : 'guía de uso 🤓',
        'pets'          : 'ver galerías disponibles 🐶'
    },
    extra = {
        'togglemute'    : 'para ignorar mensajes que no entendí 🧐',
    },
    pet_format = 'pedir foto de {}'
)

privileged_scope = tele_types.BotCommandScopeChat(chat_id=BOT_OWNER)

# ============================== FUNCTIONS ===============================

def commands_get(lang: str) :
    if lang in commands_langs :
        return commands_langs[lang]
    return commands_langs[DEFAULT_LANG]

def commands_list(commands: dict) :
    list = []
    for key in commands:
        list.append(tele_types.BotCommand(key, commands[key]))
    return list

regularCommandsList = commands_list(commands_langs[DEFAULT_LANG].get_regular())
privilegedCommandsList = commands_list(commands_langs[DEFAULT_LANG].get_privileged())
offlineCommandsList = commands_list(commands_langs[DEFAULT_LANG].offline)

def set_regular_commands(bot) :
    for lang in commands_langs:
        thisLangCommands = commands_get(lang).get_regular()
        bot.set_my_commands(commands=commands_list(thisLangCommands), language_code=lang)
    logger.debug('Comandos regulares establecidos')

def delete_regular_commands(bot) :
    for lang in commands_langs:
        bot.delete_my_commands(language_code=lang)
    logger.debug('Comandos regulares eliminados')

def set_privileged_commands(bot) :
    bot.set_my_commands(commands=privilegedCommandsList, scope=privileged_scope)
    logger.debug('Comandos privilegiados establecidos')

def delete_privileged_commands(bot) :
    bot.delete_my_commands(scope=privileged_scope)
    logger.debug('Comandos privilegiados eliminados')

def set_commands(bot) :
    bot.set_my_commands(commands=regularCommandsList)
    set_privileged_commands(bot)
    set_regular_commands(bot)

def delete_commands(bot) :
    bot.delete_my_commands()
    delete_privileged_commands(bot)
    delete_regular_commands(bot)

def set_offline(bot) :
    delete_commands(bot)
    bot.set_my_commands(commands=offlineCommandsList)
    logger.debug('Comandos seteados offline')

def cms_menu(lang : str) :
    cms_menu = commands_get(lang).menu
    cms_pets = commands_get(lang).pets
    cms_extra = commands_get(lang).extra
    menu = cms_string(cms_menu)
    menu += "\n<b>Pedir fotos</b>\n"
    menu += cms_string(cms_pets)
    menu += "\n<b>Extras</b>\n"
    menu += cms_string(cms_extra)
    return menu

def cms_string(cms : dict) :
    result = ''
    for key in cms:
        result += f'/{key} — {cms[key]}\n'
    return result