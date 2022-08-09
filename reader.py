import yaml

with open("Py Files/Assests/newegg.yaml", "r") as config:
    configData = yaml.load(config, Loader=yaml.FullLoader)

print(str(configData['website-info']['search-url']))