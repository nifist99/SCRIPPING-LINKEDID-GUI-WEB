import pathlib
from os.path import exists
from bs4 import BeautifulSoup
import glob
import os
import requests
import json
from api.api_web import Api
from module.scrapping import Scrap
from module.setting import Config
import chromedriver_autoinstaller
from module.excel import Excel


path = pathlib.Path(__file__).parent.resolve()

def main():

    #install chroem driver if not exist
    chromedriver_autoinstaller.install()

    code   = input('masukan code scryping check di website = ?\n') 

    print('#*********** PILIH METODE FILTER ***************#')
    print('KETIK 1 (BY KATEGORI)')
    print('KETIK 2 (BY URL FILTER)')
    print('#*********** PILIH ANGKA 1 / 2 ***************#')

    metode = int(input('Enter a number: '))

    #menghapus semua file html

    folder = f"{path}\public\{code}"
    Config.delete_create(folder)

    #delete transpool
    Api.transpool_delete()

    result = Api.setting(code)

    if result['status'] == 'success':
        #MENYIMPAN LIST PAGINATE
        scrap = Scrap(path,result['code'],result['username'],result['sandi'],result['url'],result['kategori'],result['start'],result['end'],result['max'])

        if metode == 1:
            r = scrap.scrap_kategori()
        elif metode ==2:
            r = scrap.scrap_filter_url()
        else:
            print("")
            print("")
            print('#*********** PASTIKAN MASUKAN ANGKA DENGAN BENAR ***************#')

            exit()
            
        
        for key in r:

            api_test=Api.save_list(key['link'],key['folder'],key['code'])
            print(api_test)

        scrap.get_profile()

        excel_data = scrap.script_profile()

        # export to excel
        name = f"{result['code']}.xlsx"
        ex = Excel.export_pandas(excel_data,name,path)

        print(ex)

        #delete transpool
        Api.transpool_delete()

        Config.delete_create(folder)

    else:

        print(result)

if __name__ == "__main__":

    main()