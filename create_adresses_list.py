import pandas as pd
import numpy as np
import re
from statistics import mean
import matplotlib.pyplot as plt


########################################################
# THIS FILE IS RELEVANT ONLY FOR DATA FROM QUALTRICS!
########################################################

def load_df():
    """
    ONLY RELEVANT FOR DATA FROM QUALTRICS
    this function loads the df from the csv files
    :return: data frame
    """
    sellers_data_1 = pd.read_csv('Data+Marketplace+stage+1+2+sellers.csv')
    # sellers_data_3 = pd.read_csv('/content/Data+marketplace+seller+stage+3.csv')
    column_list = sellers_data_1.columns.values
    print(column_list)
    sellers_data_1 = sellers_data_1.drop(
        columns=["StartDate", "EndDate", 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'RecordedDate',
                 'ResponseId', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail', 'ExternalReference',
                 'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage', 'Introduction', 'i',
                 'metamask feedback', 'mining feedback', 'wallet screenshot_Id', 'wallet screenshot_Name',
                 'wallet screenshot_Size', 'wallet screenshot_Type', 'conf. creating auct', 'conf. auction page',
                 'thank you'])
    # sellers_data_3 = sellers_data_3.drop(columns=["StartDate", "EndDate", 'Status', 'IPAddress', 'Progress',
    # 'Duration (in seconds)', 'RecordedDate', 'ResponseId', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail',
    # 'ExternalReference', 'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage',
    # 'introduction', 'prolific id']) df_combined = pd.merge(sellers_data_1, sellers_data_3, on="PROLIFIC_PID",
    # how="left") column_list_full = df_combined.columns.values print(column_list_full) df_combined = df_combined[ (
    # df_combined['Finished_x'] == 'True' ) | (df_combined['Finished_y'] == 'True')] df_combined
    return sellers_data_1


def create_bid_dict(col_lst, a, df_combined):
    """
    this function creates a dictionary of all auctions: address, start price, end price. it takes the data from the
    qualtrics df.
    :param col_lst: the columns name that we took the data from
    :param a: number of auctions for each seller
    :param df_combined: the df we created from the two csv files
    :return: dictionary of all auctions: address, start price, end price
    """
    bids_dict = {}
    for i in range(a):
        for index in df_combined.index:
            if pd.isna(df_combined[col_lst[0] + str(i + 1) + "_1"][index]) | pd.isna(
                    df_combined[col_lst[1] + str(i + 1) + "_1"][index]):
                continue
            else:
                # bids_dict[df_combined[col_lst[0]+str(i+1)+"_1"][index]] = [df_combined[col_lst[0]+str(i+1)+"_2"][index], df_combined[col_lst[1]+str(i+1)+"_2"][index]]
                if str(i + 1) in bids_dict:
                    bids_dict[str(i + 1)].extend([[df_combined[col_lst[0] + str(i + 1) + "_1"][index],
                                                   df_combined[col_lst[0] + str(i + 1) + "_2"][index],
                                                   df_combined[col_lst[1] + str(i + 1) + "_2"][index]]])
                else:
                    bids_dict[str(i + 1)] = [[df_combined[col_lst[0] + str(i + 1) + "_1"][index],
                                              df_combined[col_lst[0] + str(i + 1) + "_2"][index],
                                              df_combined[col_lst[1] + str(i + 1) + "_2"][index]]]

                print(df_combined[col_lst[0] + str(i + 1) + "_2"][index],
                      df_combined[col_lst[1] + str(i + 1) + "_2"][index])
                print(bids_dict)
    return bids_dict


def create_address_list(col_lst, a, df_combined):
    """
    creates a list of all the addresses that were used in the auctions
    :param col_lst: the columns name that we took the data from
    :param a: number of auctions for each seller
    :param df_combined: the df we created from the two csv files
    :return: a list of all the addresses that were used in the auctions
    """
    address_list = []
    clean_address_list = []
    for i in range(a):
        for index in df_combined.index:
            # print("row num: ", index)
            if pd.isna(df_combined[col_lst[0] + str(i + 1) + "_1"][index]):
                continue
            elif not df_combined[col_lst[0] + str(i + 1) + "_1"][index].startswith('0x'):
                # print("skip: ", df_combined[col_lst[0] + str(i + 1) + "_1"][index])
                continue
            else:
                if df_combined[col_lst[0] + str(i + 1) + "_1"][index] not in address_list:
                    clean_address = re.findall(r"0x\w+", df_combined[col_lst[0] + str(i + 1) + "_1"][index])
                    # print("clean address: ", clean_address)
                    clean_address_list.extend(clean_address)
                    address_list.append(df_combined[col_lst[0] + str(i + 1) + "_1"][index])
                    # print(df_combined[col_lst[0] + str(i + 1) + "_2"][index])
                # else:
                # print("already in address list: ", df_combined[col_lst[0] + str(i + 1) + "_1"][index])
    # print(address_list)
    # print(len(address_list))
    # print(clean_address_list)
    # print(len(clean_address_list))
    # print(set(address_list))
    # print(len(set(address_list)))
    # print(clean_address_list == address_list)
    return clean_address_list


def create_bid_df(bids_dict):
    """
    this function creates a df from the dictionary of the starting price and the wining bid for each auction
    :param bids_dict: a dictionary of all auctions: address, start price, end price
    :return: df of the starting price and the wining bid for each auction
    """
    new_dict = {"address": [], "start": [], "end": []}
    for key in bids_dict:
        for index in bids_dict[key]:
            print('index', index)
            print(bids_dict[key])
            new_dict['address'].append(index[0])
            new_dict['start'].append(pd.to_numeric(index[1]))
            new_dict['end'].append(pd.to_numeric(index[2]))
            # new_dict['start'].extend(pd.to_numeric(index[1]))
            # new_dict['end'].extend(pd.to_numeric(index[2]))
    print(new_dict)
    new_df = pd.DataFrame(new_dict)
    print(new_df)
    return new_df


def profit_mean(bids_dict):
    """
    this function calculates the profit for each auction
    :param bids_dict: a dictionary of all auctions: address, start price, end price
    :return: a list of the profit for each auction
    """
    mean_list = []
    for key in bids_dict:
        num_list = []
        for index in bids_dict[key]:
            num_list.append(pd.to_numeric(index[2]))
        mean_list.append(mean(num_list))
        print(num_list)
    print(mean_list)
    return mean_list


def calc_ratio(bids_dict):
    """
    this function calculates the ratio between the start price and the end price for each auction
    :param bids_dict: a dictionary of all auctions: address, start price, end price
    :return: a list of the ratio between the start price and the end price for each auction
    """
    ratio_list = []
    for key in bids_dict:
        num_list = []
        for index in bids_dict[key]:
            start_price = pd.to_numeric(index[1])
            end_price = pd.to_numeric(index[2])
            num_list.append(end_price / start_price)
        ratio_list.append(mean(num_list))
        print(num_list)
    print(ratio_list)
    return ratio_list


def create_addresses_list():
    """
    ONLY RELEVANT FOR DATA FROM QUALTRICS
    this function creates a list of all the addresses that were used in the auctions
    :return: auction addresses list
    """
    df = load_df()
    # bids_dictionary = create_bid_dict(['verification_', 'bids information_'], 3)
    # profit_mean(bids_dict)
    # calc_ratio(bids_dict)
    # create_bid_df(bids_dictionary)
    return create_address_list(['verification_'], 3, df)
