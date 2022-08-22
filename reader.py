# Created by: Stephen Becker
# Created on: 08-07-2022
# Program name: Web Scraper
# Program description: This program scrapes a website, specifically newegg, and pulls requested searched data
#                      then sorts it by price into console.

# Imports & Libs
from cgitb import html
import os
from bs4 import BeautifulSoup as bs
from Core.search import createObjects, getSearchOptions
import requests
import re
import cchardet
import lxml
import json

# # Gets user input to be used to search the website
# itemCount = 0

# Gets the url information and takes the html for BeautifulSoup to analyize
HDR = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

websites = createObjects()
website_items = {}
itemStorage = {}
sortedItems = {}

settings = getSearchOptions("./config.yaml")


print("Searching: ", end="")

for site in websites:
    print(site.name, end=" ")

userInquiry = str(input("\nWhat item to search for? "))

for site in websites:

    baseUrl, urlPrefix, searchPrefix, pagePrefix = site.getUrlInfo()

    url = baseUrl + urlPrefix + searchPrefix + userInquiry
    searchPage = requests.get(url, headers=HDR).text
    htmlFrame = bs(searchPage, "lxml")

    #pagnation
    footer_element = htmlFrame.select("." + site.pagnation)
    pageNumbers = []

    for x in footer_element:

        try:
            num = int(x.text.strip())
        except:
            continue

        pageNumbers.append(num)

    if len(pageNumbers) == 0:
        pageNumbers = 1
    else:
        pageNumbers = max(pageNumbers)

    pageLimit = settings['limit-pages']

    if pageLimit > pageNumbers or pageLimit <= 0:
        pageLimit = pageNumbers

    limitRangeNumber = (pageNumbers - (pageNumbers - pageLimit))

    for currentPage in range(1, limitRangeNumber+1):
        newUrl = url + urlPrefix + pagePrefix + str(currentPage)
        onPage = currentPage
        searchPage = requests.get(newUrl, headers=HDR).text
        htmlFrame = bs(searchPage, "lxml")

        div = htmlFrame.find(class_=site.itemTags)
        itemsFound = div.find_all(text=(re.compile(userInquiry, flags=re.I)))

        print("{} - Scanning Page {}/{}\t-\tApprox {} items scanned.".format(site.name, currentPage,limitRangeNumber,len(itemsFound)))

        for item in itemsFound:
            parent = item.parent
            link = None
            dParent = parent.parent

            if parent.name != "a":

                continue

            link = parent['href']


            if site.name == "BestBuy":
                link = "https://bestbuy.com" + link

            nextParent = item.find_parent(class_=site.parentClass)

            try:

                price = nextParent.find(class_=site.priceClass).find(site.priceType).text
                price = price.strip("$")

                if not ".99" in price:
                    price = price + ".99"

                itemStorage[item] = {"site id": str(site.name), "price": float(price.replace(",", "")), "link": link, "in stock": True}
            
            except:

                pass

sortedItems = sorted(itemStorage.items(), key=lambda x: x[1]['price'])

# Creates a generic json file with all the output
if not os.path.exists("Output Directory"):
    os.mkdir("Output Directory")

with open("Output Directory/output.json", "w") as file:
    json.dump(sortedItems, file, indent=4)