import urllib.request as request
import re
import os
from PIL import Image
import shutil

pages = [
    'https://commons.wikimedia.org/w/index.php?title=Category:SVG_rowing_blades&fileuntil=University+of+West+England+Boat+Club+Rowing+Blade.svg#mw-category-media',
    'https://commons.wikimedia.org/w/index.php?title=Category:SVG_rowing_blades&filefrom=University+of+West+England+Boat+Club+Rowing+Blade.svg#mw-category-media']


def getlinks(url):
    return ['https://upload.wikimedia.org/wikipedia/commons/' + x[:-6:] for x in
            re.findall('thumb/[a-zA-Z0-9]/[a-zA-Z0-9]+/.*/120px', request.urlopen(url).read().decode("utf-8"))]


def trim(im):
    return im.crop(im.getbbox())


def crop(im):
    return im.crop([420, 0, im.size[0], im.size[1]])


links = []
for page in pages:
    links += getlinks(page)

if not os.path.exists('temp'):
    os.mkdir('temp')
if not os.path.exists('images'):
    os.mkdir('images')
for link in links:
    print('Downloading ' + link[58:-4:])
    request.urlretrieve(link + '/2000px-' + link[58::] + '.png', 'temp/' + link[58:-4:] + '.png')
    print('Processing ' + link[58:-4:])
    im = Image.open('temp/' + link[58:-4:] + '.png')
    im = crop(trim(im))
    im.thumbnail([16, 11], Image.ANTIALIAS)
    im2 = Image.new("RGBA", [16, 11])
    im2.paste(im, [0, 1, im.size[0], 1 + im.size[1]])
    im2.save('images/' + link[58:-4:] + '.png')
    print('Processed ' + link[58:-4:])
print('Removing temp files')
shutil.rmtree('temp')
print('Done!')