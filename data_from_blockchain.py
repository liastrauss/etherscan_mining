import numpy as np
import pandas as pd
import os
from eth_utils import to_wei
import matplotlib.pyplot as plt

file_list = os.listdir("data")


def eth_to_wei(eth_val):
    wei_val = to_wei(eth_val, 'ether')
    # print(f"ETH: {eth_val}, Wei: {wei_val}")
    return wei_val


# creates column with wei value of transactions
def create_df_and_csv_with_wei_val():
    for file in file_list:
        df = pd.read_csv("data/" + file, float_precision='round_trip')
        for index, row in df.iterrows():
            if pd.isna(row['Status']):
                eth_val = row['Value_IN(ETH)']
                wei_val = eth_to_wei(eth_val)
                df.at[index, 'Value_IN(Wei)'] = wei_val
        df.to_csv("data in wei/" + file + ".csv")
        # print(df['Value_IN(ETH)'])


def create_dict_for_plot():
    folder_path = 'data in wei'
    data_dict = {}

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            if 'Value_IN(Wei)' in df.columns:
                to_column = df['To']
                value_column = df['Value_IN(Wei)']

                for to, value in zip(to_column, value_column):
                    if pd.notna(to):
                        to = str(to)
                        if pd.notna(value):
                            if to not in data_dict:
                                data_dict[to] = [value]
                            else:
                                data_dict[to].append(value)
    return data_dict


def adapt_dict(data_dict):
    new_dict = data_dict.copy()
    for key, val in new_dict.items():
        if len(val) > 1:
            for i in range(len(val)-1, 0, -1):
                val[i] = val[i] - val[i-1]
    return new_dict


def create_stacked_bar_plot(data_dict):
    new_dict = adapt_dict(data_dict)
    # Extract keys and values from the dictionary
    keys = list(new_dict.keys())
    values = list(new_dict.values())

    # Set up the figure and axes
    fig, ax = plt.subplots()

    # Create a color map
    cmap = plt.get_cmap('Set1')

    # Plot each column as a stacked bar
    for i, (key, lst) in enumerate(zip(keys, values)):
        # if key != '0x7664e53c74b3beced08710d2617761d6a09ea4af':
        if True:
            bottom = 0
            for value in lst:
                if value != 0:  # Skip zero values
                    height = value
                    color = cmap((bottom + height / 2) / sum(lst))  # Center the color on the bar
                    ax.bar(key, height, bottom=bottom, color=color)
                    bottom += height

    # Set the y-axis limit based on the maximum value
    ax.set_ylim(0, 1000)

    # Customize the plot
    ax.set_xlabel('Address')
    ax.set_ylabel('Bids')
    ax.set_title('Bids Stacked Bar Plot')
    plt.xticks(rotation='vertical')

    # Display the plot
    plt.show()

# data_dict = create_dict_for_plot()

# print(adapt_dict(data_dict))

# print(data_dict)

# create_stacked_bar_plot(data_dict)
