#!/usr/bin/env python

import requests
import traceback
import sys
from bs4 import BeautifulSoup
import csv

## getHTML
def getHTML():
    url = "http://mcc-mnc.com/"
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
def getHeaders(table):
    ## Find thead
    thead = table.find("thead")
    if thead is None:
        print "Didn't find thead tag in table, cannot proceed!!!"
        sys.exit(1)
    return [header.text.strip() for header in thead.find_all("th")]
## end

## getRows
def getRows(table):
    ## Find tbody
    tbody = table.find("tbody")
    if tbody is None:
        print "Didn't find tbody tag in table, cannot proceed!!!"
        sys.exit(1)

    rows= []
    for row in tbody.find_all("tr"):
        rows.append([val.text.strip() for val in row.find_all("td")])
    return rows
## end

html = getHTML()
if html == "":
    print "HTML retrieve is empty, cannot proceed!!!"
    sys.exit(1)

soup = BeautifulSoup(html)
table = soup.find("table", attrs={"id": "mncmccTable"})
headers = getHeaders(table)
rows = getRows(table)

outputFileName = "mcc-mnc.csv"
try :
    f = open(outputFileName, "wb")
    writer = csv.writer(f, delimiter=",", quoting = csv.QUOTE_MINIMAL)
    writer.writerow(headers)
    writer.writerows(rows)
except:
    traceback.print_exc()
    sys.exit(1)
