import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import ListedColormap
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output


df = s_data = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv')

df = df.rename(columns= {"Country/Region" : "Country", "Province/State": "Province"})

s_data= s_data.rename(columns= {"Country/Region" : "Country", "Province/State": "Province"})
s_data.drop(df.columns[[0, 2, 3]], axis=1, inplace=True) # removes long, lat, and province

deaths = deaths.rename(columns= {"Country/Region" : "Country", "Province/State": "Province"})
recovered = recovered.rename(columns= {"Country/Region" : "Country", "Province/State": "Province"})

country = df['Country'].unique() #list of countries
totalarr=[] #holds total cases
deathsarr=[] #holds deaths cases
recoveredarr=[] #holds recovered cases
aggregation_functions={} # dict to sum all dates count since countries are repeated due to province

for date in range(4,len(df.columns)):
    total_list = df.groupby('Country')[df.columns[date]].sum().tolist()
    totalarr.append(total_list)
    total_list = deaths.groupby('Country')[deaths.columns[date]].sum().tolist()
    deathsarr.append(total_list)
    total_list = recovered.groupby('Country')[recovered.columns[date]].sum().tolist()
    recoveredarr.append(total_list)
    aggregation_functions.update({df.columns[date]:'sum'})

s_data_new = s_data.groupby(s_data["Country"],as_index=False).aggregate(aggregation_functions) # sums date

country_list = df["Country"].tolist()
country_set = set(country_list)
country_list = list(country_set)
country_list.sort()
format_data=[] #holds data with countries total cases, deaths, and recovery data
repeat_dates=[] # list of dates to append to format_data

for x in range(len(totalarr)):
    format_data.append(list(zip(country_list, totalarr[x], deathsarr[x], recoveredarr[x])))

for i in range(4,len(df.columns)):
    for x in range(len(format_data[0])):
        repeat_dates.append(df.columns[i])

data=[] #array to hold all the formated data with dates
for i in range(len(format_data)):
    for x in range(len(format_data[i])):
        data.append(format_data[i][x])

for i in range(len(data)):
    date= (repeat_dates[i],)
    update= data[i] + date
    data[i]=update

new_df = pd.DataFrame(data, 
               columns =['Country','Total_Cases','Deaths','Recovered','Date'])

df_countrydate= new_df.groupby(['Country','Date']).sum().reset_index()

# Creating Choropleth Maps for each array
fig_total = px.choropleth(df_countrydate, 
                    locations="Country", 
                    locationmode = "country names",
                    color="Total_Cases", 
                    hover_name="Country", 
                    animation_frame="Date",
                    color_continuous_scale="Blues",
                   )
fig_total.update_layout(
    title_text = 'Global Spread of Coronavirus',
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
    )
)

fig_recover = px.choropleth(df_countrydate, 
                    locations="Country", 
                    locationmode = "country names",
                    color="Recovered", 
                    hover_name="Country", 
                    animation_frame="Date",
                    color_continuous_scale="Greens",
                   )
fig_recover.update_layout(
    title_text = 'Recovered per Country',
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
    )
)

fig_death = px.choropleth(df_countrydate, 
                    locations="Country", 
                    locationmode = "country names",
                    color="Deaths", 
                    hover_name="Country", 
                    animation_frame="Date",
                    color_continuous_scale="OrRd",
                   )
fig_death.update_layout(
    title_text = 'Deaths per Country',
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
    )
)

# Deploying web page

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("Corona Virus affect on the World")
        ]),
        html.Div([
            dcc.Graph( figure=fig_total),
            dcc.Graph( figure=fig_recover),
            dcc.Graph( figure=fig_death),
        ])
    ],className="map"),
    html.Div([
        html.H1("Compare Curves")
    ],style={"text-align": "center"}),
    html.Div([
        dcc.Dropdown(
            id='countries1',
            options=[{'label': i, 'value': i} for i in country],
            value='Countries',
            placeholder="Select a country",
            clearable=False,
            style={'float': 'right','margin': 'auto','width':'33%'}
        ),
        dcc.Dropdown(
            id='countries2',
            options=[{'label': i, 'value': i} for i in country],
            value='Countries',
            placeholder="Select a country",
            clearable=False,
            style={'float': 'right','margin': 'auto','width':'33%'}
        ),
        dcc.Dropdown(
            id='countries3',
            options=[{'label': i, 'value': i} for i in country],
            value='Countries',
            placeholder="Select a country",
            clearable=False,
            style={'float': 'right','margin': 'auto','width':'33%'}
        )
    ], className= 'select_country'),

    html.Div([
        dcc.Graph(
            id='scatterplot',
        )
    ]),
])

# Update Scatter plot
@app.callback(
    dash.dependencies.Output('scatterplot', 'figure'),
    [dash.dependencies.Input('countries1', 'value'), 
     dash.dependencies.Input('countries2', 'value'),
     dash.dependencies.Input('countries3', 'value')])

def update_graph(country_to_display1,country_to_display2,country_to_display3):

    if(country_to_display1=="Countries") and (country_to_display2=="Countries") and (country_to_display3=="Countries"):
        traces = [go.Scatter(x=[0],
                         y=[0],)] #default scatter plot when nothing selected

    elif (country_to_display1!="Countries") and (country_to_display2!="Countries") and (country_to_display3!="Countries"):
        arr1 = [] #Array for dates
        arr2 = [] #Array for 1st country data
        arr3 = [] #Array for 2nd country data
        arr4 = [] #Array for 3rd country data

        index1= s_data_new.loc[s_data_new['Country']==str(country_to_display1)].index #find index of country
        index2= s_data_new.loc[s_data_new['Country']==str(country_to_display2)].index
        index3= s_data_new.loc[s_data_new['Country']==str(country_to_display3)].index

        for i in range(4, len(df.columns)):
            arr1.append(df.columns[i]) 
            arr2.append(s_data_new[df.columns[i]][index1[0]])
            arr3.append(s_data_new[df.columns[i]][index2[0]])
            arr4.append(s_data_new[df.columns[i]][index3[0]])

        #updated scatter plot
        traces = [go.Scatter(x=arr1,
                            y=arr2,
                            name=country_to_display1),
                    go.Scatter(x=arr1,
                            y=arr3,
                            name=country_to_display2),
                    go.Scatter(x=arr1,
                            y=arr4,
                            name=country_to_display3),] 
    
    elif ((country_to_display1!="Countries") and (country_to_display2!="Countries")) or ((country_to_display1!="Countries") and (country_to_display3!="Countries")) or ((country_to_display3!="Countries") and (country_to_display2!="Countries")):
        arr1 = []
        arr2 = []
        arr3 = []
        if(country_to_display1!="Countries" and country_to_display2!="Countries"):
            target1= country_to_display1
            target2= country_to_display2
        elif(country_to_display2!="Countries" and country_to_display3!="Countries"):
            target1= country_to_display2
            target2= country_to_display3
        elif(country_to_display1!="Countries" and country_to_display3!="Countries"):
            target1= country_to_display1
            target2= country_to_display3

        index1= s_data_new.loc[s_data_new['Country']==str(target1)].index
        index2= s_data_new.loc[s_data_new['Country']==str(target2)].index
        for i in range(4, len(df.columns)):
            arr1.append(df.columns[i])
            arr2.append(s_data_new[df.columns[i]][index1[0]])
            arr3.append(s_data_new[df.columns[i]][index2[0]])

        traces = [go.Scatter(x=arr1,
                            y=arr2,
                            name=target1),
                    go.Scatter(x=arr1,
                            y=arr3,
                            name=target2)]     

    elif (country_to_display1!="Countries") or (country_to_display2!="Countries") or (country_to_display3!="Countries"):

        arr1 = []
        arr2 = []
        arr3 = []

        if(country_to_display1!="Countries"):
            target= country_to_display1
        elif(country_to_display2!="Countries"):
            target= country_to_display2
        elif(country_to_display3!="Countries"):
            target= country_to_display3

        index= s_data_new.loc[s_data_new['Country']==str(target)].index

        for i in range(4, len(df.columns)):
            arr1.append(df.columns[i])
            arr2.append(s_data_new[df.columns[i]][index[0]])
        traces = [go.Scatter(x=arr1,
                            y=arr2,
                            name=country_to_display1)]         

    return {
        'data': traces,
        'layout': go.Layout(title=country_to_display1)
    }


app.run_server(debug=True, use_reloader=False)