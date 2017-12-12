import sys
import requests
from bs4 import BeautifulSoup as bs
#dynamic scraping boiz!!!
import time
from selenium import webdriver
#cheating a little with URLs
#looking at m2g.io, we have these repos
url_dwi = "https://raw.githubusercontent.com/neurodata/mri.neurodata.io/master/table_dwi.html"
url_fmri = "https://raw.githubusercontent.com/neurodata/mri.neurodata.io/master/table_fmri.html"
###########
#GEN LINKS#
###########
def gen_data_links(url):
    website = requests.get(url_dwi).text
    soup = bs(website, 'html.parser')
    names=[]
    links=[]
    for td in soup.find_all('td'):
        name = td.text.strip()
        link = td.find('a')['href']
        if link not in links:
            names.append(name)
            links.append(link)
    scrapes = []
    for i in range(len(names)):
        scrape = {}
        scrape['name'] = names[i]
        scrape['link'] = links[i]
        scrapes.append(scrape)
    return scrapes

#assuming there is a dataset location not in s3, and a csv
def sort_data_links(data_links):
    datasets = []
    dataset={}
    for link in data_links:
        if 's3' not in link['link'] and 'git' not in link['link']:
            datasets.append(dataset)
            dataset = {}
        dataset[link['name']] = link['link']
    return datasets[1:]

##############
#SCRAPE LINKS#
##############
import time
from selenium import webdriver

#populates data with anything it can find
def dynamic_scrape(data):
    newdata = []
    for group in data:
        newgroup = {}
        browser = webdriver.Chrome()
        print("STARTING SESSION")
        for link in group:
            newgroup[link] = group[link]
            print(link + ': ' + group[link])
            if 's3' in group[link] and 'csv' not in group[link] and 'git' not in group[link]:
                browser.get(group[link]) #navigate to the page
                print("OPENED")
                time.sleep(.1) #wait for .1 seconds(kind of jank)
                innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
                print("SCRAPED")
                inner_soup = bs(innerHTML, 'lxml')
                data_links = inner_soup.find_all('a')
                sorted_data_links = []
                for single in data_links:
                    sorted_data_links.append([single.text, single['href']])
                newgroup[link+'_scrape'] = sorted_data_links[1:]
        browser.close()
        print("CLOSED")
        newdata.append(newgroup)
    return newdata

def scrape_m2g(url):
    temp = gen_data_links(url)
    data = sort_data_links(temp)
    newdata = dynamic_scrape(data)
    return newdata

if(__name__=='__main__'):
    dwi = scrape_m2g(url_dwi)
    for piece in dwi:
        print(piece.keys())
