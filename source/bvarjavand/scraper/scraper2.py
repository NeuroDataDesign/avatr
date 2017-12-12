import sys
import requests
from bs4 import BeautifulSoup as bs
#dynamic scraping boiz!!!
import time
from selenium import webdriver

def m2g_scrape(url): #returns a dictionary
    #{'DWI' : {'BNU1':{'Aligned Images':'link',
    #                  'Tensors':'link',
    #                   ...},
    #          'BNU3':{'Aligned Images':'link',
    #                   'Tensors':'link',
    #                   ...},
    #           ...},
    # 'FMRI': {...}}
    #Indexing: scrape['DWI']['BNU1']['Tensors'] = 'link'
    #scrape
    browser = webdriver.Chrome()
    print("STARTING SESSION")
    browser.get(url) #navigate to the page
    print("OPENED")
    time.sleep(.25) #wait for .25 seconds(kind of jank)
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    print("SCRAPED")
    browser.close()
    print("CLOSED")
    #soupify
    soup = bs(innerHTML, 'lxml')
    #organize soup
    scrape = {}
    tables = soup.find_all('tbody') #this part kinda jank
    tables = [x for x in tables if len(x.text)>100] #don't look at me
    dwi = tables[0]
    #DWI
    dwi_dict = {}
    for row in dwi.find_all('tr'):
        if len(row.find_all('a')) > 0:
            row_dict = {}
            elements = row.find_all('a')
            for element in elements[1:]:
                if 'csv' not in element.text and 'github' not in element['href']:
                    row_dict[element.text] = element['href']
            if len(row_dict) > 0:
                dwi_dict[elements[0].text] = row_dict

    fmri = tables[1]
    #FMRI
    fmri_dict = {}
    for row in fmri.find_all('tr'):
        if len(row.find_all('a')) > 0:
            row_dict = {}
            elements = row.find_all('a')
            for element in elements[1:]:
                if 'csv' not in element.text and 'github' not in element['href']:
                    row_dict[element.text] = element['href']
            if len(row_dict) > 0:
                fmri_dict[elements[0].text] = row_dict

    scrape['DWI'] = dwi_dict
    scrape['FMRI'] = fmri_dict
    return scrape

def m2g_data_scrape(scrape): #converts links to s3, to list of links to data
    data = scrape#saves scrape for something else potentially
    browser = webdriver.Chrome()
    print("STARTING SESSION")

    for scan in data.keys(): #DWI and FMRI
        for dataset in data[scan].keys(): #BNU1,BNU3,...
            for derivative in data[scan][dataset].keys(): #Aligned Images, Fibers, Graphs...
                #print(scan, dataset, derivative, '~~~~~~~~~~~')
                #print(data[scan][dataset][derivative])
                if 'http' in data[scan][dataset][derivative]:
                    browser.get(data[scan][dataset][derivative]) #navigate to the page
                    #print("OPENED")
                    time.sleep(.25) #wait for .25 seconds(kind of jank)
                    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
                    #print("SCRAPED")

                    soup = bs(innerHTML, 'lxml')#soupify
                    links = [[link.text,link['href']] for link in soup.find_all('a') if 's3' in link['href']]
                    data[scan][dataset][derivative] = links

    browser.close()
    print("CLOSED")

    return data

if __name__ == '__main__':
    scrape = m2g_scrape('https://m2g.io')
    data = m2g_data_scrape(scrape)
    #print(scrape['DWI']['BNU1']['Aligned Images'])
    for scan in data.keys():
        #print(key + '--------------')
        #print(scrape[key])
        for dataset in data[scan].keys():
            print(dataset + ':~~~~')
            for derivative in data[scan][dataset].keys():
                print(derivative)
                for link in data[scan][dataset][derivative][:5]:
                    print('   ~~ ' + str(link))
