import os
from bs4 import BeautifulSoup
import pickle
import wget
import requests

data_location = "Z:\\DATA\\World Food Programme\\UNBIS"
url = "http://metadata.un.org/thesaurus/categories?lang=en"
headers={"Accept":"text/html"}

# Extract all links from a given page
def extract_links(url, hierarchy):

    print("Processing link : ", url)

    # import storages
    all_links = pickle.load(open(os.path.join(data_location, "compile jsons\\all_links.p"), "rb"))
    downloaded_links = pickle.load(open(os.path.join(data_location, "compile jsons\\downloaded_links.p"), "rb"))
    downloaded_files = pickle.load(open(os.path.join(data_location, "compile jsons\\downloaded_files.p"), "rb"))

    # make sure that the current input url has not already been extracted from
    temp_downloaded_links = downloaded_links.copy()
    temp_downloaded_links.add(url)
    if temp_downloaded_links == downloaded_links:
        return

    if url in hierarchy:
        return

    hierarchy.append(url)
    print("Downloading link: " + url)

    # if this is a new URL, fetch the page contents
    page = requests.get(url, headers = headers)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')

    # find links to other pages
    for link in soup.find_all('a'):
        # fail safe
        if link.get('href') == None:
            continue
        # identify and download relevant links

        if ("http://metadata.un.org/thesaurus/" in link.get('href') and "?lang=en" in link.get('href')):

            all_links.add(link.get('href'))

        if ("metadata.un.org/thesaurus/" in link.get('href') and "json" in link.get('href')):
            temp_downloaded_files = downloaded_files.copy()
            temp_downloaded_files.add(link.get('href'))
            if temp_downloaded_files == downloaded_files:
                continue
            # if not, download
            print("downloading file " + link.get('href'))
            wget.download(link.get('href'), os.path.join(data_location, 'jsondata'))
            downloaded_files.add(link.get('href'))

    print("Downloaded link : " + url)
    downloaded_links.add(url)

    # Save storages
    pickle.dump(downloaded_links, open(os.path.join(data_location, "compile jsons\\downloaded_links.p"), "wb"))
    pickle.dump(all_links, open(os.path.join(data_location, "compile jsons\\all_links.p"), "wb"))
    pickle.dump(downloaded_files, open(os.path.join(data_location, "compile jsons\\downloaded_files.p"), "wb"))

    # Iterate over the links found in current page
    for link in soup.find_all('a'):
        if link.get('href') == None:
            continue
        if ("http://metadata.un.org/thesaurus/" in link.get('href') and "?lang=en" in link.get('href')):
            if not(link.get('href') in downloaded_links) and not(link.get('href') in hierarchy):
                extract_links(link.get('href'), hierarchy)
                if len(hierarchy)>0:
                    hierarchy.pop()

def temp_reset_pickle_storages():
    downloaded_links = set()
    pickle.dump(downloaded_links, open(os.path.join(data_location, "compile jsons\\downloaded_links.p"), "wb"))

    all_links = set()
    pickle.dump(all_links, open(os.path.join(data_location, "compile jsons\\all_links.p"), "wb"))

    downloaded_files = set()
    pickle.dump(downloaded_files, open(os.path.join(data_location, "compile jsons\\downloaded_files.p"), "wb"))

if __name__ == "__main__":
    while True:
        try:
            all_links = pickle.load(open(os.path.join(data_location, "compile jsons\\all_links.p"), "rb"))
            downloaded_links = pickle.load(open(os.path.join(data_location, "compile jsons\\downloaded_links.p"), "rb"))

            for link in all_links.difference(downloaded_links):
                extract_links(link, list())

            if all_links == downloaded_links:
                break
        except RecursionError as error:
            continue