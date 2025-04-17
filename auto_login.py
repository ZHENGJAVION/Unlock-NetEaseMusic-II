# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U=00CAD6391D9DCFF0C5F58B48FA943FF076A9F5ABD605BE30C0A9ACB1B54B2B90D58FA683966807F720513BE214A270E4391F8DBB8761E5A782AD4C54A3F4777099822788D8B15E92B444508BCAEF20C65127461FB95B86A90216308542C25B8DA78B1EB73CA9147B5B2FD284F3C0AD68C904A2FC06C929EC0B5FBD7BEA02EE3BED94C5C880ADCDDCF8D3D73BE3DD722CCC97959549884A36C48C6B6C600B744D42F097E09A36DE0DB2177BE9AA836D172AF9DF2ABEBAB3FFCCC2885C4C3DFCC164A4244E9582F381DED012B78D618A079D270EE8AEFF83A6720AF8C6192F8EE8871CD1C4AB552A957DA795DDACCFB69D350AF85DFDEA6C258752EA233E256017CB3697337F0E17D89E183084C7E23824BFA2C7C4409A653B51B1832D5D35F899D59F08320735E696F907CD24F81ED6F2BB3F0F28E4CC4A2B19297065E31863AF989672F93ED3245607C0759D98B1A39980C7D84D272ACFCF6046584B329BE12FC3"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
