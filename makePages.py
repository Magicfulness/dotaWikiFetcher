import urllib.request
import json
import os
import datetime
import re

def getWikitext(title):
    reformedTitle = re.compile("\s").sub('_', title)
    wikiPage, headers = urllib.request.urlretrieve(
        "https://dota2.gamepedia.com/api.php?action=query&titles=%s&indexpageids=&prop=revisions&rvprop=content&format=json" % reformedTitle)
    pageData = json.load(open(wikiPage))
    #pageData is the actual json, I get the wikitext parse it into a more readable format
    pageID = str(pageData['query']['pageids'][0]) #hopefully only one everytime
    
    return pageData['query']['pages'][pageID]['revisions'][0]['*']
	
def makeList(category, name): 
    raw, headers = urllib.request.urlretrieve(
        "https://dota2.gamepedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:%s&cmlimit=500&format=json" % category)
    with open(raw) as cat:
        catData = json.load(cat)
    memberList = {}
    for member in catData['query']['categorymembers']:
        memberList[member['title']] = True
    with open("%sList.json" % name, 'w') as listFile:
        listFile.write(json.dumps(memberList))
    
def makePage(inputStr):
    if not os.path.exists("heroList.json"):
        makeList("Heroes", "hero")
    if not os.path.exists("itemList.json"):
        makeList("Items", "item")
        
    with open("heroList.json") as heroJson:
        heroList = json.load(heroJson)
    with open("itemList.json") as itemJson:
        itemList = json.load(itemJson)
        
    if inputStr in heroList:
        cat = "heroes"
    elif inputStr in itemList:
        cat = "items"
    else:
        cat = None
    
    if cat:
        try:
            os.makedirs(cat)
        except OSError:
            pass
        with open("%s/%s.wikitext" % (cat, inputStr), 'w') as savedPage:
            savedPage.write(getWikitext(inputStr))
            savedPage.write("\n\n==Self Tags==\n| DateLastMod = %s" % datetime.datetime.today())
    else:
        print("Failure")
