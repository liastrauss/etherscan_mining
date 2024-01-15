import os
import pandas as pd
import matplotlib.pyplot as plt

# file_list = os.listdir("data in wei")

# def plotting_bids():
    # for file in file_list

df = pd.read_csv("export-0x71E4825412700b83552ef900552dC3E94B781608.csv.csv")

df['Value_IN(Wei)'].plot(kind='bar', stacked=True, colormap='viridis')

# Customize the plot
plt.title('Stacked Bar Plot of Value_IN(Wei)')
plt.xlabel('Index')  # Assuming you don't have a specific category column
plt.ylabel('Value_IN(Wei)')

# Show the plot
plt.show()