__author__ = "Tao Zhang"
__copyright__ = "Copyright 2019, Zillow Scraper"
__email__ = "uncczhangtao@yahoo.com"

import requests
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup


def get_all_rent_house_url_by_zip(zip):
    # Initialize
    url_list_final, total_page = get_zillow_rental_by_page(zip)

    page = 1
    for i in range(0, total_page):
        url_list, total_page = get_zillow_rental_by_page(zip, i + 2)
        url_list_final.append(url_list)

    return url_list_final


def get_zillow_rental_by_page(zip, page=1):
    url_list = []

    url = 'https://www.zillow.com/homes/{0}_rb/rentals/{1}_p/'.format(zip, page)

    print("Downloading URL:{0}".format(url))
    header = {
        'authority': 'www.zillow.com',
        'method': 'GET',
        'path': '/homes/{0}_rb/rentals/{1}_p/'.format(zip, page),
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'cache-control': 'max-age=0',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }

    timeout = random.choice(range(80, 180))

    try:
        rep = requests.get(url, headers=header, timeout=timeout)
        rep.encoding = 'utf-8'
    except socket.timeout as e:
        print(e)
        time.sleep(random.choice(range(8, 15)))
    except socket.error as e:
        print(e)
        time.sleep(random.choice(range(8, 15)))
    except http.client.BadStatusLine as e:
        print('5:', e)
        time.sleep(random.choice(range(30, 80)))

    except http.client.IncompleteRead as e:
        print('6:', e)
        time.sleep(random.choice(range(5, 15)))

    html_text = rep.text

    # Parse data using beautifulSoup
    bs = BeautifulSoup(html_text, 'html.parser')
    body = bs.body
    data = body.find('div', {'id': 'grid-search-results'})
    results = data.find_all('div', class_='list-card-info')

    total_result = int(body.find_all('span', class_='result-count')[0].text.split(" ")[0])
    for result in results:
        try:
            url = result.find_all('a')[0].get('href')
            url_list.append(url)
        except:
            print("Error in getting URL.")
            continue

    total_page = int(total_result / 40) + 1
    print("Total {0} Properties listed for leasing in Zip {1}".format(len(url_list), zip))
    return url_list, total_page


if __name__ == '__main__':
    p = get_all_rent_house_url_by_zip('28277')
