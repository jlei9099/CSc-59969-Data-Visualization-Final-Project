# coding=utf-8
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
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

compare=[]

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("Corona Virus affect on the World")
        ]),
        html.Div([
            dcc.Graph(id='graph2', figure=fig_recover),
            dcc.Graph(id='graph3', figure=fig_death),
        ])
    ],className="map"),
    html.Div([
        dcc.Graph(id='graph1', figure=fig_total),
    ]),
    html.Div([
        html.H1("Compare Curves")
    ],style={"text-align": "center"}),
    html.Div(
        id="test"),
    html.Div([
        dcc.Graph(
            id='scatterplot',
        )
    ]),
])


@app.callback(Output('scatterplot', 'figure'), [Input("graph1", "clickData")])

def event_cb(data):
    if data is None:    
        traces = [go.Scatter(x=[0],
                          y=[0],)] 
    else:
        country_selec= data['points'][0]['location']
        # if data1 is not None:
        #     country_selec= data1['points'][0]['location']
        # elif data2 is not None:
        #     country_selec= data2['points'][0]['location']
        # else:
        #     country_selec= data3['points'][0]['location']

        if country_selec in compare:
            compare.remove(country_selec)
        else:
            compare.append(country_selec)

        indexes=[]
        for country in compare:
            index=s_data_new.loc[s_data_new['Country']==str(country)].index
            indexes.append(index[0])

        date_store = []
        col_length= len(df.columns) - 4
        row_length= len(indexes)
        storage= [[0 for i in range(col_length)] for j in range(row_length)]
        
        for i in range(4, len(df.columns)):
            date_store.append(df.columns[i]) 
            for x in range(len(indexes)):
                storage[x][i-4]=(s_data_new[df.columns[i]][indexes[x]])

        traces = [] 

        for i in range(len(storage)):
            trace=go.Scatter(x=date_store,
                            y=storage[i],
                            name=s_data_new['Country'][indexes[i]])
            traces.append(trace)
        
    return {
        'data': traces,
        'layout': go.Layout(title="Countries")
    }








app.run_server(debug=True, use_reloader=False)