import makePages as mP
import re
import parseQuery
import utils

def testmP():
    inputHero = input("Give me input: ")
    mP.getPage(inputHero)

def testParse1():
    fileLoc = mP.parseWikitext("Axe")
    query = "Ability"
    start = re.compile("\\{\\{%s" % query)
    var = re.compile("\\|(\\w*) = (.*)")
    end = re.compile("\\}\\}")
    with open(fileLoc, 'r') as savedPage:
        for line in savedPage:
            if p1.match(line):
                print(p1.match(line))
        #a = a[p1.search(a).end():]
        
def testParse2():
    e = "H?ello"
    p = re.compile("\w*")
    #print(p.match(e).group())
    print(mP.makeList("Heroes", "Hero"))

def testParseWT():
    axe = mW.parse("Axe")
    q = axe["Abilities"][1]
    for info in q:
        print(info)
        print("  " + str(q[info]))

def testParseQuery():
    q = axe["Abilities"][1]
    for info in q:
        print(info)
        print("  " + str(q[info]))

def testRefresh():
    utils.refresh()

def testGetPage():
    axe = utils.getPage("Axe")
    print(axe)

#testmP()
#testParseWT()
#print(mP.ensureExist("Axe"))
#testParseQuery()
#testRefresh()
#testGetPage()
parseQuery.parseInput("Axe")
