import os
import random
import pickle

from params import imgsDir
from params import maxFileSize
from params import newImagePrefix

def get_img(name) :
    if name in os.listdir(imgsDir):
        img = name
    else:
        img = random.choice(os.listdir(imgsDir))
    return imgsDir + '/' + img

def create_new_img_name() :
    newImageIndex = get_newImageIndex()
    newName = f"{newImagePrefix}{newImageIndex}.jpg"
    newImageIndex += 1
    set_newImageIndex(newImageIndex)
    return newName

def get_newImageIndex() :
    with open('./src/newImageIndex', 'rb') as f: 
        newImageIndex = pickle.load(f)
    return newImageIndex

def set_newImageIndex(newImageIndex) :
    with open('./src/newImageIndex', 'wb') as f: 
        pickle.dump(newImageIndex, f)

def try_download_pic(photos, bot) :
    photo = photos[-1] # Best quality in -1 index
    try_download(photo, bot)

def try_download(file, bot) :
    if not is_valid_pic(file) :
        return f"Foto no válida. Excede el tamaño máximo \\({maxFileSize/(10**6)}\\ megabytes)"
    else:
        fileInfo = bot.get_file(file.file_id)
        downloadedFile = bot.download_file(fileInfo.file_path)
        name = create_new_img_name()
        download_pic(name, downloadedFile)
        return f"Imagen descargada con exito! Yippie! \\('{name}'\\)"

def is_valid_pic(photo) :
    return photo.file_size < maxFileSize

def download_pic(name, pic) :
    path = imgsDir + '/' + name
    with open(path, 'wb') as new_file:
        new_file.write(pic)
    print(f"Guardada imagen {path}\n")