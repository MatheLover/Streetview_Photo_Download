# Author: Chiang Yui/ JIANG Rui / 蔣睿
# Objective: Download google streetview photos using a link
# Implementation: Based on 3 references(mainly selenium and streetview )
# Reference 1 -- https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d -- #
# Reference 2 -- https://medium.com/swlh/web-scraping-stock-images-using-google-selenium-and-python-8b825ba649b9 -- #
# Reference 3 -- https://github.com/robolyst/streetview -- #
import hashlib
import io
import os
import requests as requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import random
import streetview

DRIVER_PATH = '/Users/benchiang/Documents/ChromeDriver/chromedriver'

# test webdriver
service = Service(DRIVER_PATH)
service.start()
wd = webdriver.Remote(service.service_url)
#wd.get('https://www.google.com.hk/')
wd.quit()


# Typical get image_url_method; no need for this implementation temporarily as we have link already
# def fetch_image_urls(query:str, wd:webdriver, sleep_between_interaction:int=1):

# coordinate pair generator
def random_coord(pair_num):  # specify number of coordinate pair
    """Generate random coordinates for latitudes and longitudes"""
    lat_default = 22.279010321531835
    long_default = 114.16889699791298

    lat_list = []
    lon_list = []

    for i in range(pair_num):
        lat_list.append(lat_default + random.uniform(0.01, 0.02))
        lon_list.append(long_default + random.uniform(0.03, 0.04))

    zipped_lat_lon_list = list(zip(lat_list, lon_list))  # zipped two lists
    return zipped_lat_lon_list


# panoid generator from coordinates
def generate_panoid(coord_list):  # zipped coordinate list
    """Generate panoid from zipped coordinate list and return photo info list(miscellaneous dictionaries)"""
    photo_info_list = []
    for i in range(len(coord_list)):  # iterate through coord_list
        panoids = streetview.panoids(lat=coord_list[i][0], lon=coord_list[i][1])
        photo_info_list.append(panoids)  # append to photo info list
    return photo_info_list


# extract each panoid in the raw_list
def extract_each_panoid(photo_info_list):
    """Extract each panoid from the list of dictionaries"""
    panoid_list = []
    for photos in photo_info_list:  # Iterate through the whole list of street view photo information dictionaries
        for photo in photos: # iterate each photo
            for key, value in photo.items():  # For each key-value pair of photo information within each photo
                if key == 'panoid':  # Create panoid list
                    panoid_list.append(value)
    return panoid_list


# Construct url for download
def prep_url(panoid):  # pass in panoid
    """Create URL for downloading streetview images"""
    search_URL = "https://geo0.ggpht.com/cbk?cb_client=maps_sv.tactile&panoid=" + str(
        panoid) + "&output=tile&x=4&y=2&zoom=4"
    return search_URL


# download image
def download_image(folder_path: str, url: str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"Error -- Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")

    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


# Test program
zipped_coord_list = random_coord(100)
photo_list = generate_panoid(zipped_coord_list)
panoid_list = extract_each_panoid(photo_list)


# iterate the panoid list and download image
for i in range(len(panoid_list)):
    download_image("/Users/benchiang/Desktop/Streetview/Selenium_StreetView",
                   prep_url(panoid_list[i]))