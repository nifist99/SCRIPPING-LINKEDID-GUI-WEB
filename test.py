from linkedin_api import Linkedin

api = Linkedin('harikarinjani@gmail.com', 'November101121')

contact_info = api.get_profile('bunga-anggrit-septyana-53302317b')

print(contact_info)