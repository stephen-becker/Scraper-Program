def readConfigYaml(path):

    from yaml import safe_load

    with open(path, 'r') as primary:
        configData = safe_load(primary)

    try:
        configData['active-websites']
    except:
        raise Exception("\'active-websites\' column was not found!")

    table = {}

    for data in configData['active-websites']:

        if configData['active-websites'][data] == False:
            continue

        table[data] = configData['active-websites'][data]

    return table

def createCompleteLink(webData):
    insertIndex = webData['search-page-index']
    te = str(webData['search-url'])
    print(te)
    ste = "{te} + {}"

    return ste

def createObjects():

    cfData = readConfigYaml('./config.yaml')

    objList = []

    from yaml import safe_load
    from Core.web import Webpage

    for x in cfData:
        configFile = x + ".yaml"
        path = "./Core/Assests/" + configFile

        with open(path, 'r') as webConfig:
            yamlData = safe_load(webConfig)
            yamlData = yamlData['website-info']

        searchUrl = createCompleteLink(yamlData)
        print(searchUrl.format("1249"))
        
        objList.append(Webpage(yamlData['site-name'], yamlData['search-url'], yamlData['search-page'],
            yamlData['html-items'], yamlData['cms-products-class'], yamlData['pagnation-class']))

    return objList