import shutil
from PIL import Image
from urllib import parse, request
from bs4 import BeautifulSoup
import os
import glob


def downloadimages(url, level, minfilesize):
    global website
    netloc = parse.urlsplit(url).netloc.split('.')
    if netloc[-2] + netloc[-1] != website:
        return

    global urlList
    if url in urlList:
        return

    try:
        urlcontent = request.urlopen(url).read().decode('latin-1')
        urlList.append(url)
        print(url)
    except:
        return

    soup = BeautifulSoup(''.join(urlcontent))
    imgtags = soup.findAll('img')
    for imgTag in imgtags:
        imgurl = imgTag['src']
        if imgurl.lower().endswith('.png'):
            try:
                request.urlretrieve(parse.urljoin(url, imgurl), 'temp/' + os.path.basename(parse.urlsplit(imgurl)[2]))
            except:
                pass

    if level > 0:
        linktags = soup.findAll('a')
        if len(linktags) > 0:
            for linkTag in linktags:
                try:
                    linkurl = linkTag['href']
                    downloadimages(linkurl, level - 1, minfilesize)
                except:
                    pass


def trim(im):
    return im.crop(im.getbbox())


def crop(im):
    return im.crop([355, 0, im.size[0], im.size[1]])


if not os.path.exists('temp'):
    os.mkdir('temp')
if not os.path.exists('images'):
    os.mkdir('images')

urlList = []
rootUrl = 'http://www.oarspotter.com'
netloc = parse.urlsplit(rootUrl).netloc.split('.')
website = netloc[-2] + netloc[-1]

print('Scraping OarSpotter')
downloadimages(rootUrl, 2, 0)
print('Finished scraping OarSpotter')

print('Resizing images')
os.chdir('temp')
for file in glob.glob("*.png"):
    im = Image.open(file)
    if im.size != (436, 48):
        continue
    im = crop(trim(im))
    im.thumbnail([20, 11], Image.BICUBIC)
    im2 = Image.new("RGBA", [20, 11])
    im2.paste(im, [0, 1, im.size[0], 1 + im.size[1]])
    im2.save('../images/' + file[:-4:] + '.png')
    print('Resized ' + file[:-4:])
print('Removing temp files')
os.chdir('..')
shutil.rmtree('temp')
print('Done!')


