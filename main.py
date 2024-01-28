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

########################################
# CHANGE NAME HERE - LOCAL DOWNLOAD DIRECTORY FOR FILES
########################################
download_directory = (r'C:\Users\liast\PycharmProjects\pythonProject1\data 2201')

# Set up Chrome options and preferences for download
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_directory,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True
})


# browser = webdriver.Chrome(options=chrome_options)


def download_csv_from_blockchain(address):
    """
    this function downloads the csv file from the blockchain using the auction address
    :param address: auction-address
    :return: none
    """
    # open the site
    address_url = url + address
    browser.get(address_url)
    time.sleep(random.randint(1, 10))

    ###################################
    # CHANGE THE START DATE (ONLY RELEVANT IF DATA GOES FURTHER THAN A MONTH BACK)
    ###################################
    js_script = """
        var element = document.getElementById('{0}');
        element.value = '{1}';
    """.format('ContentPlaceHolder1_txtstart_time', '1/01/2023')
    browser.execute_script(js_script)
    time.sleep(random.randint(1, 10))

    # Function to check if element exists by XPath
    def check_exists_by_xpath(xpath):
        """
        this function checks if an element exists by xpath
        :param xpath: xpath
        :return: boolean
        """
        try:
            browser.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    # Ticks reCAPTCHA checkbox
    if not check_exists_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div/span/div[4]'):
        element = browser.find_element(By.TAG_NAME, 'iframe')
        # print("scrolling down")
        browser.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)
        # print("scrollllllllll")
        browser.find_element(By.TAG_NAME, 'iframe').click()
    time.sleep(30)

    # clicks on download
    browser.find_element(By.ID, 'ContentPlaceHolder1_btnSubmit').click()

    # Wait for the file to be downloaded
    while_num = 0
    while not any(re.findall(rf"{address}", fname) for fname in os.listdir(download_directory)):
        time.sleep(1)
        while_num += 1
        print("while num is: ", while_num)
    print("end of while loop")


##################################
# THIS FUNCTION IS ONLY RELEVANT FOR DATA FROM QUALTRICS
##################################
def load_df():
    """
    ONLY RELEVANT FOR DATA FROM QUALTRICS
    this function loads the df from the csv files
    :return: data fram
    """
    sellers_data_1 = pd.read_csv('Data+Marketplace+stage+1+2+sellers.csv')
    column_list = sellers_data_1.columns.values
    # print(column_list)
    sellers_data_1 = sellers_data_1.drop(
        columns=["StartDate", "EndDate", 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'RecordedDate',
                 'ResponseId', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail', 'ExternalReference',
                 'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage', 'Introduction', 'i',
                 'metamask feedback', 'mining feedback', 'wallet screenshot_Id', 'wallet screenshot_Name',
                 'wallet screenshot_Size', 'wallet screenshot_Type', 'conf. creating auct', 'conf. auction page',
                 'thank you'])
    return sellers_data_1


##################################
# THIS FUNCTION IS ONLY RELEVANT FOR DATA FROM QUALTRICS
##################################
def create_address_list(col_lst, a, df_combined):
    """
    ONLY RELEVANT FOR DATA FROM QUALTRICS
    this function creates a list of all the addresses that were used in the auctions
    :param col_lst: a list of columns that we want to take this data qualtrics/address from
    :param a: the number of auctions that we want to take the data qualtrics from for each seller
    :param df_combined: the df we created from the two csv files
    :return: auction addresses list
    """
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


##################################
# THIS FUNCTION IS ONLY RELEVANT FOR DATA FROM QUALTRICS
##################################
def create_addresses_list():
    """
    ONLY RELEVANT FOR DATA FROM QUALTRICS
    this function creates a list of all the addresses that were used in the auctions
    :return: auction addresses list
    """
    df = load_df()
    return create_address_list(['verification_'], 3, df)


if __name__ == '__main__':
    """
    this is the main function crawls the blockchain and downloads the csv files
    """
    ##################################
    # CHANGE NAME HERE
    ##################################
    df = pd.read_csv('blockchain 2201.csv')
    for address in df['Address']:
        print("starting with " + address)
        browser = webdriver.Chrome(options=chrome_options)
        try:
            # trying to download the csv file from the blockchain
            download_csv_from_blockchain(address)
        except:
            print("exception!")
            browser.quit()
            browser = webdriver.Chrome(options=chrome_options)
            print("continue with " + address)
            download_csv_from_blockchain(address)
        finally:
            print("finished with " + address)
            browser.quit()
            time.sleep(2)
