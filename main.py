import json
import logging
import time

import requests
from bs4 import BeautifulSoup
from requests import RequestException

from db import save_data_to_db
from settings import URL, FULL_URL, LOGGING_LEVEL, HEADERS

logging.basicConfig(level=LOGGING_LEVEL)


def get_html(url):
    try:
        return requests.get(url, headers=HEADERS).text
    except RequestException:
        logging.warning('Unable to connect to server! The server is unavailable or your request has been blocked.')
        logging.info('Finishing work...')
        raise


def get_info_from_elements(elements):
    groups_info = {}
    for element in elements:
        group_information = element.get_text().strip().split()
        link = URL + element.find('a').get('href')
        group_code = group_information[0]
        group_desc = ' '.join(group_information[1:])
        groups_info[group_code] = {'code': group_code,
                                   'link': link,
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
        logging.info(f'Getting data from the site {FULL_URL}...')

        groups_elements = get_groups_elements(get_html(FULL_URL))
        groups_info = get_info_from_elements(groups_elements)
        for group_code, group_info in groups_info.items():
            detailed_groups_elements = get_detailed_elements(get_html(group_info['link']))
            detailed_groups_info = get_info_from_elements(detailed_groups_elements)
            for detailed_group_code, detailed_group_info in detailed_groups_info.items():
                time.sleep(2)
                elements = get_detailed_elements(get_html(detailed_group_info['link']))
                elements_info = get_info_from_elements(elements)
                detailed_groups_info[detailed_group_code]['detailed_code'] = elements_info
            groups_info[group_code]['detailed_code'] = detailed_groups_info

        logging.info('Data received. Connecting to MySQL database...')

        try:
            save_data_to_db(groups_info)
        except Exception:
            logging.warning('An error occurred while saving data to DB!')
        else:
            logging.info(f'All data successfully parsed from {URL} and saved to MySQL DB!')
        finally:
            logging.info('Finishing work...')


    parse()
