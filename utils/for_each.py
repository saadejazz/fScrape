from sites import SITE_NAMES
from datum import CACHE_NAMES

def searchScrape(siteName, keyword):
    if checkValidityOfSite(siteName):
        s = SITE_NAMES[siteName]()
        return s.scrapeAll(s.search(keyword))
    return []

def categoryScrape(siteName, category):
    if checkValidityOfSite(siteName):
        s = SITE_NAMES[siteName]()
        return s.scrapeAll(s.getListings(category))
    return []

def scrape(siteName, args):
    if checkValidityOfSite(siteName):
        category = []
        keywords = []
        for i in args:
            if ":" in i:
                sp = i.split(":")
                cat = sp[0].strip()
                sub = sp[1].strip()
                if cat in CACHE_NAMES[siteName]:
                    if sub in CACHE_NAMES[siteName][cat]:
                        category.append(i)
                    else:
                        keywords.append(sub)
                else:
                    keywords.append(sub)
            else:
                if i in CACHE_NAMES[siteName]:
                    category += [i + ": " + k for k in list(CACHE_NAMES[siteName][i].keys())]
                else:
                    keywords.append(i)
        return categoryScrape(siteName, category) + searchScrape(siteName, keywords)
    return []

def printCategories(siteName):
    if checkValidityOfSite(siteName):
        for i in CACHE_NAMES[siteName]:
            print(i)
            for x in CACHE_NAMES[siteName][i]:
                print(f"{i}: {x}")
            print("")

def checkValidityOfSite(siteName):
    if siteName in SITE_NAMES:
        return True
    print("Invalid Site name")
    return False