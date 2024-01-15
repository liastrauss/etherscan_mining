import pandas as pd
import os
from eth_utils import to_wei

file_list = os.listdir("data")


def eth_to_wei(eth_val):
    wei_val = to_wei(eth_val, 'ether')
    print(f"ETH: {eth_val}, Wei: {wei_val}")
    return wei_val


# creates column with wei value of transactions
def create_df_and_csv_with_wei_val():
    for file in file_list:
        df = pd.read_csv("data/" + file, float_precision='round_trip')
        for index, row in df.iterrows():
            eth_val = row['Value_IN(ETH)']
            wei_val = eth_to_wei(eth_val)
            df.at[index, 'Value_IN(Wei)'] = wei_val
        df.to_csv("data in wei/"+file+".csv")
        print(df['Value_IN(ETH)'])


def create_plot():

    return 0
