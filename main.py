from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
import time
from pprint import pprint
import pandas as pd

MTCC_SITE = "https://www.mtccc.com/events/"


def get_browser():
    # Selenium Setup
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(chrome_options=chrome_options)


def get_site(site):
    session = HTMLSession()
    response = session.get(site)
    response.html.render()

    with open('data/mtcc.html', mode='w') as file:
        file.write(response.html.html)


def read_site(site):
    try:
        open(f"data/{site[0]}")
    except FileNotFoundError:
        get_site(site[1])
    finally:
        with open(f'data/{site[0]}') as file:
            content = file.read()
        return BeautifulSoup(content, 'html.parser')


def get_mtcc():
    browser = get_browser()
    browser.get(MTCC_SITE)

    time.sleep(5)
    events = browser.find_elements(By.XPATH, '//ul[@id="eventList"]/li/a')

    formatted = pd.DataFrame({
             'title': event.find_element(By.XPATH, './/div[@class="mainEvItemTitle"]').text,
             'link': event.get_attribute('href'),
             'dates': event.find_element(By.XPATH, './/div[@class="alt eventDay"]').text,
             'type': event.find_element(By.XPATH, './/div[@class="mainEvItemType"]').text
                             } for event in events)
    pprint(formatted)
    formatted.to_csv('data/mtcc.csv')


def read_mtcc():
    return pd.read_csv('data/mtcc.csv')


data = read_mtcc()
print(data)
# get_mtcc()
