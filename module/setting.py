import requests
import json
import pyautogui
import time
import os
import shutil
import pathlib

class Config:

    def checkFileExist(directory):
        timeout=1000
        file_path = os.path.normpath(directory)
        attempts = 0
        while attempts < timeout:
            # Check if the file exists.
            if os.path.isfile(file_path):
                return
            # Wait 1 second before trying again.
            time.sleep(1)
            attempts += 1 

    def save(folder,name):
        # To simulate a Save As dialog. You can remove this since you'll be saving/downloading a file from a link
        pyautogui.hotkey('ctrl', 's')
        # Wait for the Save As dialog to load. Might need to increase the wait time on slower machines
        time.sleep(2)
        #to get the current working directory
        FILE_NAME   = f"{folder}\{name}"
        direct      = f"{folder}\{name}"
        # Type the file path and name is Save AS dialog
        pyautogui.typewrite(FILE_NAME)
        #Hit Enter to save
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(2)

        check = Config.checkFileExist(direct)
        if check is True:
            time.sleep(3)
            return True
    
    def delete_create(folder):

        isExistHTML     = os.path.exists(f"{folder}\html")
        isExistPROFILE  = os.path.exists(f"{folder}\profile")

        if isExistPROFILE:
            dir_profile = folder+'\profile'
            shutil.rmtree(dir_profile)

        if isExistHTML:
            dir_html    = folder+'\html'
            shutil.rmtree(dir_html)

        return True
            

    def userAgent():
        headers_list = [
            # Firefox 77 Mac
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            },
            # Firefox 77 Windows
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            },
            # Chrome 83 Mac
            {
                "Connection": "keep-alive",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Dest": "document",
                "Referer": "https://www.google.com/",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
            },
            # Chrome 83 Windows 
            {
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Referer": "https://www.google.com/",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9"
            }
        ]

        return headers_list
# MASUKAN EMAIL DAN PASSWORD DISINI