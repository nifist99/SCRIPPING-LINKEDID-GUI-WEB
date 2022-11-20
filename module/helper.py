
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