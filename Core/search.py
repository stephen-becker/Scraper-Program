# readConfigYaml
# description: returns active websites from config file
# parameters: path to a config yaml file
# returns: a dict with active configurations
def readConfigYaml(path):

    from yaml import safe_load

    # Opens config file
    with open(path, 'r') as primary:
        configData = safe_load(primary)

    # Checks to ensure config file is formatted to read correctly
    try:
        configData['active-websites']
    except:
        raise Exception("\'active-websites\' column was not found!")

    table = {}

    # Sends config data to the table which is returned
    for data in configData['active-websites']:

        if configData['active-websites'][data] == False:
            continue

        table[data] = configData['active-websites'][data]

    return table

# getSearchOptions
# description: returns the search options from the config file
# parameters: path to a config yaml file
# returns: a dict with search options
def getSearchOptions(path):

    from yaml import safe_load

    with open(path, 'r') as primary:
        configData = safe_load(primary)
    
    return configData['search-options']

# createObjects
# description: this creates website objects from the web_class.py and returns them
# parameters: none
# returns: list of class objects
def createObjects():

    # PATH/FILE Declarations
    cPATH = './Core/ConfigFiles/config.yaml'
    cfsPATH = './Core/ConfigFiles/'
    EXT = '.yaml'

    # Needs active websites from config
    cfData = readConfigYaml(cPATH)

    objList = []

    from yaml import safe_load
    from Core.web_class import Webpage

    # Loop iterates through each active website and creates it respective object
    for x in cfData:

        configFile = x + EXT
        path = cfsPATH + configFile

        # Loads each config file for each active website
        with open(path, 'r') as webConfig:
            yamlData = safe_load(webConfig)
            yamlData = yamlData['website-info']

        # Creates the object and appends it to a list
        urlInfo = {"baseUrl": yamlData['search-url'], "urlPrefix": yamlData['url-prefix'],
                    "searchPrefix": yamlData['search-prefix'], "pagePrefix": yamlData['page-prefix']}

        objList.append(Webpage(yamlData['site-name'], urlInfo,
            yamlData['html-items'], yamlData['cms-products-class'], yamlData['pagination-class'],
            yamlData['parent-info'], yamlData['price-info'], yamlData['price-type'], yamlData['out-of-stock']))

    # Validator
    if len(objList) == 0:
        if len(cfData) == 0:
            raise Exception("There are no active websites. Exiting program.")
        else:
            raise Exception("Something went wrong with creating the website class objects.")

    return objList