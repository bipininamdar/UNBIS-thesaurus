from bs4 import BeautifulSoup
import requests
import re
import pickle
import os
import pandas
import logging

data_location = "Z:\\DATA\\World Food Programme\\UNBIS"
headers={"Accept":"text/html"}
list_of_languages = pickle.load(open(os.path.join(data_location, "compile jsons\\data tables\\list_of_languages.p"), "rb"))

logfile = "Z:\\DATA\\World Food Programme\\UNBIS\\compile jsons\\log file - descriptions not in JSONs.log"

def get_description(url):

    try:
        page = requests.get(url, headers = headers)
        page_content = page.content
        soup = BeautifulSoup(page_content, 'html.parser')

        for div in soup.find('div', attrs={"class":"row h4"}):
            return div.string
    except:
        logging.basicConfig(filename=logfile, level=logging.WARNING, format='%(message)s')
        logging.warning(url)
        return ""

if __name__ == "__main__":

    all_links = pickle.load(open(os.path.join(data_location, "compile jsons\\all_links.p"), "rb"))
    downloaded_links = pickle.load(open(os.path.join(data_location, "compile jsons\\downloaded_links.p"), "rb"))
    downloaded_files = pickle.load(open(os.path.join(data_location, "compile jsons\\downloaded_files.p"), "rb"))

    downloaded_files2 = set()
    for file in downloaded_files:
        downloaded_files2.add(file.replace('.json', '?lang=en'))

    links_without_json = all_links.difference(downloaded_files2)

    description_data = pandas.DataFrame({'id':[], 'Synonyms':[], 'Hypernym': [], '@language':[]})

    for link in links_without_json:

        print(link)
        if len(link) > 43:
            parent = link[33:35]
        else:
            parent = ""
        for language in list_of_languages:
            print(language)
            description_data = description_data.append({'id': str(link.split('/')[-1].replace('?lang=en', '')), 'Synonyms':str(get_description(link.replace('?lang=en', '?lang='+language))), 'Hypernym': str(parent), '@language': str(language)}, ignore_index=True)

    pickle.dump(description_data, open(os.path.join(data_location, "compile jsons\\data tables\\links_without_JSON_descriptions.p"), "wb"))