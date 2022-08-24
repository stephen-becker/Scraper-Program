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

def getSearchOptions(path):

    from yaml import safe_load

    with open(path, 'r') as primary:
        configData = safe_load(primary)
    
    return configData['search-options']

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

        urlInfo = {"baseUrl": yamlData['search-url'], "urlPrefix": yamlData['url-prefix'],
                    "searchPrefix": yamlData['search-prefix'], "pagePrefix": yamlData['page-prefix']}

        objList.append(Webpage(yamlData['site-name'], urlInfo,
            yamlData['html-items'], yamlData['cms-products-class'], yamlData['pagination-class'],
            yamlData['parent-info'], yamlData['price-info'], yamlData['price-type'], yamlData['out-of-stock']))

    return objList