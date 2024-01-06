import json
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

import storage
from config import BASE_LINK, STORAGE_TYPE
from parser import AdvertisementPageParser
from storage import FileStorage, MongoStorage


class BaseCrawler(ABC):

    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == 'mongo':
            return MongoStorage()
        return FileStorage()

    @abstractmethod
    def start(self, store=False):
        pass

    @abstractmethod
    def store(self, data, *args):
        pass

    @staticmethod
    def get(link):
        try:
            response = requests.get(link)
        except requests.HTTPError:
            return None
        return response


class LinkCrawler(BaseCrawler):

    def __init__(self, cities, link=BASE_LINK):
        self.cities = cities
        self.link = link
        super().__init__()

    @staticmethod
    def find_links(html_doc):
        soup = BeautifulSoup(html_doc, features="html.parser")
        return soup.find_all('a', attrs={'class': 'hdrlnk'})

    def start(self, store=False):

        adv_links = list()
        for city in self.cities:
            new_link = self.link.format(city)
            response = self.get(new_link)
            links = self.find_links(response.text)
            print(f'{city} total: {len(links)}')
            adv_links.extend(links)

        if store:
            links_list = [{'url': li.get('href'), 'flag': False} for li in adv_links]
            self.store(links_list)
        # if store:
        #     self.store(
        #         [{'url': li.get('href'), 'flag': False} for li in adv_links])
        # return adv_links

    def store(self, data, *args):
        self.storage.store(data, "results/", 'advertisements_links')


class DataCrawler(BaseCrawler):

    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = AdvertisementPageParser()

    def __load_links(self):
        return self.storage.loader('advertisements_links', {'flag': False})

    def start(self, store=False):
        for link in self.links:
            response = self.get(link['url'])
            data = self.parser.parse(response.text)
            if store:
                self.store(data)

            self.storage.update_flag(link)

    def store(self, data, *args):
        self.storage.store(data, "results/datas/", "advertisement_data")
        print(data['post_id'])


#---------------------------------------

class ImageDownloader(BaseCrawler):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.advertisements = self.__load_advertisements()

    def __load_advertisements(self):
        return self.storage.loader('advertisement_data')

    @staticmethod
    def get(link):
        try:
            response = requests.get(link, stream=True)
        except requests.HTTPError:
            return None
        return response

    def start(self, store=True):
        for advertisement in self.advertisements:
            counter = 1
            for image in advertisement['images']:
                response = self.get(image['url'])
                if store:
                    self.store(response, advertisement['post_id'], counter)
                counter += 1

    def store(self, data, adv_id, img_number):
        filename = f'{adv_id}-{img_number}'
        return self.save_to_disk(data, filename)

    def save_to_disk(self, response, filename):
        with open(f'results/images/{filename}.jpg', 'ab') as f:
            f.write(response.content)
            for _ in response.iter_content():
                f.write(response.content)

        print(filename)
        return filename