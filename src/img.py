import random
import pickle
from datetime import date
import os

from utils import logger
from params import IMGS_DIR
from params import MAX_FILE_SIZE
from params import NEW_IMG_PREFIX
from params import NEW_IMG_SUFIX
from params import NEW_IMG_INDEX_PATH

from imgs_data import imgs_dict

AVAILABLE_PETS = os.listdir(f'{IMGS_DIR}')

def get_img(name, dir) :
    if dir not in AVAILABLE_PETS : raise Exception(f"Invalid directory {dir}. Cannot get an image")
    path = f'{IMGS_DIR}/{dir}'
    imgs = os.listdir(path)
    if name in imgs:
        img = name
    else:
        img = random.choice(imgs)
    return f'{path}/{img}'

def get_today_img() :
    today = (date.today()).isoformat()
    validImgs = list(filter(lambda img: (same_date(imgs_dict[img], today) and (NEW_IMG_PREFIX not in img)), list(imgs_dict.keys())))
    if validImgs:
        img = random.choice(validImgs)
        path = f'{IMGS_DIR}/eevee/{img}'
        year = imgs_dict[img].split('-')[0]
        return [path, year]
    return []

def same_date(date1 : str, date2 : str) :
    [ year1, month1, day1 ] = date1.split('-')
    [ year2, month2, day2 ] = date2.split('-')
    return day1 == day2 and month1 == month2

def check_newImageIndex() :
    botImgs = list(filter(lambda img: (NEW_IMG_PREFIX in img), list(imgs_dict.keys())))
    botImgs = map(lambda img: int(img.removeprefix(NEW_IMG_PREFIX).removesuffix(NEW_IMG_SUFIX)), botImgs)
    return max(botImgs)+1

def set_newImageIndex(newImageIndex) :
    with open(NEW_IMG_INDEX_PATH, 'wb') as f: 
        pickle.dump(newImageIndex, f)

def get_newImageIndex() :
    try:
        with open(NEW_IMG_INDEX_PATH, 'rb') as f: 
            newImageIndex = pickle.load(f)
    except:
        newImageIndex = check_newImageIndex()
        set_newImageIndex(newImageIndex)
    return newImageIndex

def create_new_img_name() :
    newImageIndex = get_newImageIndex()
    newName = f"{NEW_IMG_PREFIX}{newImageIndex}{NEW_IMG_SUFIX}"
    newImageIndex += 1
    set_newImageIndex(newImageIndex)
    return newName

def is_valid_pic(photo) :
    return photo.file_size < MAX_FILE_SIZE

def download_pic(name, pic) :
    path = IMGS_DIR + '/eevee/' + name
    with open(path, 'wb') as new_file:
        new_file.write(pic)
    logger.info(f"Guardada imagen {path}")

def try_download(file, bot) :
    if not is_valid_pic(file) :
        return f"Foto no válida. Excede el tamaño máximo \\({MAX_FILE_SIZE/(10**6)}\\ megabytes)"
    else:
        fileInfo = bot.get_file(file.file_id)
        downloadedFile = bot.download_file(fileInfo.file_path)
        name = create_new_img_name()
        download_pic(name, downloadedFile)
        logger.debug(f'Se descargó la imagen {name}')
        return f"Imagen descargada con exito! Yippie! ('{name}')"
    
def try_download_pic(photos, bot) :
    photo = photos[-1] # Best quality in -1 index
    try_download(photo, bot)