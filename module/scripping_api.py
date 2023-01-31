from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
from tkinter import *
import re
import pandas as pd
import os

from module.setting import Config
from bs4 import BeautifulSoup
from linkedin_scraper import Person, actions
from module.helper import Helper
from lxml import html
from lxml import etree

from module.excel import Excel
from api.api_web import Api

from linkedin_api import Linkedin

class Scrap_API:
    def __init__(self,path,code,user,sandi,url,kategori,strt, end,max,id):
        self.strt   = strt
        self.end    = end
        self.code   = code
        self.user   = user
        self.sandi  = sandi
        self.url    = url
        self.kategori = kategori
        self.path   = path
        self.max    = max
        self.id     = id

    def scrap_api_url(self):
        #*********** MEMBUAT FOLDER JIKA BELUM ADA ***************#
        folder = f'{self.path}\public\{self.code}\html'

        isExist = os.path.exists(folder)

        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(folder)


        driver = webdriver.Chrome()
        actions.login(driver, self.user, self.sandi)
        driver.maximize_window()
            
        global data
        self.data = []

        for no in range(self.strt,self.end):
            start = "&page={}".format(no) 
            search_url = self.url+"{}".format(start)
            driver.get(search_url)

            time.sleep(2)

            name = f"{self.code}{no}.html" #PENAMAAN DOWNLOAD HTML

            Config.save(folder,name) #FUNCTION MENYIMPAN NAMA FILE

            time.sleep(5)

        driver.close()

        # api = Linkedin(self.user, self.sandi)
        api = Linkedin('harikarinjani@gmail.com', 'November101121')

        link_check = []
        total_get  = self.max
        for no in range(self.strt,self.end):
            check_html =Helper.exist_html(f"{folder}\{self.code}{no}.html")

            if check_html == 'success':
                soup = BeautifulSoup(open(f"{folder}\{self.code}{no}.html", encoding="utf8"), "html.parser")
                tag_a = soup.select("a.app-aware-link",attrs={'href': re.compile("^https://")})
                for link in tag_a:
                    href = link.get('href')
                    if link.get('href'):
                        if "miniProfileUrn" in href:
                        
                            if href not in link_check:
                                #script agar url tidak doubel
                                check_href_db = Api.url_list(href)

                                #jika ada tambah
                                if check_href_db['code']==400:
                                    if total_get == 0:
                                        break

                                    link_check.append(href)

                                    id_profile = Helper.id_profile(href)

                                    print(f'run script check number profile = {id_profile}')

                                    # Authenticate using any Linkedin account credentials
                                    # GET a profiles contact info
                                    contact_info = api.get_profile_contact_info(id_profile)
                                    # GET a profile
                                    profile_info      = api.get_profile(id_profile)

                                    #helper
                                    contact = Helper.api_contact(contact_info)
                                    profile = Helper.api_profile(profile_info)

                                    key = {
                                        'email'       :contact['email'],
                                        'phone'       :contact['phone'],
                                        'web'         :contact['web'],
                                        'nama'        :profile['nama'],
                                        'tentang'     :profile['tentang'],
                                        'jabatan'     :profile['jabatan'],
                                        'pengalaman'  :profile['pengalaman'],
                                        'url_profile' :href,
                                        'folder'      :self.code,
                                        'url_overlay' :Helper.url_overlay(href),
                                        'html_profile':'api',
                                        'link'        : id_profile,
                                        'crap_id'     : self.id 
                                    }

                                    t=Api.save(key)

                                    print(t)

                                    #mengurangi jumlah data sesui maximal di ambil
                                    total_get -=1

                                    

        return 'selesai menjalakan scripping'