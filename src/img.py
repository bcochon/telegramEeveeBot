import random
import imgur

AVAILABLE_PETS = imgur.generate_available_pets()

def get_img(pet, image_id=None) :
    if pet not in AVAILABLE_PETS : raise Exception(f"Invalid pet {pet}. Cannot get an image")
    imgs = imgur.get_album_images(AVAILABLE_PETS[pet])
    if image_id and image_id in [img['id'] for img in imgs]:
        img = imgur.get_album_image(AVAILABLE_PETS[pet], image_id)
    else:
        img = random.choice(imgs)
    return img['link']

if __name__ == '__main__' :
    result = get_img(pet='eevee')
    print(result)