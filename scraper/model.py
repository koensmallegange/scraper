import requests
from bs4 import BeautifulSoup
import pandas as pd

class RealEstateModel:
    def __init__(self, url):
        self.url = url
        self.houses = []

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            self.parse_data(soup)
        else:
            raise Exception(f"Failed to fetch data from {self.url}")

    def parse_data(self, soup):
        listings = soup.select("div.zoekresultaat")
        new_houses = []
        for house in listings:
            location = house.select_one("div.objectgegevens").get_text(strip=True)
            address = house.select_one("div.objectgegevens").get_text(strip=True)

            # Check if the location is in Amsterdam
            if "Amsterdam" not in location:
                continue

            house_data = {
                'address': address,
                'price': None,
                'url': None
            }

            # Get the price
            price_tag = house.select_one('div.objectgegevens span.vraagprijs')
            if price_tag:
                house_data['price'] = price_tag.get_text(strip=True)

            # Get the 'Meer informatie' URL
            info_url = house.select_one("div.over a")
            if info_url:
                house_data['url'] = info_url['href']

            new_houses.append(house_data)

        self.houses = new_houses

    def get_new_houses(self, old_houses):
        return [house for house in self.houses if house['address'] not in old_houses]
