import os
import random

imgsDir = "../imgs"

def getRandomImg() :
    return imgsDir + '/' + random.choice(os.listdir(imgsDir))