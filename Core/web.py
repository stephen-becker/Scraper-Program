class Webpage:

    def __init__(self, name, searchLink, searchTag, itemTags, cmsTags, pagnation):
        self.name = name
        self.searchLink = searchLink
        self.searchTag = searchTag
        self.itemTags = itemTags
        self.cmsTags = cmsTags
        self.pagnation = pagnation
        self.itemStorage = {}
    
    def updateStorage(self, itemDict):
        self.itemStorage = itemDict

    def getStorage(self):
        return self.itemStorage