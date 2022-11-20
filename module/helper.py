
from linkedin_scraper import Person,Company
import pyautogui
import time
import os
import shutil
import pathlib

class Helper:

    def id_profile(url : str):

        split_ul = url.split('?')
        result = split_ul[0].split('/')

        return result[4]
    
    def url_overlay(url : str):

        split_ul = url.split('?')

        return split_ul[0]

    def exist_html(directory):

        file_path = os.path.normpath(directory)

        if os.path.isfile(file_path):
                return "success"

        else:

                return "failed"

    def checkFileExist(directory):
        timeout=360
        file_path = os.path.normpath(directory)
        attempts = 0
        while attempts < timeout:
            # Check if the file exists.
            if os.path.isfile(file_path):
                return
            # Wait 1 second before trying again.
            time.sleep(1)
            attempts += 1 

    def save(name):
        # To simulate a Save As dialog. You can remove this since you'll be saving/downloading a file from a link
        pyautogui.hotkey('ctrl', 's')
        # Wait for the Save As dialog to load. Might need to increase the wait time on slower machines
        time.sleep(2)
        #to get the current working directory
        # File path + name
        path = pathlib.Path(__file__).parent.resolve()
        FILE_NAME   = f"{path}\html\{name}"
        direct      = f"{path}\html\{name}"
        # Type the file path and name is Save AS dialog
        pyautogui.typewrite(FILE_NAME)
        #Hit Enter to save
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(2)

        check = Helper.checkFileExist(direct)

        if check is True:

            time.sleep(3)

            return True

    def saveprofile(name):
        # To simulate a Save As dialog. You can remove this since you'll be saving/downloading a file from a link
        pyautogui.hotkey('ctrl', 's')
        # Wait for the Save As dialog to load. Might need to increase the wait time on slower machines
        time.sleep(2)
        #to get the current working directory
        # File path + name
        path = pathlib.Path(__file__).parent.resolve()

        FILE_NAME   = f"{path}\profile\{name}"
        direct      = f"{path}\profile\{name}"
        # Type the file path and name is Save AS dialog
        pyautogui.typewrite(FILE_NAME)
    
        #Hit Enter to save
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(2)

        check = Helper.checkFileExist(direct)

        if check is True:
            
            time.sleep(3)
            
            return True

    
    def delete_create():
        dir_html    = os.getcwd()+'/html'
        dir_profile = os.getcwd()+'/profile'
        shutil.rmtree(dir_html)
        shutil.rmtree(dir_profile)

        # create new folder
        try: 
            os.mkdir(dir_html) 
            os.mkdir(dir_profile) 

            return True
        except OSError as error: 
            print(error)  

            return False

    def api_contact(key):

        if key['email_address'] is  None:
            email = 'N/A'
        else:
            email = key['email_address']

        if len(key['phone_numbers']) ==0:
            phone = 'N/A'
        else:
            phone = key['phone_numbers'][0]['number']

        if len(key['websites']) == 0:
            web = 'N/A'
        else:
            web = key['websites'][0]['url']

        return {
            'email':email,
            'phone':phone,
            'web'  : web
        }

    def api_profile(key):

        pengalaman = ''
        if len(key['experience']) != 0:
            for ex in key['experience']:
                try:
                    c = ex['companyName']
                except:
                    c = 'N/A'

                try:
                    t = ex['companyName']
                except:
                    t = 'N/A'

                try:
                    p = ex['companyName']
                except:
                    p = 'N/A'


                pengalaman += f"(PT{c} JABATAN {t} PERIODE {p})\n"

        try:
            tentang = key['summary']
        except:
            tentang = 'N/A'

        try:
            jabatan = key['headline']
        except:
            jabatan = 'N/A'

        try:
            nama = f"{key['firstName']} {key['lastName']}"
        except:
            nama = 'N/A'

        return {
            'nama'    : nama,
            'tentang' : tentang,
            'jabatan' : jabatan,
            'pengalaman': pengalaman
        }