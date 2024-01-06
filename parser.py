from bs4 import BeautifulSoup


class AdvertisementPageParser:

    # @staticmethod
    # def price_changer(price):
    #     new_price = price.replace('\\xa0', '')
    #     return new_price
    # data['price'] = self.price_changer(price_tag.text)

    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title_tag = self.soup.find('span', attrs={'id': 'titletextonly'})
        if title_tag:
            return title_tag.text
        return None

    @property
    def price(self):
        price_tag = self.soup.find('span', attrs={'class': 'price'})
        if price_tag:
            return price_tag.text
        return None

    @property
    def body(self):
        body_tag = self.soup.select_one('#postingbody')
        if body_tag:
            return body_tag.text
        return None

    @property
    def post_id(self):
        selector = 'p.postinginfo:nth-child(1)'
        id_tag = self.soup.select_one(selector)
        if id_tag:
            return id_tag.text.replace('Id publi: ', '')
        return None

    @property
    def created_time(self):
        selector = '.postinginfos > p:nth-child(2) > time:nth-child(1)'
        created_time_tag = self.soup.select_one(selector)
        if created_time_tag:
            return created_time_tag.attrs['datetime']
        return None

    @property
    def modified_time(self):
        selector = 'p.postinginfo:nth-child(3) > time:nth-child(1)'
        modified_time_tag = self.soup.select_one(selector)
        if modified_time_tag:
            return modified_time_tag.attrs['datetime']
        return None

    def parse(self, html_data):
        self.soup = BeautifulSoup(html_data, 'html.parser')
        data = dict(
            title=self.title, price=self.price, body=self.body,
            post_id=self.post_id,
            created_time=self.created_time, modified_time=self.modified_time
        )

        return data
