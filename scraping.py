from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import pprint
import pandas as pd
from time import sleep

# Make pandas print all columns
pd.set_option('display.max_columns', None)

MTCC_URL = "https://www.mtccc.com/events/"
SBA_URL = "https://www.scotiabankarena.com/calendar"
NPS_URL = "https://www.toronto.ca/services-payments/venues-facilities-bookings/booking-city-facilities/city-squares/nathan-phillips-square/events-happening-on-nathan-phillips-square/"


class Scraper:
    def __init__(self):
        self.browser = self.get_browser()

    def get_browser(self):
        # Selenium Setup
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox") # linux only
        # chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        return driver

    def get_mtcc(self):
        self.browser.get(MTCC_URL)

        sleep(2)
        events = self.browser.find_elements(By.XPATH, '//ul[@id="eventList"]/li/a')

        formatted = pd.DataFrame({
                 'title': event.find_element(By.XPATH, './/div[@class="mainEvItemTitle"]').text,
                 'link': event.get_attribute('href'),
                 'dates': event.find_element(By.XPATH, './/div[@class="alt eventDay"]').text,
                 'type': event.find_element(By.XPATH, './/div[@class="mainEvItemType"]').text
                                 } for event in events)

        formatted.to_csv('data/mtcc.csv', index=False)

    def get_sba(self):
        self.browser.get(SBA_URL)

        events = self.browser.find_elements(By.XPATH, '//div[contains(@class, "hasEvent")]')
        formatted = pd.DataFrame({
            'title': event.find_element(By.XPATH, './/div[@class="event_item"]').text,
            'link': event.find_element(By.XPATH, './/a').get_attribute('href'),
            'dates': event.get_attribute('data-fulldate'),
            'type': 'public'
                                 }for event in events)
        formatted.to_csv('data/sba.csv')

    def get_nps(self):
        self.browser.get(NPS_URL)

        months = self.browser.find_elements(By.XPATH, '//div[@class="accordion__section"]/div')
        events = months[0].find_elements(By.XPATH, './/p')

        formatted = pd.DataFrame({
            'title': event.get_attribute('textContent').split(':')[1].strip(),
            'link': "",
            'dates': event.get_attribute('textContent').split(':')[0].strip(),
            'type': 'Public Event'
                                 }for event in events)
        formatted.to_csv('data/nps.csv', index=False)

    def read_csv(self, file):
        return pd.read_csv(f'data/{file}.csv')

# # MTCC stuff
# get_mtcc()
# data = read_csv('mtcc')
# print(data)


# # SBA stuff
# get_sba()
# data = read_csv('sba')
# print(data)

scraper = Scraper()
scraper.get_nps()