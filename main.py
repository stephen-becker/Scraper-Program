# Created by: Stephen Becker
# Created on: 08-07-2022
# Program name: Web Scrapper
# Program description: This program scrapes a website, specifically newegg, and pulls requested searched data
#                      then sorts it by price into console.

# Imports & Libs
from posixpath import split
from bs4 import BeautifulSoup
import requests
import re

# Gets user input to be used to search the website
userInquiry = str(input("What item to search for? "))
itemCount = 0

# Gets the url information and takes the html for BeautifulSoup to analyize
url = "https://www.newegg.com/p/pl?d={}".format(userInquiry)
searchPage = requests.get(url).text
htmlFrame = BeautifulSoup(searchPage, "lxml")

# Finds how many pages of the items there are
pageSelector = htmlFrame.find(class_="list-tool-pagination-text").find("strong")
maxNumberPages = int(str(pageSelector).split("/")[1].split(">")[1][:-1])

# Creates an empty hash table to add the items in that we want
itemStorage = {}

# For loop is responsible for going through each page up to the max number to go through all found items
for pageNumber in range(1, maxNumberPages + 1):

    # Gets new page html information for each page
    url = "https://www.newegg.com/p/pl?d={}&page={}".format(userInquiry, pageNumber)
    pageNumber = requests.get(url).text
    htmlFrame = BeautifulSoup(pageNumber, "lxml")
    
    # This finds a specific class where the information we want is located (name, price, etc.) then it procedes to
    # match what we typed in to search for to match all the items containing our inquiry keyword
    div = htmlFrame.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    itemsFound = div.find_all(text=(re.compile(userInquiry, flags=re.I)))

    # Loop is responsible for iterating through each found item and pulling price and link information
    for item in itemsFound:

        # Goes out to parent cell since price and link are in another subclass
        parent = item.parent
        link = None

        # Decision statement to determine if item has a link tag
        if parent.name != "a":

            continue
        
        # Sets the link tag, then goes to next parent to get the price infomration
        link = parent['href']
        nextParent = item.find_parent(class_="item-container")

        # Try-except statement needed because some prices don't have a strong tag
        try:

            # Sets price and place into the hash table
            price = nextParent.find(class_="price-current").find("strong").string
            itemStorage[item] = {"price": int(price.replace(",", "")), "link": link}

        except:

            pass

# Sorts the items by lowest price first
sortedItems = sorted(itemStorage.items(), key=lambda x: x[1]['price'])

# Loop prints each item from the hash table by name, price, and link
for item in sortedItems:
    print("Name:\t{}\nPrice:\t${}\nLink:\t{}\n\n".format(item[0],item[1]['price'],item[1]['link']))
    itemCount += 1

print("{} items returned\n".format(itemCount))