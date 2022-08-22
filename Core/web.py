class Webpage:

    def __init__(self, name, url, itemTags, cmsTags, pagnation, parentClass, priceClass, priceType):
        self.name = name
        self.url = url
        self.itemTags = itemTags
        self.cmsTags = cmsTags
        self.pagnation = pagnation
        self.parentClass = parentClass
        self.priceClass = priceClass
        self.priceType = priceType
        self.itemStorage = {}
    
    def updateStorage(self, itemDict):
        self.itemStorage = itemDict

    def getStorage(self):
        return self.itemStorage

    def getUrlInfo(self):
        return (self.url['baseUrl'], self.url['urlPrefix'],
            self.url['searchPrefix'], self.url['pagePrefix'])