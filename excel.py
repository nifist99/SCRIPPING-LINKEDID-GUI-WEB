
import xlsxwriter
import pandas as pd

class Excel:

    def export_pandas(data):
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
        writer = pd.ExcelWriter('output.xlsx')
        # write dataframe to excel
        df_marks.to_excel(writer)
        # save the excel
        writer.save()

        return 'DataFrame is written successfully to Excel File.'