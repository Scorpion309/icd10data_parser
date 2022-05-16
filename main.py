import json
import logging
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import RequestException
from settings import URL, FULL_URL, LOGGING_LEVEL
from db import connect_to_db

logging.basicConfig(level=LOGGING_LEVEL)

def get_html(url):
    try:
        return requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
    except RequestException:
        logging.warning('Невозможно подключиться к серверу! Сервер недоступен или Ваш запрос заблокирован.')


def get_info_from_elements(elements):
    groups_info = {}
    for element in elements:
        group_information = element.get_text().strip().split()
        link = URL + element.find('a').get('href')
        group_code = group_information[0]
        group_desc = ' '.join(group_information[1:])
        groups_info[group_code] = {'link': link,
                                   'group_desc': group_desc}
    return groups_info


def get_groups_elements(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.find('div', class_="body-content").find('ul').find_all('li')


def get_detailed_elements(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.find('div', class_="body-content").find('ul', class_="i51").find_all('li')


def save_to_json(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == '__main__':
    def parse():
        logging.info('Получаю данные с сайта...')
        # groups_elements = get_groups_elements(get_html(FULL_URL))
        # groups_info = get_info_from_elements(groups_elements)
        # for group_code, group_info in groups_info.items():
        #     detailed_groups_elements = get_detailed_elements(get_html(group_info['link']))
        #     detailed_groups_info = get_info_from_elements(detailed_groups_elements)
        #     for detailed_group_code, detailed_group_info in detailed_groups_info.items():
        #         time.sleep(2)
        #         elements = get_detailed_elements(get_html(detailed_group_info['link']))
        #         elements_info = get_info_from_elements(elements)
        #         detailed_groups_info[detailed_group_code].update(elements_info)
        #     groups_info[group_code].update(detailed_groups_info)

        connect_to_db()
        with open('data.json', 'r') as inputfile:
            groups_info = json.load(inputfile)



        logging.info('Данные получены! Сохраняю...')
        save_to_json(groups_info)


    parse()
