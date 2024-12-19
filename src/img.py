import random
import pickle
from datetime import date

from params import imgsDir
from params import maxFileSize
from params import newImagePrefix
from params import newImageSufix
from params import newImageIndexPath

from imgs_data import imgs_dict

def get_img(name) :
    if name in imgs_dict:
        img = name
    else:
        img = random.choice(list(imgs_dict.keys()))
    return f'../{imgsDir}/{img}'

def get_today_img() :
    today = (date.today()).isoformat()
    validImgs = list(filter(lambda img: (imgs_dict[img] == today), list(imgs_dict.keys())))
    if validImgs:
        img = random.choice(validImgs)
        path = f'../{imgsDir}/{img}'
        year = imgs_dict[img].split('-')[0]
        return [path, year]
    return []

def check_newImageIndex() :
    botImgs = list(filter(lambda img: (newImagePrefix in img), list(imgs_dict.keys())))
    botImgs = map(lambda img: int(img.removeprefix(newImagePrefix).removesuffix(newImageSufix)), botImgs)
    return max(botImgs)+1

def set_newImageIndex(newImageIndex) :
    with open(newImageIndexPath, 'wb') as f: 
        pickle.dump(newImageIndex, f)

def get_newImageIndex() :
    try:
        with open(newImageIndexPath, 'rb') as f: 
            newImageIndex = pickle.load(f)
    except:
        newImageIndex = check_newImageIndex()
        set_newImageIndex(newImageIndex)
    return newImageIndex

def create_new_img_name() :
    newImageIndex = get_newImageIndex()
    newName = f"{newImagePrefix}{newImageIndex}{newImageSufix}"
    newImageIndex += 1
    set_newImageIndex(newImageIndex)
    return newName

def is_valid_pic(photo) :
    return photo.file_size < maxFileSize

def download_pic(name, pic) :
    path = imgsDir + '/' + name
    with open(path, 'wb') as new_file:
        new_file.write(pic)
    print(f"Guardada imagen {path}\n")

def try_download(file, bot) :
    if not is_valid_pic(file) :
        return f"Foto no válida. Excede el tamaño máximo \\({maxFileSize/(10**6)}\\ megabytes)"
    else:
        fileInfo = bot.get_file(file.file_id)
        downloadedFile = bot.download_file(fileInfo.file_path)
        name = create_new_img_name()
        download_pic(name, downloadedFile)
        return f"Imagen descargada con exito! Yippie! \\('{name}'\\)"
    
def try_download_pic(photos, bot) :
    photo = photos[-1] # Best quality in -1 index
    try_download(photo, bot)