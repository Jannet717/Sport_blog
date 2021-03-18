import csv

import requests
from bs4 import BeautifulSoup

import threading


def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text


# def get_total_pages(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     # print(soup.prettify())
#     pages_ul = soup.find('div', class_="pager-wrap").find('ul')
#     last_page = pages_ul.find_all('li')[-1]
#     total_pages = last_page.find('a').get('href').split('=')[-1]
#     # print(total_pages)
#     return int(total_pages)


# def write_to_csv(data):
#     with open('taskparsing.csv', 'a') as csv_file:
#         writer = csv.writer(csv_file, delimiter='/')
#         writer.writerow((data['title'],
#                         data['description']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_list = soup.find('div', class_="maincol")
    products = product_list.find_all('ul', class_="news-list")
    list_ = []
    for product in products:



        title = product.find('div', class_="headline").find('a').text
            # print(title)


        description = product.find('div', class_="txt").find('p').text



        data = {'title': title, 'description': description }
        # print(data)
        list_.append(data)
    return list_

def main():
    parsing_url = 'https://terrikon.com/posts/'
    pages = 'page/'

    total_pages = get_html(parsing_url)
    # print(total_pages)
    list_ = []
    for page in range(18390, 18409):  # 37
        # print(page)
        url_with_page = parsing_url + pages + str(page)
        #    print(url_with_page)
        threading.Timer(3600.0, main).start()
        html = get_html(url_with_page)
        # print(html)
        _list_ = get_page_data(html)
        list_.extend(_list_)
    # print(list_)
    return list_


