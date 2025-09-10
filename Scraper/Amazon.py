#Scraper for Amazon
from bs4 import BeautifulSoup as bs
import requests as rq
import re
import random
import time
from Helpers.Standardise import standardiseModel
from Helpers.ShortenURL import shorten
from Helpers.GetVRAM import getVram

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
]

HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "DNT": "1",
}

def getHeaders():
    return {
        **HEADERS,
        "User-Agent": random.choice(USER_AGENTS)
    }
referer = None

def findProduct(productName, limit = 20): #Takes in a string productName to search
    #Headers and URL
    with rq.Session() as session:
        session.headers.update(getHeaders())
        URL = f"https://www.amazon.sg/s?k=\"{str(productName)}\""

        #Get Webpage soup
        webpage = session.get(URL)
        logger.info(f"webpage: {webpage}")
        soup = bs(webpage.content, 'html.parser')
        
        #Get Product Page soup
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-line-clamp-4 s-link-style a-text-normal'})
        logger.info(f"links found: {len(links)}")
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
            productLink = shorten(f'https://www.amazon.sg{href}')
            if productLink in seen_links:
                continue
            
            session.headers.update(getHeaders())
            productPage = session.get(productLink, headers={'Referer': referer})
            productPage.raise_for_status()
            productSoup = bs(productPage.content, 'html.parser')

            priceWhole = productSoup.find("span", attrs={"class": "a-price-whole"})
            priceFraction = productSoup.find("span", attrs={"class": "a-price-fraction"})
            if priceWhole is None or priceFraction is None:
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

                cleanedPriceWhole = re.sub(r'[^\d]', '', priceWhole.get_text(strip=True)) #remove non digits from price strings
                cleanedPriceFraction = re.sub(r'[^\d]', '', priceFraction.get_text(strip=True))
                cleanedPrice = ".".join([cleanedPriceWhole, cleanedPriceFraction])
                
                data['Price'] = round(float(cleanedPrice), 2) #convert to float 2dp

                data['Link'] = productLink
                
                data['Title'] = title

                #Locate its image link if possible too
                imageTag = productSoup.find('img', attrs={'id': "landingImage"})
                if imageTag:
                    data['ImageLink'] = imageTag.get("src") or imageTag.get("data-old-hires")
                else:
                    data["ImageLink"] = None

                seen_links.append(data['Link'])
                productInfos.append(data)
            
        except Exception as e:
            logger.error(f"Error processing {href}: {str(e)}")
            continue

    return productInfos



