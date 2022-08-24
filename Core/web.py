class Webpage:

    def __init__(self, name, url, itemTags, cmsTags, pagination, parentClass, priceClass, priceType, stockOption):
        self.name = name
        self.url = url
        self.itemTags = itemTags
        self.cmsTags = cmsTags
        self.pagination = pagination
        self.parentClass = parentClass
        self.priceClass = priceClass
        self.priceType = priceType
        self.stockOption = stockOption
        self.itemStorage = {}
    
    def updateStorage(self, itemDict):
        self.itemStorage = itemDict

    def getStorage(self):
        return self.itemStorage

    def getUrlInfo(self):
        return (self.url['baseUrl'], self.url['urlPrefix'],
            self.url['searchPrefix'], self.url['pagePrefix'])