from django.conf import settings
from PIL import Image, ImageEnhance
import os

import time

def get_box_thumb(image, TIS):
    """
    image - объект картинка, на которую накладываете изображение
    TIS - THUMB_IMAGE_SIZE (50, 50)

    """
    st = time.time()
    img_w, img_h = image.size
    min_size = min(img_w, img_h)
    left = int((img_w-min_size)/2)
    upper = int((img_h-min_size)/2)
    box = (left, upper, left+min_size, upper+min_size)
    image = image.crop(box)
    image.thumbnail(TIS, resample=Image.LANCZOS)
    print('get_box_thumb {}'.format(time.time()-st))
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


def add_watermark(image, watermark_path=settings.WATERMARK_PATH, opacity=0.6, opacity2=0.7):
    """
    image - объект картинка, на которую накладываете изображение
    watermark - картинка, которую накладываете
    opacity - прозрачность

    """
    st = time.time()
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
        alpha2 = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        alpha2 = ImageEnhance.Brightness(alpha2).enhance(opacity2)
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
    print('add_watermark {}'.format(time.time()-st))
    return Image.composite(layer,  image,  layer)

def to_webp(path, name):
    '''Конвертация картинки в формат WebP'''

    st = time.time()

    dirname = os.path.dirname(path)
    newpath = os.path.join(dirname, 'tmp.webp')
    
    dirname = os.path.dirname(name)
    newname = os.path.join(dirname, 'tmp.webp')
    
    img = Image.open(path)
    img.save(newpath, "WEBP", quality=90)
    os.remove(path)

    print('to_webp {}_{}'.format(time.time()-st, path))

    return newname

def get_jpg_path(path, folder='JPG'):
    '''Получить путь к файлу в формате JPG'''

    dir, filename = os.path.split(path)
    newdir = os.path.join(dir, folder)
    name, ext = os.path.splitext(filename)
    newfilename = '{0}.{1}'.format(name, 'jpg')
    newpath = os.path.join(newdir, newfilename)

    return newpath

def to_jpg(path, folder='JPG'):
    '''Сохранение картинки в формате jpg в указанную папку'''

    st = time.time()

    dir, filename = os.path.split(path)
    newdir = os.path.join(dir, folder)
    if not os.path.exists(newdir):
        os.mkdir(newdir)

    newpath = get_jpg_path(path, folder)
    img = Image.open(path)
    if img.mode == 'RGBA':
        background = Image.new('RGBA', img.size, (242,242,242))
        img = Image.alpha_composite(background, img)
        img = img.convert('RGB')
    img.save(newpath, quality=100)

    print('to_jpg {}_{}'.format(time.time()-st, path))

    return newpath
