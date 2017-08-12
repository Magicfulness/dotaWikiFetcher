import makePages as mP
import re
import json

def makeRe():
    #sect and start group(1) give the group's name, var.group(1) = var.group(2)
    return {"sect": re.compile("==\s(.*)\s=="), "start": re.compile("\\{\\{(.*)\n"), "var": re.compile("\\| (.*) = (.*)"), "end": re.compile("\n\\}\\}") }
    
def parse(inputStr):
    regex = makeRe()
    
 #   with open(fileLoc, 'r') as wikiText:
  #      raw = wikiText.read()
    
    raw = mP.getWikitext(inputStr)[0]
    pageInfo = {}
    #parse header first
    pageInfo["header"] = parseVals(getPart(raw, regex["sect"])[0], regex["var"])
    #rest of page
    #while raw:
        #regex["sect"].search(raw)
        #section = getPart(raw, regex["end"], regex["start"])
        #vals = parseVals(section, varRe)
    
    with open(inputStr, 'w') as listFile:
        listFile.write(json.dumps(pageInfo))
    print(pageInfo)
    return None
    
def getPart(raw, endRe, startRe=re.compile("")):
    startSect = startRe.search(raw).end()
    endSect = endRe.search(raw[startSect:]).start() + startSect
    return raw[startSect : endSect], endSect
    
def parseVals(section, varRe):
    vals = {}
    while section:
        val = varRe.search(section)
        if not val:
            break
        vals[val.group(1)] = val.group(2)
        section = section[val.end():]
    return vals    
#try:
#    os.makedirs(cat)
#except OSError:
#    pass
    
    
    
