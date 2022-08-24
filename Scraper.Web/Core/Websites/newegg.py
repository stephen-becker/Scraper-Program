import yaml
import os
from posixpath import split
from bs4 import BeautifulSoup
import requests
import re
import cchardet
import lxml
import json
import sys

if not os.path.exists("Assests/newegg.yaml"):
    assert("Error, config file not found")

with open("Assests/newegg.yml", "r") as neweggConfig:
    configData = yaml.load(neweggConfig, Loader=yaml.FullLoader)

productSearch = str(sys.argv)