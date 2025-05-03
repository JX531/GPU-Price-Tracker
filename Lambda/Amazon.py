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

def findProduct(productName, limit = 10): #Takes in a string productName to search
    #Headers and URL
    with rq.Session() as session:
        session.headers.update(HEADERS)
        URL = f"https://www.amazon.sg/s?k=\"{str(productName)}\""

        #Get Webpage soup
        webpage = session.get(URL)
        soup = bs(webpage.content, 'html.parser')
        
        #Get Product Page soup
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-line-clamp-4 s-link-style a-text-normal'})

        products = processLinks(links[:limit], session, webpage.url)
        
        return [product for product in products if productName == product["Model"]]

def processLinks(links, session, referer=None):
    productInfos = []
    seen_links = [] #to remove duplicate listings by their link
    for link in links:
        href = link.get('href') 
        if href is None:
            continue

        try:
            productLink = f'https://www.amazon.sg{href}'
            productPage = session.get(productLink, headers={'Referer': referer})
            productPage.raise_for_status()
            productSoup = bs(productPage.content, 'html.parser')

            price = productSoup.find("span", attrs={"class": "aok-offscreen"})
            if price is None:
                continue

            table = productSoup.find('table', attrs={"class": "a-normal a-spacing-micro"})
            if table is None:
                continue
                
            data = {}
            
            #extract only model, brand, vram
            for i, row in enumerate(table.find_all('tr')):
                if i >= 3:  #stop after top 3 rows
                    break
                key = row.find('td', attrs={"class": "a-span3"}).get_text(strip=True)
                value = row.find('td', attrs={"class": "a-span9"}).get_text(strip=True)
                
                # Rename keys
                if key == "Graphics co-processor":
                    value = standardiseModel(value)
                    key = "Model"
                
                elif key == "Graphics RAM size":
                    value = getVram(value)
                    key = "VRAM"
                
                data[key] = value
            
            if data["Model"] and data["VRAM"]:
                title = productSoup.find("span", attrs={"class": "a-size-large product-title-word-break"}).get_text(strip=True)

                cleanedPrice = re.sub(r'[^\d.]', '', price.get_text(strip=True)) #remove non digits from price string
                data['Price'] = round(float(cleanedPrice), 2) #convert to float 2dp

                data['Link'] = shorten(productLink)
                
                data['Title'] = title

                if data['Link'] not in seen_links:
                    seen_links.append(data['Link'])
                    productInfos.append(data)
            
        except Exception as e:
            logger.error(f"Error processing {href}: {str(e)}")
            continue

    return productInfos



