# Created by: Stephen Becker
# Created on: 08-07-2022
# Updated on: 08-28-2022
# Version: 1.0.1
# Program name: Web Scraper
# Program description: This program scrapes a website, specifically newegg and bestbuy, and pulls requested searched data
#                      then sorts it by price.

# Imports & Libs
import os
from bs4 import BeautifulSoup as bs
from Core.search import createObjects, getSearchOptions
import requests
import re
import json
import time

# Header information for the User-Agent when getting the link
HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
cPATH = './Core/ConfigFiles/config.yaml'
OUTPUT_PATH = './Output Directory/'

# Variables & Initalizations
websites = createObjects()
settings = getSearchOptions(cPATH)
website_items = {}
itemStorage = {}
sortedItems = {}
delay = settings['wait-time']
stockOption = settings['include-out-of-stock']
isInStock = True

# Begin the web scraping process

# Prints the list of websites scraping - this list is taken from the config.yaml
print("Searching: ", end="")

for site in websites:
    print(site.name, end=" ")

# Gets the user inquiry - please note that this has to be relatively exact, more is explained on docs
userInquiry = str(input("\nWhat item to search for? "))

# Loops through the selected websites to scrape product data
for site in websites:

    baseUrl, urlPrefix, searchPrefix, pagePrefix = site.getUrlInfo()

    # Creates the url and requests to get the page content
    url = baseUrl + urlPrefix + searchPrefix + userInquiry
    searchPage = requests.get(url, headers=HDR).text
    htmlFrame = bs(searchPage, 'lxml')

    # Handles getting the max page numbers from the pagination class for each website
    pageLimit = settings['limit-pages']
    pagination = htmlFrame.select("." + site.pagination)
    pageNumbers = []

    # Loop goes through each html frame and only takes the ones that are ints
    for x in pagination:

        try:
            num = int(x.text.strip())
        except:
            continue
        
        # When it finds a number, it appends it to a list
        pageNumbers.append(num)

    # Fallback statement incase the page is found to only be 1 page of results
    if len(pageNumbers) == 0:
        pageNumbers = 1
    else:
        # Gets the max number from the pageNumbers list
        pageNumbers = max(pageNumbers)

    # Ensures that the page limit is within valid bounds
    if pageLimit > pageNumbers or pageLimit <= 0:
        pageLimit = pageNumbers
    
    limitRangeNumber = (pageNumbers - (pageNumbers - pageLimit))

    # Ensures that the delay limit is within valid bounds
    if delay < 0 or delay > 600:
        print("Wait time of {} was found to be invalid, reverting to back to default value.".format(delay))
        delay = 0

    # This loop is responsible for going through each page and grabbing elements containing the keyword from the inquiry
    for currentPage in range(1, limitRangeNumber+1):

        # Logic for everyother site except Newegg out of stock options, not finalized version
        if not site.name == "Newegg" and not stockOption:
            newUrl = url + urlPrefix + pagePrefix + str(currentPage) + urlPrefix + site.stockOption
        else:
            newUrl = url + urlPrefix + pagePrefix + str(currentPage)

        # Variables & Initalizations
        onPage = currentPage
        searchPage = requests.get(newUrl, headers=HDR).text
        htmlFrame = bs(searchPage, 'lxml')

        # Goes through specific divs to pull product name, once it gets the product names it matches for the user inquiry
        div = htmlFrame.find(class_=site.itemTags)

        try:
            itemsFound = div.find_all(text=(re.compile(userInquiry, flags=re.I)))
        except:
            raise Exception("The input of \"{}\", returned an invalid response. Please try again.".format(userInquiry))

        # Standard - Outputs status
        print("{} - Scanning Page {}/{}\t-\tApprox {} items scanned.".format(site.name, currentPage,limitRangeNumber,len(itemsFound)))

        # Goes through the items found and pulls price and link
        for item in itemsFound:

            # HTML navigation from items position - like a tree structure
            parent = item.parent
            link = None
            dParent = parent.parent

            # If link is not present, skips item
            if parent.name != "a":
                continue

            # Sets the link for the item
            link = parent['href']

            # BestBuys links are naturally missing the bestbuy.com so it's added to the string
            if site.name == "BestBuy":
                link = "https://bestbuy.com" + link
            
            # Logic for Newegg out of stock options, not finalized version
            if site.name == "Newegg" and not stockOption:

                try: 

                    if "OUT OF STOCK" in list(dParent.children)[2]:

                        continue
            
                except:

                    pass

            elif site.name == "Newegg" and stockOption:

                try: 

                    if "OUT OF STOCK" in list(dParent.children)[2]:

                        isInStock = False
            
                except:

                    pass

            # This gets the parent for where the price is located inside of it
            nextParent = item.find_parent(class_=site.parentClass)

            try:

                # Finds the price, removes the '$' from it to allow for proper sorting
                price = nextParent.find(class_=site.priceClass).find(site.priceType).text
                price = price.strip('$')

                # Basic string amender to add .99 to end of price if it's not included
                if not ".99" in price:
                    price = price + ".99"

                # Adds the item to itemStorage to be outputted later on once sorted
                itemStorage[item] = {"site_id": str(site.name), "price": float(price.replace(",", "")), "link": link, "in_stock": isInStock}
            
            except:

                pass
        
        # If wait time is set this is where it will wait to proceed
        if delay > 0:
            print("Waiting {} seconds to scrape the next page.".format(delay))
            time.sleep(delay)

# Basic sorting algorithim that sorts based on price
sortedItems = sorted(itemStorage.items(), key=lambda x: x[1]['price'])

# Final output to console
print("Scrape finished, outputted {} items to output file.".format(len(sortedItems)))

# Creates a generic json file with all the sorted output
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

OUT_FILE_NAME = userInquiry + "_search.json"
fPATH = OUTPUT_PATH+OUT_FILE_NAME

with open(fPATH, "w") as file:
    json.dump(sortedItems, file, indent=4)