import pathlib

from os.path import exists

from bs4 import BeautifulSoup

import glob

import os

path = pathlib.Path(__file__).parent.resolve()

path_html        = f"{path}\html"
path_profile     = f"{path}\profile"


def main():

    # This is our counter
    count = 0

    # Notice r'' raw string to preserve literal backslash
    for file in os.listdir(path_profile):
        if(file.endswith('html')):
            print(file)
            count += 1

    print('Total:', count)

if __name__ == "__main__":

    main()