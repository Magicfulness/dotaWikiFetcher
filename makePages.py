import urllib.request
import json
import re

"""
This file is basically most of the backend-ish stuff that fetches from the wiki and makes the json files
You should never have to use any of these functions, instead look at utils.py
"""

# gets string from wiki in wikitext format
def getWikitext(title):
    reformedTitle = re.compile("\s").sub('_', title)
    wikiPage, headers = urllib.request.urlretrieve(
        "https://dota2.gamepedia.com/api.php?action=query&titles=%s&indexpageids=&prop=revisions&rvprop=content|timestamp&format=json" % reformedTitle)
    with open(wikiPage) as openedPage:
        pageData = json.load(openedPage)
    #pageData is the actual json, I get the wikitext parse it into a more readable format
    pageID = str(pageData['query']['pageids'][0]) #hopefully only one everytime
    
    #returns wikitext and date of last revision
    return pageData['query']['pages'][pageID]['revisions'][0]['*'], pageData['query']['pages'][pageID]['revisions'][0]['timestamp']
	
# Makes a dictionary of all heroes and items
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

# Parses wikitext format into a json using complicated re    
def parseWikitext(inputStr):
    #sect and start group(1) give the group's name, var.group(1) = var.group(2)
    regex = {"sect": re.compile("==\s(.*)\s=="), "start": re.compile("\\{\\{(.*)\n"), "var": re.compile("\\| (.*) = (.*)"), "end": re.compile("\n\\}\\}") }
    raw = getWikitext(inputStr)[0]
    pageInfo = {}

    # This function gets a "Part" using the given re as start and end markers
    # Returns a tuple consisting of "part, a number indicating the end of the part, and one indicating the start
    def getPart(raw, endRe, startRe=re.compile("")):
        #print(raw)
        if type(raw) is not str:
            return None, None, None
        
        start = startRe.search(raw)
        if not start:
            return None, None, None
        startSect = start.end()
        end = endRe.search(raw[startSect:])
        if not end:
            return None, None, None
        endSect = end.start() + startSect
        return raw[startSect : endSect], endSect, start
    
    # This function parses an entire section for "val" pairs and returns a dictionary of these pairs
    def parseVals(section, varRe):
        vals = {}
        while section:
            val = varRe.search(section)
            if not val:
                break
            vals[val.group(1)] = val.group(2)
            section = section[val.end():]
        return vals    

    #parse header first
    pageInfo["header"] = parseVals(getPart(raw, regex["sect"])[0], regex["var"])

    #rest of page
    while True:
        #get a section
        head, endHead, headMatch = getPart(raw, regex["sect"], regex["sect"])
        if not head:
            break
        valList = []
        
        while True:
            #get subsections
            section, endSection, sectionMatch = getPart(head, regex["end"], regex["start"])
            if not section:
                break
            valList.append(parseVals(section, regex["var"]))
            head = head[endSection:]
            
        if headMatch:
            pageInfo[headMatch.group(1)] = valList
            raw = raw[endHead:]
        
    #print(pageInfo)
    #print(pageInfo["Abilities"])
    return pageInfo
    

#try:
#    os.makedirs(cat)
#except OSError:
#    pass

