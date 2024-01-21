import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import random
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np
import re
from statistics import mean
import matplotlib.pyplot as plt

url = 'https://sepolia.etherscan.io/exportData?type=address&a='
download_directory = (r'C:\Users\User\Documents\עבודה רננה\Blockchain\ניתוח נתונים מכירה פומבית\data')
file_list = os.listdir("data")

# download_directory = (r'C:\Users\liast\Documents\RA Internship\Blockchain\data marketplace analysis\transactions by '
#                       r'auction address')

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
        element = browser.find_element(By.TAG_NAME, 'iframe')
        print("scrolling down")
        browser.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)
        print("scrollllllllll")
        browser.find_element(By.TAG_NAME, 'iframe').click()
    time.sleep(15)

    # clicks on download
    browser.find_element(By.ID, 'ContentPlaceHolder1_btnSubmit').click()

    # Wait for the file to be downloaded
    while_num = 0
    while not any(re.findall(rf"{address}", fname) for fname in os.listdir(download_directory)):
        time.sleep(1)
        while_num += 1
        print("while num is: ", while_num)
    print("end of while loop")
    # browser.quit()
    # r"0x\w+"
    # while_num = 0
    #     while not any(fname.startswith(address) for fname in os.listdir(download_directory)):
    #         time.sleep(1)
    #         while_num += 1
    #         print("while num is: ", while_num)
    #     print("end of while loop")
    #     # browser.quit()


def load_df(file_path, col):
    sellers_data_1 = pd.read_csv(file_path)
    column_list = sellers_data_1.columns.values
    # print(column_list)
    sellers_data_1 = sellers_data_1.drop(
        columns=col)
    return sellers_data_1


def create_address_list(col_lst, a, df_combined):
    address_lst = []
    clean_address_list = []
    for i in range(a):
        for index in df_combined.index:
            if pd.isna(df_combined[col_lst[0] + str(i + 1) + "_1"][index]):
                continue
            elif not df_combined[col_lst[0] + str(i + 1) + "_1"][index].startswith('0x'):
                continue
            else:
                if df_combined[col_lst[0] + str(i + 1) + "_1"][index] not in address_lst:
                    clean_address = re.findall(r"0x\w+", df_combined[col_lst[0] + str(i + 1) + "_1"][index])
                    clean_address_list.extend(clean_address)
                    address_lst.append(df_combined[col_lst[0] + str(i + 1) + "_1"][index])
    return clean_address_list


def create_addresses_list():
    df1 = load_df('Data+Marketplace+stage+1+2+sellers.csv',
                  ["StartDate", "EndDate", 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'RecordedDate',
                   'ResponseId', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail', 'ExternalReference',
                   'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage', 'Introduction', 'i',
                   'metamask feedback', 'mining feedback', 'wallet screenshot_Id', 'wallet screenshot_Name',
                   'wallet screenshot_Size', 'wallet screenshot_Type', 'conf. creating auct', 'conf. auction page',
                   'thank you'])
    df2 = load_df('Data+marketplace+seller+stage+3.csv',
                  ["StartDate", "EndDate", 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'RecordedDate',
                   'ResponseId', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail', 'ExternalReference',
                   'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage', 'introduction',
                   'prolific id'])

    part1_address_lst = create_address_list(['verification_'], 3, df1)
    part3_address_lst = create_address_list(['bids information_'], 3, df2)
    # print(set(part1_address_lst.extend(part3_address_lst)))
    # print(len(set(part1_address_lst.extend(part3_address_lst))))
    for add in part3_address_lst:
        if add in part1_address_lst:
            continue
        else:
            part1_address_lst.append(add)
            print(add)
    print(part1_address_lst)
    print(len(part1_address_lst))
    return part1_address_lst


# address_list = ['0xDFc97DF05F35315D6B84A49BB7FEF5d52c3c4850', '0xB3D54069f271919088158F9DE5E5f610C0D23C8B']


if __name__ == '__main__':
    address_list = create_addresses_list()
    for address in address_list:
        # if "export-" + address + ".csv.csv" not in download_directory:
        if "export-" + address + ".csv" not in file_list:
            print("starting with " + address)
            browser = webdriver.Chrome(options=chrome_options)
            try:
                login(address)
            except:
                print("exception!")
                browser.quit()
                browser = webdriver.Chrome(options=chrome_options)
                print("continue with " + address)
                login(address)
            finally:
                print("finished with " + address)
                browser.quit()
                time.sleep(2)


# 0x93eeE25C77671084B234046e77e7207da8dF3bc4
# 0xB3D54069f271919088158F9DE5E5f610C0D23C8B
# 0x3053531A176F4eFEF1ef78126Da54EbAf978A9De
