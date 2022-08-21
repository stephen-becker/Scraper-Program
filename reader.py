# Created by: Stephen Becker
# Created on: 08-07-2022
# Program name: Web Scraper
# Program description: This program scrapes a website, specifically newegg, and pulls requested searched data
#                      then sorts it by price into console.

# Imports & Libs
from cgitb import html
import os
from bs4 import BeautifulSoup as bs
from Core.search import createObjects
import requests
import re
import cchardet
import lxml
import json

# Gets user input to be used to search the website
userInquiry = str(input("What item to search for? "))
itemCount = 0

# Gets the url information and takes the html for BeautifulSoup to analyize
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

websites = createObjects()
website_items = {}
itemStorage = {}

for site in websites:

    url = site.searchLink + userInquiry
    searchPage = requests.get(url, HEADERS).text
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

    pageNumbers = max(pageNumbers)

    for currentPage in range(1, pageNumbers+1):
        newUrl = url + site.searchTag + str(currentPage)
        onPage = currentPage
        searchPage = requests.get(newUrl, HEADERS).text
        htmlFrame = bs(searchPage, "lxml")

        div = htmlFrame.find(class_=site.itemTags)
        itemsFound = div.find_all(text=(re.compile(userInquiry, flags=re.I)))

        #Added status feature to see progress
        print("Scanning Page {}/{}\t-\tApprox {} items scanned.".format(currentPage,pageNumbers,len(itemsFound)))

        for item in itemsFound:

            # Goes out to parent cell since price and link are in another subclass
            parent = item.parent
            link = None
            outOfStock = False
            dualParent = item.parent.parent

            # # If exclude out of stock feature is enabled, will pass by items that are out of stock
            # if outOfStockExcluded:

            #     try: 

            #         if "OUT OF STOCK" in list(dualParent.children)[2]:

            #             continue
                    
            #     except:

            #         pass

            # # If exclude out of stock feature is disabled, will include the item but will be shown as out of stock
            # else:

            #     try: 

            #         if "OUT OF STOCK" in list(dualParent.children)[2]:

            #             outOfStock = True
                    
            #     except:

            #         pass

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
                itemStorage[item] = {"id": hash(item), "price": int(price.replace(",", "")), "link": link, "newegg in stock": not outOfStock}

            except:

                pass
        
        site.updateStorage(itemStorage)
        website_items[site.name] = site

print(website_items)

# # Sorts the items by lowest price first
# sortedItems = sorted(itemStorage.items(), key=lambda x: x[1]['price'])

# print(sortedItems)


#     # Gets new page html information for each page
#     url = "https://www.newegg.com/p/pl?d={}&page={}".format(userInquiry, pageNumber)
#     currentPage = pageNumber
#     pageNumber = requests.get(url).text
#     htmlFrame = BeautifulSoup(pageNumber, "lxml")
    
#     # This finds a specific class where the information we want is located (name, price, etc.) then it procedes to
#     # match what we typed in to search for to match all the items containing our inquiry keyword
#     div = htmlFrame.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
#     itemsFound = div.find_all(text=(re.compile(userInquiry, flags=re.I)))

#     # Added status feature to see progress
#     print("Scanning Page {}/{}\t-\tApprox {} items scanned.".format(currentPage,limitRangeNumber-1,len(itemsFound)))

#     # Loop is responsible for iterating through each found item and pulling price and link information
#     for item in itemsFound:

#         # Goes out to parent cell since price and link are in another subclass
#         parent = item.parent
#         link = None
#         outOfStock = False
#         dualParent = item.parent.parent

#         # If exclude out of stock feature is enabled, will pass by items that are out of stock
#         if outOfStockExcluded:

#             try: 

#                 if "OUT OF STOCK" in list(dualParent.children)[2]:

#                     continue
                
#             except:

#                 pass

#         # If exclude out of stock feature is disabled, will include the item but will be shown as out of stock
#         else:

#             try: 

#                 if "OUT OF STOCK" in list(dualParent.children)[2]:

#                     outOfStock = True
                
#             except:

#                 pass

#         # Decision statement to determine if item has a link tag
#         if parent.name != "a":

#             continue
        
#         # Sets the link tag, then goes to next parent to get the price infomration
#         link = parent['href']
#         nextParent = item.find_parent(class_="item-container")

#         # Try-except statement needed because some prices don't have a strong tag
#         try:

#             # Sets price and place into the hash table
#             price = nextParent.find(class_="price-current").find("strong").string
#             itemStorage[item] = {"id": hash(item), "price": int(price.replace(",", "")), "link": link, "newegg in stock": not outOfStock}

#         except:

#             pass

# # Sorts the items by lowest price first
# sortedItems = sorted(itemStorage.items(), key=lambda x: x[1]['price'])

# # Loop prints each item from the hash table by name, price, and link
# for item in sortedItems:
#     # print("Name:\t{}\nId:\t{}\nPrice:\t${}\nLink:\t{}\nIn Stock:\t{}\n\n".format(item[0],item[1]['id'],item[1]['price'],item[1]['link'],item[1]['newegg in stock']))
#     # Statement above is now irrelevent due to the new json output
#     itemCount += 1

# # Creates a generic json file with all the output
# if not os.path.exists("Output Directory"):
#     os.mkdir("Output Directory")

# with open("Output Directory/output.json", "w") as file:
#     json.dump(sortedItems, file, indent=4)

# print("{} items returned. Outputed to \"Output Directory/output.json\" file.\n".format(itemCount))