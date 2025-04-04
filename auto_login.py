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
    browser.add_cookie({"name": "MUSIC_U", "value": "009154162E2944A44B1EFC403A82892F60B222DC1030AF4456CC6EECAF4D16BD2B836FDDC3EEC583578FBB6749E1377C83C86A0F9041EC822CFF30CF887F32FB14E7698F33084C5A81BF5DD26FD397DE9DCD817FB700855BA6BEAC96C1148DEABA20D30E2E0650843BFCF73E905F7CBE6F0D657F8C2516F385D49746FBD0A8B47CDBBA8BD071D45B935DA64CBF33293224C14F96FDBC1AA63F8294872D7F40DEB36DAB8494F30A11963B40BE6D1F1BCE1D37FA8D9ABA4D64D08A6B66F82D6DE3AA46436CEAE09717FD369341573D5D0F4131C04A1A9E5C165707D341B99B0EFA7D7AE5EE15FC655E9CAE6551EDC1266C36EAB683F665B267FE5083E7CF11CFEA8EDAE99E0545A8C428B545469A393C23ED2EC207B1BE2D0CCC4BBC8D6841DAC0805C149D4BA44DAA957B180B2DEBB028C08A55E84CF3C19E8AEE3C489A6E8D9C439D1C3526AB3082027B640293C840731BCE4677B8110DED206CCB382409219AED"})
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
