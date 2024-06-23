import requests
from bs4 import BeautifulSoup


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        'accept-language': 'en-GB,en;q=0.9',
        'country': 'US',
    }
cookies = {
        "aep_usuc_f": "site=glo&c_tp=USD"
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
            my_dict["price"] = item.find('span', 'a-color-base').get_text()
        except:
            continue
        
        if rating > max_rating:
            max_rating = rating
            results[0] = my_dict
        if len(results) >= 20:
            break
    return results


def scrape_aliexpress(product_name):
    url = f"https://www.aliexpress.com/w/wholesale-{product_name.replace(' ', '-')}.html?spm=a2g0o.productlist.search.0"
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
    results = [{}]
    max_sold = 0
    for item in soup.select('.list--galleryWrapper--29HRJT4'):
        my_dict = {}
        my_dict["image_link"] = 'https:' +  item.find('img', 'images--item--3XZa6xf')['src']
        my_dict["title"] = item.find('h3', 'multi--titleText--nXeOvyr').get_text()
        temp = item.find('div', 'multi--price-sale--U-S0jtj').find_all('span')
        my_dict["price"] = temp[0].get_text() + temp[1].get_text() + temp[2].get_text() + temp[3].get_text() 
        if int(item.find('span', 'multi--trade--Ktbl2jB').get_text().split(' ')[0]):
            my_dict["number_of_sold"] = int(item.find('span', 'multi--trade--Ktbl2jB').get_text().split(' ')[0])
        else:
            continue
        print(my_dict)
        if max_sold < my_dict["number_of_sold"]:
            results[0] = my_dict
    
    return results
