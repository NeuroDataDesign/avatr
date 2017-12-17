import sys
import requests
from bs4 import BeautifulSoup as bs
#dynamic scraping boiz!!!
import time
from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

import pickle

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
    time.sleep(1) #wait for .25 seconds(kind of jank)
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
                    browser.get(data[scan][dataset][derivative])
                    time.sleep(1) #wait for .25 seconds(kind of jank)
                    innerHTML = browser.execute_script("return document.body.innerHTML")
                    soup = bs(innerHTML, 'lxml')
                    #links = [[link.text,data[scan][dataset][derivative]+link['href']]\
                    #for link in soup.find_all('a')[1:]]
                    links = [[link.text,data[scan][dataset][derivative]+link['href']]\
                              for link in soup.find_all('a')[1:]]
                    data[scan][dataset][derivative] = links
                    '''
                    for link in links:
                        if 's3' not in link[1]:
                            print(link[1])
                            browser.get(link[1])
                            time.sleep(.5) #wait for .25 seconds(kind of jank)
                            innerHTML = browser.execute_script("return document.body.innerHTML")
                            soup2 = bs(innerHTML, 'lxml')
                            dublinks = [[dublink.text,dublink['href']]\
                                     for dublink in soup2.find_all('a')[1:]]
                            data[scan][dataset][derivative+'.'+link[0]] = dublinks
                        else:
                            data[scan][dataset][derivative] = links
                            break
                    '''
    browser.close()
    print("CLOSED")

    return data

def dive_deeper(data):
    data2 = data
    browser = webdriver.Chrome()
    print("STARTING SESSION")
    for scan in data2.keys():
        for dataset in data2[scan].keys():
            for derivative in data2[scan][dataset].keys():
                for link in data2[scan][dataset][derivative]:
                    if link[1][-1] == '/':
                        browser.get(link[1])
                        time.sleep(1) #wait for .25 seconds(kind of jank)
                        innerHTML = browser.execute_script("return document.body.innerHTML")
                        soup = bs(innerHTML, 'lxml')
                        link[1] = [[link2.text,link2['href']]\
                                   for link2 in soup.find_all('a')[1:]]
    browser.close()
    print('CLOSED')
    for scan in data.keys():
        for dataset in data2[scan].keys():
            for derivative in data2[scan][dataset].copy():
                #print('DERIVATIVE ______ ' + str(derivative) + ': ' + str(len(derivative)))
                #print(data2[scan][dataset][derivative][0][0])
                if len(data2[scan][dataset][derivative][0])>0 and data2[scan][dataset][derivative][0][0][-1] == '/':
                    for subderivative in data2[scan][dataset][derivative]:
                        #print('...~~~~~~~~~~~...')
                        #print(subderivative)
                        data2[scan][dataset][derivative+'.'+subderivative[0][:-1]] = subderivative[1]
                    data2[scan][dataset].pop(derivative)
    return data2

def notebook():
    scrape = m2g_scrape('https://m2g.io')
    data = m2g_data_scrape(scrape)
    data2 = dive_deeper(data)
    for scan in data.keys():
        #print(key + '--------------')
        #print(scrape[key])
        for dataset in data[scan].keys():
            print(dataset + ':~~~~')
            for derivative in data[scan][dataset].keys():
                print(derivative)
                for link in data[scan][dataset][derivative][:5]:
                    print('   ~~ ' + str(link))
    return data

if __name__ == '__main__':
    scrape = m2g_scrape('https://m2g.io')
    #data = m2g_data_scrape({'FMRI':scrape['FMRI']})
    data = m2g_data_scrape(scrape)
    data2 = dive_deeper(data)
    data2['FMRI']['NKI1']['Preproc Images'] = data2['FMRI']['NKI1'].pop('Preproc. Images')
    #print(scrape['DWI']['BNU1']['Aligned Images'])
    pickle.dump( data2, open( "data.p", "wb" ) )
    for scan in data2.keys():
        #print(key + '--------------')
        #print(scrape[key])
        for dataset in data2[scan].keys():
            print(dataset + ':~~~~')
            for derivative in data2[scan][dataset].keys():
                print(derivative)
                for link in data2[scan][dataset][derivative][:5]:
                    print('   ~~ ' + str(link))
