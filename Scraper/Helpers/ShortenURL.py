import re
from urllib.parse import unquote

def shorten(link):
    
    link = link.strip()

    # Case 1: Amazon SSPA link (with encoded URL)
    sspa_pattern = r'^(https:\/\/[^\/]+)\/sspa\/click\?.*?url=([^&]+)'
    match = re.search(sspa_pattern, link)
    if match:
        base_url = match.group(1)
        decoded_path = unquote(match.group(2))
        # extract only up to /dp/ASIN
        clean_match = re.search(r'^([^?]*?/dp/[^\/]+)', decoded_path)
        if clean_match:
            return base_url + clean_match.group(1)
        return base_url + decoded_path.split('?')[0]  # fallback

    # Case 2: Normal Amazon product URL
    product_pattern = r'^(https:\/\/[^\/]+\/[^\/]+\/dp\/[^\/]+)'
    match = re.search(product_pattern, link)
    if match:
        return match.group(1)

    # Fallback: remove query string
    return link.split('?')[0]
