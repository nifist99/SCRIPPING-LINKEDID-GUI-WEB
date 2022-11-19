from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import xlsxwriter
from tkinter import *
import requests
import re
import pyautogui
import pandas as pd
import os

from module.setting import Config

from bs4 import BeautifulSoup
from linkedin_scraper import Person, actions
from module.helper import Helper
from lxml import html
from lxml import etree

from module.excel import Excel

from os.path import exists

from api.api_web import Api

class Scrap:
    def __init__(self,path,code,user,sandi,url,kategori,strt, end,max):
        self.strt   = strt
        self.end    = end
        self.code   = code
        self.user   = user
        self.sandi  = sandi
        self.url    = url
        self.kategori = kategori
        self.path   = path
        self.max    = max

    def scrap_kategori(self):
        #*********** MEMBUAT FOLDER JIKA BELUM ADA ***************#
        folder = f'{self.path}\public\{self.code}\html'

        isExist = os.path.exists(folder)

        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(folder)


        driver = webdriver.Chrome()
        actions.login(driver, self.user, self.sandi)
        driver.maximize_window()
        

        #*********** Search Result ***************#
        search_key = self.kategori # Enter your Search key here to find people
        key = search_key.split()
        keyword = ""
        for key1 in key:
            keyword = keyword + str(key1).capitalize() +"%20"
        keyword = keyword.rstrip("%20")
            
        global data
        self.data = []

        for no in range(self.strt,self.end):
            start = "&page={}".format(no) 
            search_url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=SUGGESTION{}".format(keyword,start)
            driver.get(search_url)

            time.sleep(2)

            name = f"{self.code}{no}.html" #PENAMAAN DOWNLOAD HTML

            Config.save(folder,name) #FUNCTION MENYIMPAN NAMA FILE

        link_check = []
        total_get  = self.max
        for no in range(self.strt,self.end):
            soup = BeautifulSoup(open(f"{folder}\{self.code}{no}.html", encoding="utf8"), "html.parser")
            tag_a = soup.select("a.app-aware-link",attrs={'href': re.compile("^https://")})
            for link in tag_a:
                href = link.get('href')
                if link.get('href'):
                    if "miniProfileUrn" in href:
                        print(f"collect link profile")
                    
                        if href not in link_check:
                            #script agar url tidak doubel
                            check_href_db = Api.url_list(href)

                            #jika ada tambah
                            if check_href_db['code']==400:
                                if total_get == 0:
                                    break

                                link_check.append(href)        

                                self.data.append({
                                    "folder":f'{self.code}{no}.html',
                                    "link"  :href,
                                    "code"  :self.code
                                })

                                #mengurangi jumlah data sesui maximal di ambil
                                total_get -=1

                                    

        return self.data

    def scrap_filter_url(self):
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

        link_check = []
        total_get  = self.max
        for no in range(self.strt,self.end):
            soup = BeautifulSoup(open(f"{folder}\{self.code}{no}.html", encoding="utf8"), "html.parser")
            tag_a = soup.select("a.app-aware-link",attrs={'href': re.compile("^https://")})
            for link in tag_a:
                href = link.get('href')
                if link.get('href'):
                    if "miniProfileUrn" in href:
                        print(f"collect link profile")
                    
                        if href not in link_check:
                            #script agar url tidak doubel
                            check_href_db = Api.url_list(href)

                            #jika ada tambah
                            if check_href_db['code']==400:
                                if total_get == 0:
                                    break

                                link_check.append(href)        

                                self.data.append({
                                    "folder":f'{self.code}{no}.html',
                                    "link"  :href,
                                    "code"  :self.code
                                })

                                #mengurangi jumlah data sesui maximal di ambil
                                total_get -=1

                                    

        return self.data

    def get_profile(self):

         #*********** MEMBUAT FOLDER JIKA BELUM ADA ***************#
        folder = f'{self.path}\public\{self.code}\profile'

        isExist = os.path.exists(folder)

        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(folder)

        driver = webdriver.Chrome()
        actions.login(driver, self.user, self.sandi)
        driver.maximize_window()
        
        n = 1 
        for key in self.data:
            print(f"save html profile")
            driver.get(key['link'])
            get_url = driver.current_url+'overlay/contact-info/'
            #MEMBUKA INFORMASI DETAIL
            driver.get(get_url)

            check_result = Api.check_result(get_url)

            if check_result['code']==400:

                try:
                    element = WebDriverWait(driver,60).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "artdeco-modal__content"))
                            )
                    
                    time.sleep(3)

                    name = f"{self.code}{n}.html"

                    Config.save(folder,name)

                    #transpool data sementara untuk mapping
                    Api.transpool_create(key['code'],key['link'],get_url,key['folder'],name)

                    #update data ke profile
                    Api.update_get_profile(get_url,name,key['link'],self.code)

                    time.sleep(2)

                    n+=1

                except:

                    pass
            


        driver.close()

        return True

    def script_profile(self):
        self.result = []
        ret = []

        all = Api.transpool_all()
        
        for key in all['data']:
            path_to_file = f"{self.path}\public\{key['code']}\profile\{key['html_profile']}"
            file_exists = exists(path_to_file)
            if file_exists:
                soup = BeautifulSoup(open(path_to_file, encoding="utf8"), "html.parser")
                
                try:
                    try:
                        nama = soup.select('h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words')[0].string
                    except:
                        pass
                except AttributeError:
                    nama = "N/A"
                
                try:
                    try:
                        jabatan = soup.select('div.text-body-medium.break-words')[0].string
                    except:
                        pass
                except AttributeError:
                    jabatan = "N/A"

                about =''
                experience = []
                pt      = ''
                jabatan = ''
                masa    = ''
                for sec in soup.find_all('section',{"class":['artdeco-card','ember-view','relative','break-words','pb3','mt2']}):
                    if sec.find(id="about"):
                        span = sec.find('div',{"class":['inline-show-more-text','inline-show-more-text--is-collapsed']})
                        if len(span)!=0:
                                for val in span.find_all('span'):
                                    about = val.text

                    if sec.find(id="experience"): 
                        li = sec.find_all('li',{"class":['artdeco-list__item','pvs-list__item--line-separated','pvs-list__item--one-column']})
                        if( len(li))!=0:
                            for ex in li:
                                pt          = ex.find('span',{"class":['t-14','t-normal','span']}).text
                                jabatan     = ex.find('span',{"class":["mr1","t-bold","span"]}).text
                                masa        = ex.find('span',{"class":['t-14','t-normal','t-black--light','span']}).text
                                experience.append({
                                    "pt"        : pt.replace('\n',''),
                                    "jabatan"   : jabatan.replace('\n',''),
                                    "masa"      : masa.replace('\n','')
                                })

                
                #INFORMASI ACCOUNT 

                profile       = soup.find('div',{"class":['pv-profile-section__section-info','section-info']})

                #link linkedin
                try:
                    l_link  = profile.find('section',{"class":['ci-vanity-url']})
                    link    = l_link.select('a.pv-contact-info__contact-link.link-without-visited-state.t-14')[0].string
                except AttributeError:
                    link = "N/A"

                #email
                try:
                    l_email  = profile.find('section',{"class":['ci-email']})
                    email    = l_email.select('a.pv-contact-info__contact-link.link-without-visited-state.t-14')[0].string
                except AttributeError:
                    email = "N/A"
                #phone    
                try:

                    l_phone  = profile.find('section',{"class":['ci-phone']})
                    l_phone2 = l_phone.find('li',{"class":['pv-contact-info__ci-container','t-14']})
                    phone  = l_phone2.select('span.t-14.t-black.t-normal')[0].string

                except AttributeError:
                    phone = "N/A"

                try:

                    l_website  = profile.find('section',{"class":['ci-websites']})
                    l_website2 = l_website.find('li',{"class":['pv-contact-info__ci-container','t-14']})
                    website   = l_website2.select('a')[0].string

                except AttributeError:
                    website = "N/A"

                ret.append({
                    "nama"      : nama,
                    "jabatan"   : jabatan,
                    "about"     : about,
                    "experience":experience,
                    "link"      : link,
                    "email"     : email,
                    "phone"     :phone,
                    "website"   :website,
                    "url_overlay":key['url_overlay']
                })

            self.result = ret

        return self.result