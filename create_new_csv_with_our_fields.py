import pandas as pd
import numpy as np
import re
from statistics import mean
import matplotlib.pyplot as plt


def create_merge_csv():
    """
    this function merges the 2 csv files of the sellers
    :return: merged df
    """
    sellers_data_1 = pd.read_csv('Data+Marketplace+stage+1+2+sellers.csv')
    sellers_data_3 = pd.read_csv('Data+marketplace+seller+stage+3.csv')
    column_list = sellers_data_1.columns.values
    print(column_list)
    sellers_data_1 = sellers_data_1.drop(
        columns=["StartDate", "EndDate", 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'RecordedDate',
                 'ResponseId', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail', 'ExternalReference',
                 'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage', 'Introduction', 'i',
                 'metamask feedback', 'mining feedback', 'wallet screenshot_Id', 'wallet screenshot_Name',
                 'wallet screenshot_Size', 'wallet screenshot_Type', 'conf. creating auct', 'conf. auction page',
                 'thank you'])
    sellers_data_3 = sellers_data_3.drop(
        columns=["StartDate", "EndDate", 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'RecordedDate',
                 'ResponseId', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail', 'ExternalReference',
                 'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage', 'introduction',
                 'prolific id'])
    df_combined = pd.merge(sellers_data_1, sellers_data_3, on="PROLIFIC_PID", how="left")
    column_list_full = df_combined.columns.values
    print(column_list_full)
    df_combined = df_combined[(df_combined['Finished_x'] == 'True') | (df_combined['Finished_y'] == 'True')]
    return df_combined


# pd.to_numeric(df_combined['verification_1_2'], errors='coerce')
# hobby_mean_df = pd.to_numeric(df_combined['verification_1_2'], errors='coerce')
# hobby_mean_df
def calculate_col_mean(col_name_lst, df_combined):
    """
    this function calculates the mean of the columns that we want to take the data qualtrics from
    :param col_name_lst: the list of columns that we want to take the data qualtrics from and calculate the mean
    :param df_combined: the df we created from the two csv files
    :return: dictionary of the columns and their mean
    """
    mean_dict = {}
    for col in col_name_lst:
        mean_df = df_combined[col]
        num_lst = []
        # print(mean_df)
        for index in mean_df:
            if pd.isna(index):
                continue
            else:
                # print(index, type(index))
                # print(re.findall('\d+', index))
                num_lst.extend(pd.to_numeric(re.findall(r'\d+', index)))
        print(num_lst)
        print(mean(num_lst))
        mean_dict[col] = mean(num_lst)
    return mean_dict


# ave_dict = calculate_col_mean(['verification_1_2', 'verification_2_2', 'verification_3_2'])
# print(ave_dict)


def create_bid_dict(col_lst, a, df_combined):
    """
    this function creates a dictionary of the starting price and the wining bid for each auction
    :param col_lst: the list of columns that we want to take the data qualtrics from
    :param a: number of auctions that we want to take the data qualtrics from for each seller
    :param df_combined: the df we created from the two csv files
    :return: a dictionary of the starting price and the wining bid for each auction
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


def create_bid_df(bids_dict):
    """
    this function creates a df from the dictionary of the starting price and the wining bid for each auction
    :param bids_dict: the dictionary of the starting price and the wining bid for each auction
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
    this function calculates the mean of the profit for each auction
    :param bids_dict:
    :return: a list of the mean of the profit for each auction
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
    this function calculates the ratio of the wining bid to the starting price for each auction
    :param bids_dict: a dictionary of the starting price and the wining bid for each auction
    :return: a list of the ratio of the wining bid to the starting price for each auction
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


# profit_mean(bids_dict)
# calc_ratio(bids_dict)
# create_bid_df(bids_dict)

# bids_dict = create_bid_dict(['verification_', 'bids information_'], 3)


def create_double_graph(bids_df):
    """
    this function creates a double graph of the starting price and the wining bid for each auction
    :param bids_df: df of the starting price and the wining bid for each auction
    :return: none
    """
    bids_df.plot(x="address", y=["start", "end"], kind="bar")
    plt.show()
    return 0


df_full = create_merge_csv()
bids__dict = create_bid_dict(['verification_', 'bids information_'], 3, df_full)
bids__df = create_bid_df(bids__dict)
create_double_graph(bids__df)
