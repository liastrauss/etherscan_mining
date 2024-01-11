import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import random
from selenium.common.exceptions import NoSuchElementException

url = 'https://sepolia.etherscan.io/exportData?type=address&a='
download_directory = (r'C:\Users\liast\Documents\RA Internship\Blockchain\data marketplace analysis\transactions by '
                      r'auction address')

# Set up Chrome options and preferences for download
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_directory,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    # 'safebrowsing.enabled': True
})

# browser = webdriver.Chrome(options=chrome_options)


def login(address):
    # open the site
    address_url = url + address
    browser.get(address_url)
    time.sleep(random.randint(1, 10))

    # change the start date
    js_script = """
        var element = document.getElementById('{0}');
        element.value = '{1}';
    """.format('ContentPlaceHolder1_txtstart_time', '1/12/2023')
    browser.execute_script(js_script)
    time.sleep(random.randint(1, 10))

    # Function to check if element exists by XPath
    def check_exists_by_xpath(xpath):
        try:
            browser.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    # Ticks reCAPTCHA checkbox
    if not check_exists_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div/span/div[4]'):
        browser.find_element(By.TAG_NAME, 'iframe').click()
    time.sleep(15)

    # clicks on download
    browser.find_element(By.ID, 'ContentPlaceHolder1_btnSubmit').click()

    # Wait for the file to be downloaded
    while not any(fname.startswith(address) for fname in os.listdir(download_directory)):
        time.sleep(1)

    # browser.quit()


address_list = ['0xDFc97DF05F35315D6B84A49BB7FEF5d52c3c4850', '0xB3D54069f271919088158F9DE5E5f610C0D23C8B']

if __name__ == '__main__':
    for address in address_list:
        print("starting with " + address)
        browser = webdriver.Chrome(options=chrome_options)
        try:
            login(address)
        finally:
            print("finished with " + address)
            browser.quit()
            time.sleep(2)

