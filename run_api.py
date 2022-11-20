import pathlib
from os.path import exists
from bs4 import BeautifulSoup
import glob
import os
import requests
import json
from api.api_web import Api
from module.scripping_api import Scrap_API
from module.setting import Config
import chromedriver_autoinstaller
from module.excel import Excel


path = pathlib.Path(__file__).parent.resolve()

def main():

    #install chroem driver if not exist
    chromedriver_autoinstaller.install()

    print('#*********** INI ADALAH METODE SCRIPT GET HTML dan API LINKEDIN ***************#')
    print("")

    code   = input('masukan code scryping check di website =') 

    #menghapus semua file html

    folder = f"{path}\public\{code}"
    Config.delete_create(folder)

    #delete transpool
    Api.transpool_delete()

    result = Api.setting(code)

    if result['status'] == 'success':
        #MENYIMPAN LIST PAGINATE
        scrap = Scrap_API(path,result['code'],result['username'],result['sandi'],result['url'],result['kategori'],result['start'],result['end'],result['max'])

        scrap.scrap_api_url()
        #delete transpool
        Api.transpool_delete()

        Config.delete_create(folder)

    else:
        print()
        print()
        print('#*********** KODE TIDAK DITEMUKAN CHECK LAGI DI WEB ***************#')
        print(result)
        exit()

if __name__ == "__main__":

    main()