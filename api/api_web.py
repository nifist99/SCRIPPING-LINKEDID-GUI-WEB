
import requests
import json

base_url = 'http://127.0.0.1:8000/api'

class Api:

    def setting(code):
        try:
            url = f'{base_url}/show/{code}'

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            r = response.json()

            return r
        except:
            return Api.check_result(code)

    def save_list(link,folder,code):
        try:
            url = f"{base_url}/save/result"

            payload = json.dumps({
            "link": link,
            "folder": folder,
            "code": code
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            return response.json()
        except:
            return Api.save_list(link,folder,code)

    def update_get_profile(url_overlay,html_profile,link,code):
        try:
            url = f"{base_url}/update/get/profile"

            payload = json.dumps({
                "link": link,
                "url_overlay": url_overlay,
                "code": code,
                "html_profile":html_profile
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            return response.json()
        except:
            return Api.update_get_profile(url_overlay,html_profile,link,code)

    def check_result(url_overlay):
        try:
            url = f"{base_url}/result/detail"

            payload = json.dumps({
                "url": url_overlay,
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            return response.json()
        except:
            return Api.check_result(url_overlay)

    
    def url_list(url_profile):
        try:
            url = f"{base_url}/result/check/url"

            payload = json.dumps({
                "url": url_profile,
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            return response.json()
        except:
            return Api.check_result(url_profile)

    def transpool_delete():
        try:
            url = f"{base_url}/transpool/delete"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            return response.json()
        except:
            return Api.transpool_delete()

    
    def transpool_create(code,url_profile,url_overlay,html,html_profile):
        try:
            url = f"{base_url}/transpool/create"

            payload = json.dumps({
                "code"          : code,
                "url_profile"   : url_profile,
                "url_overlay"   : url_overlay,
                "html"          : html,
                "html_profile"  : html_profile
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            return response.json()
        except:
            return Api.transpool_create(url_profile,url_overlay,html,html_profile)

    def transpool_all():
        try:
            url = f"{base_url}/transpool"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            return response.json()
        except:
            return Api.transpool_delete()


    def result_update(key):
        try:
                url = f"{base_url}/result/update"
                payload = json.dumps({
                    "url_overlay": key['url_overlay'] ,
                    "nama"       : key['nama'],
                    "jabatan"    : key['jabatan'],
                    "tentang"    : key['tentang'],
                    "hp"         : key['hp'],
                    "email"      : key['email'],
                    "link"       : key['link'],
                    "web"        : key['web'],
                    "pengalaman" : key['pengalaman']
                })
                headers = {
                'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(key['nama'])
                print('save profile api run')
                return response.json()

        except:
            return Api.result_update(key)

        
    def save(key):
        try:
                url = f"{base_url}/result/save"
                payload = json.dumps({
                    "url_profile"   : key['url_profile'],
                    "folder"        : key['code'],
                    "html_profile"  : key['id_profile'],
                    "url_overlay"   : key['url_overlay'] ,
                    "nama"          : key['nama'],
                    "jabatan"       : key['jabatan'],
                    "tentang"       : key['tentang'],
                    "hp"            : key['hp'],
                    "email"         : key['email'],
                    "link"          : key['link'],
                    "web"           : key['web'],
                    "pengalaman"    : key['pengalaman']
                })
                headers = {
                'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(key['nama'])
                print('save profile api run')
                return response.json()

        except:
            return Api.result_update(key)       