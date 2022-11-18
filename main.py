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


from bs4 import BeautifulSoup
from linkedin_scraper import Person, actions
from setting import USER,PASS
from helper import Helper
from lxml import html
from lxml import etree

from excel import Excel

from os.path import exists


class Linkedin:
    def __init__(self,strt, end):
        self.strt = strt
        self.end   = end

    def getData(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        actions.login(driver, USER, PASS)
        

        #*********** Search Result ***************#
        search_key = "manager" # Enter your Search key here to find people
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

            name = f"halaman{no}.html"
            Helper.save(name)

        link_check = []
        for no in range(self.strt,self.end):
            soup = BeautifulSoup(open(f"C:\\python\\FREELANCE\\LINKEDIN\\html\\halaman{no}.html", encoding="utf8"), "html.parser")
            tag_a = soup.select("a.app-aware-link",attrs={'href': re.compile("^https://")})
            for link in tag_a:
                href = link.get('href')
                if link.get('href'):
                    if "miniProfileUrn" in href:
                        print(f"collect link profile")
                    
                        if href not in link_check:
                            link_check.append(href)        
                            self.data.append({
                                "link":href
                            })
        

    def getProfile(self):
        driver = webdriver.Chrome()
        actions.login(driver, USER, PASS)
        driver.maximize_window()
        
        n = 1 

        for key in self.data:
            print(f"save html profile")
            driver.get(key['link'])
            get_url = driver.current_url+'/overlay/contact-info/'
            #MEMBUKA INFORMASI DETAIL
            driver.get(get_url)

            element = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "artdeco-modal__content"))
                    )

            time.sleep(3)

            name = f"profile{n}.html"
            Helper.saveprofile(name)
            time.sleep(2)
            n+=1

        self.total_profile = n

        driver.close()


    def script_profile(self):
        self.result = []
        ret = []

        total = self.total_profile + 1
        # total = 17 + 1
        for no in range(self.strt,total):
            path_to_file = f"C:\\python\\FREELANCE\\LINKEDIN\\profile\\profile{no}.html"
            file_exists = exists(path_to_file)
            if file_exists:
                soup = BeautifulSoup(open(f"C:\\python\\FREELANCE\\LINKEDIN\\profile\\profile{no}.html", encoding="utf8"), "html.parser")
                
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
                    "website"   :website
                })

            self.result = ret

        return self.result


    def start(self):
        Helper.delete_create()
        self.getData()
        self.getProfile()
        data = self.script_profile()
        Excel.export_pandas(data)
        
        
        
        
if __name__ == "__main__":
    obJH = Linkedin(1,2)
    obJH.start()
