
import xlsxwriter
import pandas as pd
import pathlib
from os.path import exists

from api.api_web import Api

class Excel:

    def export_pandas(data,name,path):
        # create dataframe
        nama    = []
        jabatan = []
        tentang = []
        phone   = []
        email   = []
        link    = []
        experience = []
        website = []
        for key in data:

            nama.append(key['nama'])
            jabatan.append(key['jabatan'])
            tentang.append(key['about'])
            phone.append(key['phone'])
            email.append(key['email'])
            link.append(key['link'])
            website.append(key['website'])

            exp = ''
            for row in key['experience']:
                exp += f'( PT : {row["pt"]} > JABATAN : {row["jabatan"]} > MASA KERJA : {row["masa"]} )'

            experience.append(exp)

            update = {
                    'nama'       : key['nama'],
                    'jabatan'    : key['jabatan'],
                    'tentang'    : key['about'],
                    'hp'         : key['phone'],
                    'email'      : key['email'],
                    'link'       : key['link'],
                    'web'        : key['website'],
                    'pengalaman' : experience,
                    "url_overlay": key['url_overlay'],
                    }

            Api.result_update(update)

            # update data
            

        df_marks = pd.DataFrame(
                {'nama'     : nama,
                'jabatan'   : jabatan,
                'tentang'   : tentang,
                'phone'     : phone,
                'email'     : email,
                'link'      : link,
                'website'   : website,
                'pengalaman': experience
                }
            )

        # create excel writer object
        loc = f"{path}\export\{name}"
        writer = pd.ExcelWriter(loc)
        # write dataframe to excel
        df_marks.to_excel(writer)

        return 'DataFrame is written successfully to Excel File.'