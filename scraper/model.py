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
            # Fill location and adress if they exis otherwise give None
            info_url = house.select_one("div.over a")
            object_data = house.select_one("div.objectgegevens").get_text(strip=True) if house.select_one("div.objectgegevens") else 'Unknown'
            location = house.select_one("div.objectgegevens").get_text(strip=True) if house.select_one("div.objectgegevens") else 'Unknown'
            address = house.select_one("div.adresgegevens").get_text(strip=True) if house.select_one("div.adresgegevens") else 'Unknown' 
            # check if 'amsterdam' is in the url
            if 'Amsterdam' not in info_url['href']:
                continue

            house_data = {
                'Listing': object_data,
                'URL': None,
            }
        
            # Get the 'Meer informatie' URL
            info_url = house.select_one("div.over a")
            if info_url:
                house_data['URL'] = info_url

            new_houses.append(house_data)
    
        self.houses = new_houses

    def get_new_houses(self, old_houses):
        return [house for house in self.houses if house['Listing'] not in old_houses]
