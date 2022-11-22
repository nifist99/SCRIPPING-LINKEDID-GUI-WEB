import os
import pathlib
from os.path import exists
from bs4 import BeautifulSoup
from run_api import main_api
from run import main
import glob
import os
import requests
import json
from module.scrapping import Scrap
from module.setting import Config
import chromedriver_autoinstaller
from module.excel import Excel
from module.scripping_api import Scrap_API
from linkedin_scraper import Person,Company
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from api.api_web import Api
import requests
import json
import shutil
from module.excel import Excel
from module.helper import Helper
from linkedin_api import Linkedin
import time
from tkinter import *
import re
import pandas as pd
import os

import chromedriver_autoinstaller

from module.setting import Config

path = pathlib.Path(__file__).parent.resolve()



def main():
    print('#*********** WELCOME TO BOT LINKED IND ***************#')
    print("ini ada 2 metode by API DAN WEB")
    print()

    print("1 by api (lebih cepat max 1000 data per hari)")
    print("2 by web (lebih lambat max unlimited)")

    print()

    code   = int(input('masukan code scryping check di website ='))

    if code == 1:
        os.system("cls")
        main_api()
    elif code == 2:
        os.system("cls")
        main()

    
    else:
        os.system("cls")
        print("masukan data yang benar")
        exit()

if __name__ == "__main__":
    main()



