#Scraper for Amazon

from bs4 import BeautifulSoup as bs
import requests as rq
from Standardise import standardiseModel

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
        for product in products:
            if productName.upper() in product["Model"]:
                print(product)

def processLinks(links, session, referer=None):
    productInfos = []
    for link in links:
        href = link.get('href') 
        if href is None:
            continue

        try:
            productLink = f'https://www.amazon.sg{href}'
            productPage = session.get(productLink, headers={'Referer': referer})
            productPage.raise_for_status()
            productSoup = bs(productPage.content, 'html.parser')

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
                    key = "VRAM"
                
                data[key] = value
            
            if data["Model"] and data["VRAM"]:
                title = productSoup.find("span", attrs={"class": "a-size-large product-title-word-break"}).get_text(strip=True)
                price = productSoup.find("span", attrs={"class": "aok-offscreen"}).get_text(strip=True)

                # data['Title'] = title
                # data['Link'] = productLink
                data['Price'] = price
                
                productInfos.append(data)
            
        except Exception as e:
            print(f"Error processing {href}: {str(e)}")
            continue

    return productInfos

findProduct("rtx 5070")

#'Model', 'Brand', 'VRAM', 'Price', 'Title', 'Link', 'Date'
# {Link, Date}



