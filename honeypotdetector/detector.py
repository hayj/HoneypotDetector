# coding: utf-8

# pew in honeypotdetector-venv python /home/hayj/Drive/Workspace/Python/Crawling/HoneypotDetector/honeypotdetector/detector.py


from systemtools.logger import *
from datatools.url import *
from datastructuretools.processing import *
from datastructuretools.hashmap import *
from systemtools.basics import *
import re
from lxml import etree
from io import StringIO, BytesIO
from sklearn import tree
# import urllib.request
# from threading import Lock
# import multiprocessing



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






LINK_TYPE = Enum("LINK_TYPE", "dead external internal")
class HoneypotDetector():
    def __init__(self, logger=None, verbose=True):
        self.logger = logger
        self.verbose = verbose
        self.clf = generateDecisionTree()
        self.urlParser = URLParser()
        self.featureCache = SerializableDict(funct=self.getHoneypotFeatures, limit=1000)

    def getHref(self, link):
        href = link.get_attribute("href")
        return self.urlParser.normalize(href)

    def isHoneypot(self, linkOrHref, driver=None):
        if isinstance(linkOrHref, str):
            href = self.urlParser.normalize(linkOrHref)
            links = driver.find_elements_by_css_selector("a")
            hrefs = list(map(self.getHref, links))
            hrefIndexes = []
            for i in range(len(hrefs)):
                currentHref = hrefs[i]
                if currentHref == href:
                    hrefIndexes.append(i)
            if len(hrefIndexes) == 0:
                return False
            for index in hrefIndexes:
                link = links[index]
                if not self.isHoneypot(link):
                    return False
            return True
        else:
            link = linkOrHref
            try:
                # theArray = self.clf.predict([self.featureCache[link]])
                theArray = self.clf.predict([self.getHoneypotFeatures(link)])
                return theArray[0]
            except:
                return False

    def getHoneypotFeatures(self, link):
        currentX = []
        try:
            currentX.append(isBigEnough(link))
            currentX.append(hasBigEnoughChild(link))
            currentX.append(hasText(link))
            currentX.append(isDisplayed(link))
            currentX.append(hasDisplayedChild(link))
            currentX.append(hasTextPlusNodeRecursive(link))
            return currentX
        except Exception as e :
            logException(e, self, location="getHoneypotFeatures")
            return [True, False, True, True, False, False]


    def getType(self, href, driver=None, domainOrUrl=None):
        domain = None
        if domainOrUrl is not None:
            if "http" in domainOrUrl:
                domain = self.urlParser.getDomain(domainOrUrl)
            else:
                domain = domainOrUrl
        elif driver is not None:
            domain = self.urlParser.getDomain(driver.current_url)
        linkType = None
        if href is None or href.strip() == "" or href.strip() == "#":
            linkType = LINK_TYPE.dead
        elif domain is not None and "http" in href and self.urlParser.getDomain(href) != domain:
            linkType = LINK_TYPE.external
        else:
            linkType = LINK_TYPE.internal
        return linkType

    def parseLink(self, link, domainOrUrl=None, driver=None):
        thisIsAHoneypot = None
        linkType = None
        href = None
        try:
            href = self.getHref(link)
            linkType = self.getType(href, domainOrUrl=domainOrUrl, driver=driver)
            thisIsAHoneypot = self.isHoneypot(link)
        except Exception as e:
            logException(e, self, location="honeypot parseLink")
        return (link, href, thisIsAHoneypot, linkType)


    def getLinks(self, *args, **kwargs):
        kwargs["returnHref"] = False
        return self.getHrefs(*args, **kwargs)

    def getHrefs(self, driver, domainOrUrl=None, removeExternal=False, cssSelectorHead="", returnHref=True):
        if len(cssSelectorHead) > 0 and cssSelectorHead[-1] != " ":
            cssSelectorHead = cssSelectorHead + " "
        links = driver.find_elements_by_css_selector(cssSelectorHead + "a")

        labels = []
        for link in links:
            labels.append(self.parseLink(link, domainOrUrl=domainOrUrl, driver=driver))

#         pool = Pool(mapType=MAP_TYPE.builtin)
#         labels = list(pool.map(links, self.parseLink))

        safeLinks = []
        for (link, href, thisIsAHoneypot, linkType) in labels:
            if linkType != LINK_TYPE.dead:
                if not removeExternal or (removeExternal and linkType != LINK_TYPE.external):
                    if not thisIsAHoneypot:
                        if returnHref:
                            safeLinks.append(href)
                        else:
                            safeLinks.append(link)
        honeypotLinks = []
        for (link, href, thisIsAHoneypot, linkType) in labels:
            if linkType != LINK_TYPE.dead:
                if not removeExternal or (removeExternal and linkType != LINK_TYPE.external):
                    if thisIsAHoneypot and href not in safeLinks:
                        if returnHref:
                            honeypotLinks.append(href)
                        else:
                            honeypotLinks.append(link)

        return (list(set(safeLinks)), list(set(honeypotLinks)))













