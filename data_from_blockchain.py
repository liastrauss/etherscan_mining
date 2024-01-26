import numpy as np
import pandas as pd
import os
from eth_utils import to_wei
import matplotlib.pyplot as plt

# CHANGE NAME HERE - THIS IS THE FOLDER WHERE WE DOWNLOADED DATA FROM BLOCKCHAIN
file_list = os.listdir("data 2201")


def eth_to_wei(eth_val):
    wei_val = to_wei(eth_val, 'ether')
    # print(f"ETH: {eth_val}, Wei: {wei_val}")
    return wei_val


# creates column with wei value of transactions
def create_df_and_csv_with_wei_val():
    for file in file_list:
        # CHANGE NAME HERE
        df = pd.read_csv("data 2201/" + file, float_precision='round_trip')
        for index, row in df.iterrows():
            if pd.isna(row['Status']):
                eth_val = row['Value_IN(ETH)']
                wei_val = eth_to_wei(eth_val)
                df.at[index, 'val_in_wei'] = wei_val
            else:
                df = df.drop(index)
        # CHANGE NAME HERE
        df.to_csv("data in wei 2201/" + file)
        # print(df['Value_IN(ETH)'])

# create_df_and_csv_with_wei_val()


def create_dict_for_plot():
    # CHANGE NAME HERE - TARGET FOLDER FOR CONVERTED WEI FILES
    folder_path = 'data in wei 2201'
    data_dict = {}

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            if 'val_in_wei' in df.columns:
                to_column = df['To']
                value_column = df['val_in_wei']

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
            for i in range(len(val) - 1, 0, -1):
                val[i] = val[i] - val[i - 1]
    return new_dict


def generate_colour():
    colour = np.random.rand(3, )
    return colour


def create_stacked_bar_plot(data_dict):
    new_dict = adapt_dict(data_dict)
    # Extract keys and values from the dictionary
    keys = list(new_dict.keys())
    values = list(new_dict.values())

    # Set up the figure and axes
    fig, ax = plt.subplots()

    # Plot each column as a stacked bar
    for i, (key, lst) in enumerate(zip(keys, values)):
        # if key != '0x7664e53c74b3beced08710d2617761d6a09ea4af':
        if True:
            bottom = 0
            for value in lst:
                if value != 0:  # Skip zero values
                    height = value
                    colour = generate_colour()
                    ax.bar(key, height, bottom=bottom, color=colour)
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


data_dict = create_dict_for_plot()

# print(data_dict)

# print(adapt_dict(data_dict))

create_stacked_bar_plot(data_dict)
