#!/usr/bin/env python

import requests
import traceback
import sys
from bs4 import BeautifulSoup
import csv

## getHTML
def getHTML():
    url = "http://en.wikipedia.org/wiki/Mobile_country_code"
    html = ""
    try :
        r = requests.get(url)
        html = r.text.encode("utf-8")
    except: 
        traceback.print_exc()
        return html
    return html
## end

## getHeaders
def getHeaders():
    return ["MCC", "Country Name"]
## end

## getRows
def getRows(contextDiv):
    ## Find all h4's and table.wikitable
    h4List = contextDiv.find_all("h4")
    tableList = contextDiv.find_all("table", attrs={"class": "wikitable"})
    ## Store result in a set to avoid dupes
    resultSet = set()
    ## We loop the min of the lists len
    loopLen = min(len(h4List), len(tableList))
    for i in xrange(loopLen):
        ## Select "h4 span a" that contains country name
        h4 = h4List[i]
        a = h4.select("span a")
        ## If we don't find appropriate "a" tag, exit with error
        if (len(a) < 1):
            print resultSet
            print "Couldn't find link for " + str(h4) + ", i = " + str(i)
            sys.exit(1)

        ## Skip the test network, hence wikitable will always be i+1 lookup
        if i+1 == len(tableList):
            break

        ## Grab wikitable
        table = tableList[i+1]
        ## Find all "tr" and skip the header "tr"
        trList = table.find_all("tr")
        skipFirst = False
        for trElem in trList:
            if not skipFirst:
                skipFirst = True
                continue
            ## Find mcc
            mccNode = trElem.find("td")
            mcc = ""
            if mccNode != None:
                mcc = mccNode.get_text()
            ## Country name
            countryName = a[0].get_text()
            ## Add (mcc, country name) to the set if not empty
            if mcc != "" and countryName != "":
                res = (mcc.encode("utf-8").strip(), countryName.encode("utf-8").strip())
                resultSet.add(res)

    # convert back to list and sort it based on MCC
    resultList = list(resultSet)
    resultList.sort(key=lambda tup: tup[0])
    return resultList
## end

## Grab html from wiki
html = getHTML()
if html == "":
    print "HTML retrieve is empty, cannot proceed!!!"
    sys.exit(1)

## Use BeautifulSoup to extract headers and rows
soup = BeautifulSoup(html)
contextDiv = soup.find("div", attrs={"id": "mw-content-text"})
headers = getHeaders()
rows = getRows(contextDiv)

## Write to file
outputFileName = "mcc-wiki.csv"
try :
    f = open(outputFileName, "wb")
    writer = csv.writer(f, delimiter=",", quoting = csv.QUOTE_MINIMAL)
    writer.writerow(headers)
    writer.writerows(rows)
except:
    traceback.print_exc()
    sys.exit(1)
