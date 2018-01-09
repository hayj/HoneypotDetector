# coding: utf-8

# pew in honeypotdetector-venv python /home/hayj/Drive/Workspace/Python/Crawling/HoneypotDetector/honeypotdetector/honeypot.py


from systemtools.logger import *
from datatools.url import *
from systemtools.basics import *
from webcrawler.browser import *
from webcrawler.utils import *
import re
from lxml import etree
from io import StringIO, BytesIO
from sklearn import tree
import urllib.request
# from threading import Lock
import multiprocessing



# Data from honeypot.php
# isBigEnough, hasBigEnoughChild, hasText, isDisplayed, hasDisplayedChild, hasTextPlusNodeRecursive
data = \
[
    [True, False, True, True, True, True],
    [True, False, True, True, True, False],
    [True, False, True, True, True, True],
    [True, False, True, True, True, False],
    [False, False, True, True, False, False],
    [False, False, False, True, False, False],
    [True, True, False, True, True, False],
    [False, False, False, False, False, False],
    [True, False, True, True, False, False],
    [True, False, True, True, False, False],
    [True, False, False, False, False, False],
    [True, False, True, True, False, False],
    [True, False, False, True, True, False],
    [False, False, False, False, False, False],
    [False, False, False, False, False, False],
    [True, False, True, True, False, False],
    [True, False, False, False, False, False],
    [False, False, False, False, False, False],
    [True, False, False, False, False, False],
    [True, False, False, False, False, False],
    [False, False, False, False, False, False],
]

# isHoneypot
labels = [False, True, False, True, True, True, False,
          True, False, False, True, False, True, True,
          True, False, True, True, True, True, True]

def generateDecisionTree():
    X = [[0, 0], [1, 1]]
    Y = [0, 1]
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(data, labels)
    return clf


def isBigEnough(element, minSurface=6):
    surface = element.size["height"] * element.size["width"]
    if surface > minSurface:
        return True
    return False


def hasBigEnoughChild(element, minSurface=6):
    for current in element.find_elements_by_css_selector("*"):
        if isBigEnough(current, minSurface=minSurface):
            return True
        else:
            return isBigEnough(current)
    return False

def hasText(element):
    text = element.text
    if text is None:
        return False
    else:
        text = text.strip()
        return len(text) > 0


def hasTextPlusNodeRecursive(element):
    if not isinstance(element, etree._Element):
        element = element.get_attribute("outerHTML")
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(element), parser)
        element = tree.find("//body/*")
    if hasTextPlusNode(element):
        return True
    children = list(element)
    if children is None:
        return False
    else:
        for current in children:
            if hasTextPlusNodeRecursive(current):
                return True
    return False

def hasTextPlusNode(element):
    if element is None:
        return False
    text = getElementText(element)
    if text is None:
        return False
    if len(list(element)) > 0 and len(text) > 0:
        return True
    return False

def getElementText(element):
    text = ""
    if element.text is not None:
        text += element.text.strip()
    for current in list(element):
        if current.tail is not None:
            text += " " + current.tail.strip()
    return text.strip()



def isDisplayed(element):
    return element.is_displayed()

def hasDisplayedChild(element):
    for current in element.find_elements_by_css_selector("*"):
        if isDisplayed(current):
            return True
        else:
            return hasDisplayedChild(current)
    return False





def getHoneypotFeatures(link):
    currentX = []
    try:
        currentX.append(isBigEnough(link))
        currentX.append(hasBigEnoughChild(link))
        currentX.append(hasText(link))
        currentX.append(isDisplayed(link))
        currentX.append(hasDisplayedChild(link))
        currentX.append(hasTextPlusNodeRecursive(link))
        return currentX
    except:
        return [True, False, True, True, False, False]


# # Expérimental :
clf = None
urlParser = URLParser()
def isHoneypot(self, link):
    try:
        theArray = clf.predict([getHoneypotFeatures(link)])
        return theArray[0]
    except:
        return False

def parseLinks(data):
    global urlParser
    global clf
    (link, domain) = data
    isHoneypot = None
    linkType = None
    href = None
    try:
        href = link.get_attribute("href")
        if href is None or href.strip() == "" or href.strip() == "#":
            linkType = LINK_TYPE.dead
        elif domain is not None and "http" in href and urlParser.getDomain(href) != domain:
            linkType = LINK_TYPE.external
        else:
            linkType = LINK_TYPE.internal
        if isHoneypot(link):
            isHoneypot = True
        else:
            isHoneypot = False
    except Exception as e:
        pass # logException(e, self, location="honeypot parseLinks")
    return (href, isHoneypot, linkType)


LINK_TYPE = Enum("LINK_TYPE", "dead external internal")
class HoneypotDetector():
    def __init__(self, logger=None, verbose=True):
        self.logger = logger
        self.verbose = verbose
        self.clf = generateDecisionTree()
        self.urlParser = URLParser()

    def isHoneypot(self, link):
        try:
            theArray = self.clf.predict([getHoneypotFeatures(link)])
            return theArray[0]
        except:
            return False

    def getLinks(self, driver, domainOrUrl=None, removeExternal=False):

        domain = None
        if domainOrUrl is not None:
            if "http" in domainOrUrl:
                domain = self.urlParser.getDomain(domainOrUrl)
            else:
                domain = domainOrUrl


        links = driver.find_elements_by_css_selector("a")
        for i in range(len(links)):
            links[i] = (links[i], domain)
        global clf
        if clf is None:
            clf = generateDecisionTree()



        pool = Pool(mapType=MAP_TYPE.spark) # best choice is parmap here
        tt = TicToc()
        tt.tic()
        labels = list(pool.map(links, parseLinks))
        tt.toc()

        safeLinks = []
        for (href, isHoneypot, linkType) in labels:
            if linkType != LINK_TYPE.dead:
                if not removeExternal or (removeExternal and linkType != LINK_TYPE.external):
                    if not isHoneypot:
                        safeLinks.append(href)
        honeypotLinks = []
        for (href, isHoneypot, linkType) in labels:
            if linkType != LINK_TYPE.dead:
                if not removeExternal or (removeExternal and linkType != LINK_TYPE.external):
                    if isHoneypot and href not in safeLinks:
                        honeypotLinks.append(href)

        return (list(set(safeLinks)), list(set(honeypotLinks)))

if __name__ == '__main__':

    print("Start")


#     url = "http://localhost/testajax/honeypot.php"
#     url = "https://www.google.com/search?q=wikipedia"
#     url = "https://www.google.fr/search?q=pytho+list+prepend"
    url = "https://www.lequipe.fr/Football/Actualites/Nice-pas-la-meme-histoire/845443"
    url = "https://stackoverflow.com/questions/38060738/python-copy-element"


    b = Browser(ajaxSleep=1.0, proxy=getRandomProxy())
    b.get(url)


#     printLTS(b.html(url))
#     page = urllib.request.urlopen(url)
#     strToFile(byteToStr(page.read()), rootPath + "/tmp/" + "no-js-no-comments" + ".html")
#     print(page)



    honeypotDetector = HoneypotDetector()
    (safeLinks, honeypotLinks) = honeypotDetector.getLinks(b.driver)
    printLTS(list(safeLinks))
    printLTS(list(honeypotLinks))











