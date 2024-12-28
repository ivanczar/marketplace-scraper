import re


def pluralize(noun: str) -> str:
    if re.search("[sxz]$", noun):
        return re.sub("$", "es", noun)
    elif re.search("[^aeioudgkprt]h$", noun):
        return re.sub("$", "es", noun)
    elif re.search("[aeiou]y$", noun):
        return re.sub("y$", "ies", noun)
    else:
        return noun + "s"


def getLastScrapedTitle(filePath: str) -> str:
    f = open(filePath, "r")
    lastScrapedTitle = f.read()
    f.close()
    return lastScrapedTitle


def setLastScrapedTitle(filePath: str, title: str) -> None:
    f = open(filePath, "w")
    f.write(title)
    f.close()
