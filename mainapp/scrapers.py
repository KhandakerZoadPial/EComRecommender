import requests
from bs4 import BeautifulSoup


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        'accept-language': 'en-GB,en;q=0.9',
    }

def scrape_amazon(product_name):
    url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = [{}]
    max_rating = 0
    for item in soup.select('.s-main-slot .s-result-item'):
        my_dict = {

        }
        try:
            my_dict["title"] = item.select_one('h2 .a-text-normal').get_text()
            rating = int(item.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style').find('span', 'a-size-base s-underline-text').get_text())            
            my_dict["rating"] = rating
            my_dict ["star"] = float(item.find('span', 'a-icon-alt').get_text().split(' ')[0])
            my_dict["image_link"] = item.find('div', 'puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v36tmkogwwueb520kjutkllt0dc s-latency-cf-section puis-card-border').find('img', 's-image s-image-optimized-rendering')['src']
        except:
            continue
        
        if rating > max_rating:
            max_rating = rating
            results[0] = my_dict
        if len(results) >= 20:
            break
    return results
