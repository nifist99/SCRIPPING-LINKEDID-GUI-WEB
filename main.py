from run import main
from run_api import main_api
import os

def bot():
    print('#*********** WELCOME TO BOT LINKED IND ***************#')
    print("ini ada 2 metode by API DAN WEB")
    print()

    print("1 by api (lebih cepat max 1000 data per hari)")
    print("2 by web (lebih lambat max unlimited)")

    print

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


    bot()



