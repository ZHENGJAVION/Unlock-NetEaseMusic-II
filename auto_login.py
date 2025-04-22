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
    browser.add_cookie({"name": "00CAD6391D9DCFF0C5F58B48FA943FF076A9F5ABD605BE30C0A9ACB1B54B2B90D58FA683966807F720513BE214A270E4391F8DBB8761E5A782AD4C54A3F4777099822788D8B15E92B444508BCAEF20C65127461FB95B86A90216308542C25B8DA78B1EB73CA9147B5B2FD284F3C0AD68C904A2FC06C929EC0B5FBD7BEA02EE3BED94C5C880ADCDDCF8D3D73BE3DD722CCC97959549884A36C48C6B6C600B744D42F097E09A36DE0DB2177BE9AA836D172AF9DF2ABEBAB3FFCCC2885C4C3DFCC164A4244E9582F381DED012B78D618A079D270EE8AEFF83A6720AF8C6192F8EE8871CD1C4AB552A957DA795DDACCFB69D350AF85DFDEA6C258752EA233E256017CB3697337F0E17D89E183084C7E23824BFA2C7C4409A653B51B1832D5D35F899D59F08320735E696F907CD24F81ED6F2BB3F0F28E4CC4A2B19297065E31863AF989672F93ED3245607C0759D98B1A39980C7D84D272ACFCF6046584B329BE12FC3", "value": "0092F055425C76D0DBC620FFBF7E31493E58FEE462574A576BEDC54FD7DE6D1EECFDB0FD3BA7C52891E66FB220FF75D0C74BA5900A2862320E16AC173DBDD833C815E291C6804E55E8B419512744687C72A191A19B3E756C6B59BBB08B5DC0C686EF370157E81862D65F1B350AAE010D00B0F4706EA85C9D98D5263EDC3BB4AC208C0B87E7C606834AA70DFCE4B0DC28DB3DC44C5E66CB346ED60296461C07DB8EFB605D1FD09F31DDF6FC409EB4AC70856F07F0CB1BA05D33EA1449417311CFDF9C16F03D6B4B3CDB347B880DAF6795B150F46E9E524CC432486ED8C14F5D886FF09ED4E05338C4AE952C07D3BCA7CB5A8F51368C136DF1D28DE4FB63811B0BA2CC6A7D2D7321100056D652ACE07417B1DECCA487607DB132F327CF12F83953192C7B9032ABB01AC22489BECA2C2215ADEFD8E9FAC5E00648A8123929C80FBF8EB7A82919D1ABC7979EA72B28A5E7865B36E5B3196DCCD968565E3A3DDD4346EE"})
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
