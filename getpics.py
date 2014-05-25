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



visited = set()
pic_number = 1

def URL_dfs(link):
    hash = getDoubleHash(link)
    if(hash in visited):
        return

    visited.add(hash)
    print link

    suffix = isPicture(link)
    if(suffix != ""):
        global pic_number
        urllib.urlretrieve(link, "./pics/" + str(pic_number) + suffix)
        pic_number += 1
        return

    try:
        htmlPage = urllib2.urlopen(link)
    except urllib2.HTTPError:
        return

    try:
        soup = BeautifulSoup(htmlPage)
    except HTMLParseError:
        return

    for pageLink in soup.findAll('a'):
        if(pageLink.has_attr("href")):
            toGo = pageLink["href"]
            if(toGo[0] == '/'):
                URL_dfs(site + normalize(toGo))



def isPicture(link):
    suff = [".jpg", ".png", ".gif"]

    for i in range(0, len(suff)):
        if(link[-len(suff[i]):] == suff[i]):
            return suff[i];
    return "";



site = sys.argv[1]
#folderToSave = sys.argv[2]

URL_dfs(site)
