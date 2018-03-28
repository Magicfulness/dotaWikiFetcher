import utils
import makePages as mP
import re
import json

#TODO: handle incorrect user inputs
def parseInput(query):

    query = query.split()

    #check if first word is valid hero or item
    cat = utils.getCat(query[0])
    if not cat:
        print("failure")
        return None

    info = utils.getPage(query[0])

    #TODO: Abilities, HeroStats (header), Talents
    #TODO: Lesser priority: Bio, Trivia, changelogs
    for item in info["header"]:
        print(item)
        print("  " + str(info["header"][item]))

