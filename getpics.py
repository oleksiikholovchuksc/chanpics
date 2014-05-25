from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import urllib
import urllib2
import hashlib
import sys
import os



def getDoubleHash(str):
    P = [31, 137]
    mult = [1, 1]
    M = [1 << 64, 1000000007]
    hash = [0, 0]

    for c in str:
        for i in range(0, 2):
            hash[i] += ord(c) * mult[i]
            hash[i] %= M[i]
            mult[i] *= P[i]

    return (hash[0], hash[1])



def normalize(link):
    for i in range(0, len(link)):
        if(link[i] == '#'):
            return link[:i]

    return link



def formPath(link, baseFolder):
    splitted = link.split('/')
    chanFolder = baseFolder + splitted[2]
    if(not os.path.exists(chanFolder)):
        os.makedirs(chanFolder)

    boardFolder = chanFolder + '/' + splitted[3] + '/'
    if(not os.path.exists(boardFolder)):
        os.makedirs(boardFolder)

    return boardFolder



Q = []
visited = set()

def traverse(link, folder):
    Q.append(link)
    visited.add(getDoubleHash(link))

    while(len(Q) > 0):
        link = Q[-1]
        Q.pop()

        print link
        try:
            htmlPage = urllib2.urlopen(link)
        except urllib2.HTTPError:
            continue

        try:
            soup = BeautifulSoup(htmlPage)
        except HTMLParseError:
            continue

        for pageLink in soup.findAll('a'):
            if(pageLink.has_attr('href')):
                newLink = pageLink['href']
                
                if(newLink[0] != '/'):
                    continue

                newLink = site + normalize(newLink)
                hash = getDoubleHash(newLink)
                if(hash in visited):
                    continue
                else:
                    visited.add(hash)

                ext = newLink.split('.')[-1]
                picExtensions = ["jpg", "jpeg", "png", "gif"]
                if(ext in picExtensions):
                    pathToSave = formPath(newLink, folder)
                    tempPath = pathToSave + "temp"
                    urllib.urlretrieve(newLink, tempPath)
                    picMd5 = hashlib.md5()
                    picMd5.update(open(tempPath, "r").read())
                    picHash = picMd5.hexdigest()
                    os.rename(tempPath, pathToSave + picHash + "." + ext)
                    continue
                
                docExtensions = ["html", "xml"]
                if(ext in docExtensions or newLink[-1] == '/'):
                    Q.insert(0, newLink)



site = sys.argv[1]
folderToSave = sys.argv[2]

traverse(site, folderToSave)
