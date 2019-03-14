from django.conf import settings
from PIL import Image, ImageEnhance
import os

import pdb

def get_box_thumb(image, TIS):
    """
    image - объект картинка, на которую накладываете изображение
    TIS - THUMB_IMAGE_SIZE (50, 50)

    """
    img_w, img_h = image.size
    min_size = min(img_w, img_h)
    left = int((img_w-min_size)/2)
    upper = int((img_h-min_size)/2)
    box = (left, upper, left+min_size, upper+min_size)
    image = image.crop(box)
    image.thumbnail(TIS, resample=Image.LANCZOS)
    return image


def get_rename_path(path, newname):
    '''Возвращает путь к переименованному файлу'''

    ext = os.path.splitext(path)[1]
    dirpath = os.path.dirname(path)
    return '{0}/{1}{2}'.format(dirpath, newname, ext)


def get_prefix_path(path, prefix='tmb'):
    '''Возвращает путь к превюшки'''

    split = os.path.splitext(path)
    dirname, ext = split
    thumb_file_name = '{0}_{1}{2}'.format(dirname, prefix, ext)
    return thumb_file_name


def add_watermark(image, watermark_path=settings.WATERMARK_PATH, opacity=0.3, opacity2=0.2):
    """
    image - объект картинка, на которую накладываете изображение
    watermark - картинка, которую накладываете
    opacity - прозрачность

    """

    assert opacity >= 0 and opacity <= 1
    watermark = Image.open(watermark_path)

    img_w, img_h = image.size
    wat_w, wat_h = watermark.size
    if wat_w != img_w:
        width = img_w
        height = int(max(wat_h * img_w / wat_w, 1))
        max_size = (width, height)
        watermark = watermark.resize(max_size, Image.ANTIALIAS)
        wat_w, wat_h = watermark.size
        
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        alpha2 = ImageEnhance.Brightness(alpha).enhance(opacity2)
        watermark.putalpha(alpha)
        watermark2 = watermark.copy()
        watermark2.putalpha(alpha2)
        watermark2.thumbnail((wat_w/3, wat_h/3), Image.ANTIALIAS)
        wat_w2, wat_h2 = watermark2.size
        
    layer = Image.new('RGBA', image.size, (0,0,0,0))
    y = img_h - wat_h*2
    layer.paste(watermark, (0, y))
    y2 = wat_h
    for x in range(0, img_w, wat_w2):
        layer.paste(watermark2, (x, y2))
                
    return Image.composite(layer,  image,  layer)

def to_webp(path, name):
    '''Конвертация картинки в формат WebP'''

    dirname = os.path.dirname(path)
    newpath = os.path.join(dirname, 'tmp.webp')
    
    dirname = os.path.dirname(name)
    newname = os.path.join(dirname, 'tmp.webp')
    
    img = Image.open(path)
    img.save(newpath, "WEBP", quality=90)
    os.remove(path)
    return newname