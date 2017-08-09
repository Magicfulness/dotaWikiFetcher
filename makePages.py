import urllib.request
import json
import os
import datetime
import re

def getWikitext(title):
    wikiPage, headers = urllib.request.urlretrieve(
        "https://dota2.gamepedia.com/api.php?action=query&titles=%s&indexpageids=&prop=revisions&rvprop=content&format=json" % title)
    pageData = json.load(open(wikiPage))
    #pageData is the actual json, I get the wikitext parse it into a more readable format
    pageID = str(pageData['query']['pageids'][0]) #hopefully only one everytime
    
    return pageData['query']['pages'][pageID]['revisions'][0]['*']
	
def makeList(category, name): 
    heroListRaw, headers = urllib.request.urlretrieve(
        "https://dota2.gamepedia.com/api.php?action=query&titles=%s&indexpageids=&prop=revisions&rvprop=content&format=json" % title)
    heroes = re.compile("\\{\\{" + matchBy + "\\|(.*)\\|")
    
    heroList = {}
    hero = heroes.search(heroListRaw)
    while hero:
        heroList[hero.group(1)] = True
        heroListRaw = heroListRaw[hero.end():]
        hero = heroes.search(heroListRaw)
    heroListFile = open("%sList.json" % matchBy, 'w')
    heroListFile.write(json.dumps(heroList))
    heroListFile.close()
    print(len(heroList))
	

def makeHero(inputHero):
    try:
        os.makedirs("heroes")
    except OSError:
        pass
        
    heroWikiPageL = open("heroes/"+inputHero+".wikitext", 'w')

    heroWikiPageL.write(getWikitext(inputHero))
    heroWikiPageL.write("\n\n==Self Tags==\n| DateLastMod = %s" % datetime.datetime.today())

    heroWikiPageL.close()
    
def makeItem(inputHero):
    try:
        os.makedirs("heroes")
    except OSError:
        pass


def findFile():
    pass
