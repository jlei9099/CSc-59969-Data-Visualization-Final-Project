# coding=utf-8
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import ListedColormap
import plotly.graph_objects as go 


df = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv')
df.drop(df.columns[[0,2,3]],axis=1, inplace=True)
# print(df)
# print(df.columns[1]) colum name
# print(len(df.columns)) length of columns
# print(len(df[df.columns[1]])) row search
# print(df[df.columns[88]][3]) col/row search

arr1=[]
arr2=[]

for i in range(1,len(df.columns)):
    arr1.append(df.columns[i])
    arr2.append(df[df.columns[i]][0])

fig = go.Figure(go.Scatter(x = arr1, y = arr2,
                  name='Afghanistan'))

fig.update_layout(title='Cases Recorded',
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True)

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False) 

