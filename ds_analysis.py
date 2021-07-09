import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

# Displaying full dataframe upon calling print()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

spam_numbers = pd.read_csv("dnc_complaint_numbers_2021-07-08.csv")

calls_num = spam_numbers.groupby(['Subject', 'Consumer_State']).size()
# print(calls_num)

x_list = []
y_list = []
data_list = []

# putting states in x_list
for state in spam_numbers['Consumer_State']:
    x_list.append(state)
new_x_list1 = list(set(x_list))
new_x_list2 = [x for x in new_x_list1 if ((i = pd.isnull(x)) == False)]
new_x_list2.sort()

# putting subjects in y_list
for subject in spam_numbers['Subject']:
    y_list.append(subject)
y_list = list(dict.fromkeys(y_list))
new_y_list = [y for y in y_list if
              (y != 'Other' and y != 'No Subject Provided')]
new_y_list.sort()

# putting numbers in data
for subject in new_y_list:
    subj = []
    for state in new_x_list2:
        if state in calls_num[subject]:
            subj.append(calls_num[subject][state])
        else:
            subj.append(0)
    data_list.append(subj)

# plotting

# create a figure
map_ = go.Figure(data=go.Heatmap(z=data_list, x=new_x_list2, y=new_y_list))
map_.update_layout(title='Spam Calls per State and Subject')
map_.write_html('map.html')  # export to HTML file
