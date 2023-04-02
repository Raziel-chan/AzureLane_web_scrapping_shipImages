import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from requests import RequestException
from urllib.parse import unquote
from unidecode import unidecode
from urllib.parse import quote

def process_ship_rows(ship_rows):
    for row in ship_rows:
        name_cell = row.find_all('td')[1]
        link = name_cell.find('a')

        ship_url = f"{base_url}{link['href']}"
        ship_response = requests.get(ship_url)
        ship_soup = BeautifulSoup(ship_response.text, 'html.parser')

        ship_name = ship_soup.find('h1', id='firstHeading').text
        ship_name = unquote(ship_name)
        folder_name = ship_name.replace(' ', '_')
        ship_folder_path = os.path.join(parent_folder, folder_name)
        os.makedirs(ship_folder_path, exist_ok=True)

        ship_images = ship_soup.find_all('img')
        print(ship_images)

        target_images = []

        for img in ship_images:
            if 'ShipyardIcon' in img['src'] or unquote(ship_name).replace(' ', '_') in img['src']:
                target_images.append(img)

        for index, img in enumerate(target_images):
            img_url = img['src']
            img_file_path = f"{ship_folder_path}/{folder_name}_{index}.png"

            if os.path.exists(img_file_path):
                #print(f"Image {img_file_path} already exists. Skipping download.")
                continue
            else:
                try:
                    img_response = requests.get(img_url)
                    time.sleep(1)
                except RequestException as e:
                    print(f"Failed to fetch image for ship {ship_name}: {e}")
                    continue

                with open(img_file_path, 'wb') as img_file:
                    img_file.write(img_response.content)

base_url = 'https://azurlane.koumakan.jp'
list_of_ships_url = f'{base_url}/wiki/List_of_Ships'

response = requests.get(list_of_ships_url)
soup = BeautifulSoup(response.text, 'html.parser')

ship_tables = soup.find_all('table', class_='wikitable')

parent_folder = "images"
os.makedirs(parent_folder, exist_ok=True)

# Normal ships
#ship_rows = ship_tables[0].find_all('tr')[1:]  # Skip header row
#process_ship_rows(ship_rows)

# Research ships
ship_rows = ship_tables[1].find_all('tr')[1:]  # Skip header row
process_ship_rows(ship_rows)

# META ships
#ship_rows = ship_tables[2].find_all('tr')[1:]  # Skip header row
#process_ship_rows(ship_rows)

# Collab ships
#ship_rows = ship_tables[3].find_all('tr')[1:]  # Skip header row
#process_ship_rows(ship_rows)

sys.exit()
