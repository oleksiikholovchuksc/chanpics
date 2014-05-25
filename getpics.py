from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import urllib
import urllib2
import sys



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



def isPicture(link):
    suff = [".jpg", ".png", ".gif"]

    for i in range(0, len(suff)):
        if(link[-len(suff[i]):] == suff[i]):
            return suff[i]
    return ""



Q = []
visited = set()
pic_number = 1

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

                suffix = isPicture(newLink)
                if(suffix != ""):
                    global pic_number
                    urllib.urlretrieve(newLink, folder + str(pic_number) + suffix)
                    pic_number += 1
                    continue

                Q.insert(0, newLink)
            



site = sys.argv[1]
folderToSave = sys.argv[2]

traverse(site, folderToSave)
