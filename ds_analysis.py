import csv
import pandas as pd
import matplotlib.pyplot as plt

spam_numbers = pd.read_csv("dnc_complaint_numbers_2021-07-08.csv")

calls_by_state = spam_numbers.groupby('Consumer_State').size()
print(type(calls_by_state))
print(calls_by_state.index[0])
print(calls_by_state[0])

import plotly.graph_objects as go  # import plotly
fig = go.Figure(data=go.Bar(x=calls_by_state.index, y=calls_by_state)) # create a figure
fig.write_html('figure.html') # export to HTML file