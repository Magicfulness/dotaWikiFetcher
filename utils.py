import makePages as mP
import json
import os

"""
This file serves as a way to access makePages functions more simply. 

It should handle all file updates and stuff.

"""

# Loads inputStr's json as a dictionary.
def getPage(inputStr):
    cat = getCat(inputStr)
    if not cat:
        print("failure")
        return None
        
    fileLoc = "%s/%s.json" % (cat, inputStr)
    if not os.path.exists(fileLoc):
        makeJson(inputStr)
    with open(fileLoc) as infoJson:
        return json.load(infoJson)

# Returns whether inputStr is a hero or item or neither (i.e. "Axe" is a hero). Neither returns None.
def getCat(inputStr):
    #ensure list exists & load it
    if not os.path.exists("list.json"):
        mP.makeList()
    with open("list.json") as listLoc:
        listcat = json.load(listLoc)
    
    #return which category input is
    for cat in listcat:
        if inputStr in listcat[cat]:
            return cat
    return None


# Given an inputStr, makes a json file under the corresponding folder
def makeJson(inputStr):
    cat = getCat(inputStr)
    if not cat:
        print("failure")
        return None
    fileLoc = "%s/%s.json" % (cat, inputStr)

    try:
        os.makedirs(cat)
    except OSError:
        pass
    with open(fileLoc, 'w') as savedPage:
        #TODO: handle errors and try to minimize calls
        print("DOPE " + inputStr)
        wikiText = mP.parseWikitext(inputStr)
        savedPage.write(json.dumps(wikiText))
        #savedPage.write("\n\n==Self Tags==\n| lastRevDate = %s" % wikiText[1])

    # Usually should be treated as void, but if you want it returns cat and fileLoc of inputStr
    return cat, fileLoc

# TODO: don't make useless category files (probably use a re on heroOrItem)
# Reloads all hero files and make a new list.json
def refresh():
    mP.makeList()
    with open("list.json") as listLoc:
        listcat = json.load(listLoc)
    for cat in listcat:
        for heroOrItem in listcat[cat]:
            makeJson(heroOrItem)
    return True    


