import requests
import urllib2
import zlib
import codecs


def splitPathAndFileName(url):
    page_path = '(none)'
    page_name = '(none)'
    i = len(url)-1
    
    while i >= 0:
        if url[i] == '/':
            page_name = url[i+1:]
            page_path = url[:i+1]
            break
        
        i = i-1

    return page_path, page_name

def saveFile(path, file_name):
    r = requests.get(path + file_name)

    with open(file_name, "wb") as code:
        code.write(r.content)

def readHTMLCode(url):
    request = urllib2.Request(url)
    request.add_header('Accept-Encoding', 'gzip')
    response = urllib2.urlopen(request)
    data = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)

    return data

def loadHTMLAndImage(url):

    page_path, page_name = splitPathAndFileName(url)
    saveFile(page_path, page_name)

    data = readHTMLCode(url)

    i = 0
    
    while i < len(data):
        if data[i:i+4] == '<img':
            a = i+4
            
            while data[a] != '>':
                a = a+1

            img_tag = data[i:a+1]

            b = img_tag.index('src')

            while img_tag[b] != '"' and img_tag[b] != "'":
                b = b+1

            c = b+1

            while img_tag[c] != '"' and img_tag[c] != "'":
                c = c+1

            img_file = img_tag[b+1:c]

            if img_file[:7] != 'http://':
                saveFile(page_path, img_file)

            i = a

        i = i+1

print 'Welcome to 2017 CN Assignment #2 !!'

while True:
    url = raw_input('Enter URL: ')

    if url == '.':
        break

    loadHTMLAndImage(url)

print 'See you next time~'
