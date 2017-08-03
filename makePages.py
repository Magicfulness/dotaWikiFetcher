 
import urllib.request
import json
import os

def makeHero(inputHero):
    try:
        os.makedirs("heroes")
    except OSError:
        pass
        
    heroWikiPageL = open("heroes/"+inputHero+".wikitext", 'w')

    heroWikiPageO, headers = urllib.request.urlretrieve(
		"https://dota2.gamepedia.com/api.php?action=query&titles=%s&indexpageids=&prop=revisions&rvprop=content&format=json" % inputHero)

    heroData = json.load(open(heroWikiPageO))
    #heroDats is the actual json, I get the wikitext parse it into a more readable format
    pageID = str(heroData['query']['pageids'][0]) #hopefully only one everytime
    
    heroWikiPageL.write(heroData['query']['pages'][pageID]['revisions'][0]['*'])
    heroWikiPageL.write("\n==Self Tags== DATELASTMOD=%s" % 'today') #get datetime stuff

    heroWikiPageL.close()
    
def makeItem(inputHero):
    try:
        os.makedirs("heroes")
    except OSError:
        pass


def findFile():
    pass
