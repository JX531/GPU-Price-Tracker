#Scraper for Amazon
from bs4 import BeautifulSoup as bs
import requests as rq
import re
from Helpers.Standardise import standardiseModel
from Helpers.ShortenURL import shorten
from Helpers.GetVRAM import getVram

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

userAgent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
language = 'en-US, en;q=0.5'
HEADERS = ({'User-Agent': userAgent, 'Accept-Language': language})
referer = None

def findProduct(productName, limit = 10): 
    '''
    Searches for products on amazon.sg and extracts relevant information
    Inputs : 
    productName - A string for the product you want to search e.g "RTX 5070"
    limit - Integer, limit on how many product listings you want to process

    Output : An array of objects, each containing information of a single listing of the product
    '''

    with rq.Session() as session:
        session.headers.update(HEADERS) #update HEADERS
        URL = f"https://www.amazon.sg/s?k=\"{str(productName)}\"" #generate URL to search for product on amazon.sg

        #get Webpage soup
        webpage = session.get(URL)
        logger.info(f"Status: {webpage}") #Status of webpage e.g 200
        soup = bs(webpage.content, 'html.parser')
        
        #get links to all product listings found
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-line-clamp-4 s-link-style a-text-normal'})
        logger.info(f"Links Found: {len(links)}") #how many links were found during search

        products = processLinks(links[:limit], session, webpage.url) #extract product information
        
        return [product for product in products if productName == product["Model"]] #return products with models that match only what you are searching for

def processLinks(links, session, referer=None):
    '''
    Takes in an array of links to product listings, and extracts information for each one
    Input : An array of links from findProduct()
    Output : An array of objects, each containing information of a single listing of the product
    '''
    productInfos = [] #array to store info
    seen_links = [] #to remove duplicate listings by their link

    for link in links:
        href = link.get('href')  #extract href
        if href is None:
            continue

        try:
            productLink = f'https://www.amazon.sg{href}' #form the link to product listing

            #Get product soup
            productPage = session.get(productLink, headers={'Referer': referer})
            productPage.raise_for_status()
            productSoup = bs(productPage.content, 'html.parser')

            price = productSoup.find("span", attrs={"class": "aok-offscreen"}) #find the price
            if price is None:
                continue

            table = productSoup.find('table', attrs={"class": "a-normal a-spacing-micro"}) #find table that contains information such as Model
            if table is None:
                continue
                
            data = {} #to store data of the current product listing
            
            #extract only model, brand, vram which are the top 3 rows in table
            for i, row in enumerate(table.find_all('tr')):
                if i >= 3:  #stop after top 3 rows
                    break
                
                #get key and value of each row
                key = row.find('td', attrs={"class": "a-span3"}).get_text(strip=True) 
                value = row.find('td', attrs={"class": "a-span9"}).get_text(strip=True)
                
                #Rename keys
                if key == "Graphics co-processor":
                    value = standardiseModel(value) #standardise the model format
                    key = "Model"
                
                elif key == "Graphics RAM size":
                    value = getVram(value) #standardise the VRAM format
                    key = "VRAM"
                
                data[key] = value #set the values
            
            if data["Model"] and data["VRAM"]: #if it has both model and vram attributes
                title = productSoup.find("span", attrs={"class": "a-size-large product-title-word-break"}).get_text(strip=True) #find title

                cleanedPrice = re.sub(r'[^\d.]', '', price.get_text(strip=True)) #remove non digits from price string
                data['Price'] = round(float(cleanedPrice), 2) #convert to float 2dp

                data['Link'] = shorten(productLink) #shorten the product link
                
                data['Title'] = title 

                #Locate its image link if possible too
                imageTag = productSoup.find('img', attrs={'id': "landingImage"})
                if imageTag:
                    data['ImageLink'] = imageTag.get("src") or imageTag.get("data-old-hires")
                else:
                    data["ImageLink"] = "https://d3pprnqmx0m8l1.cloudfront.net/data/dailyCheapest/GPU_Placeholder.jpg"

                if data['Link'] not in seen_links: #not a duplicate
                    #append data
                    seen_links.append(data['Link'])
                    productInfos.append(data)
            
        except Exception as e:
            logger.error(f"Error processing {href}: {str(e)}")
            continue

    return productInfos



