import urllib.request
import json
import os
import datetime
import re

def getWikitext(title):
    reformedTitle = re.compile("\s").sub('_', title)
    wikiPage, headers = urllib.request.urlretrieve(
        "https://dota2.gamepedia.com/api.php?action=query&titles=%s&indexpageids=&prop=revisions&rvprop=content|timestamp&format=json" % reformedTitle)
    pageData = json.load(open(wikiPage))
    #pageData is the actual json, I get the wikitext parse it into a more readable format
    pageID = str(pageData['query']['pageids'][0]) #hopefully only one everytime
    
    #returns wikitext and date of last revision
    return pageData['query']['pages'][pageID]['revisions'][0]['*'], pageData['query']['pages'][pageID]['revisions'][0]['timestamp']
	
def makeList():
    cats = ["Heroes", "Items"]
    catList = {}
    for category in cats:
        catList[category] = {}
        raw, headers = urllib.request.urlretrieve(
	    "https://dota2.gamepedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:%s&cmlimit=500&format=json" % category)
        with open(raw) as cat:
            catData = json.load(cat)
        for member in catData['query']['categorymembers']:
            catList[category][member['title']] = True
    with open("list.json", 'w') as listFile:
        listFile.write(json.dumps(catList))

def getCat(inputStr):
    #ensure list exists & load it
    if not os.path.exists("list.json"):
        makeList()
    with open("list.json") as listLoc:
        listcat = json.load(listLoc)
    
    #return which category input is
    for cat in listcat:
        if inputStr in listcat[cat]:
            return cat
    return None
        
def makeJson(fileLoc, cat, inputStr):
    try:
        os.makedirs(cat)
    except OSError:
        pass
    with open(fileLoc, 'w') as savedPage:
        #TODO handle errors and try to minimize calls
        wikiText = getWikitext(inputStr)
        savedPage.write(wikiText[0])
        savedPage.write("\n\n==Self Tags==\n| lastRevDate = %s" % wikiText[1])

def getPage(inputStr):
    cat = getCat(inputStr)
    if not cat:
        print("failure")
        return None
        
    fileLoc = "%s/%s.json" % (cat, inputStr)
    if not os.path.exists(fileLoc):
        makePage(fileLoc, cat, inputStr)
    return fileLoc
