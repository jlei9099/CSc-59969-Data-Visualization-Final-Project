# coding=utf-8
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv')

df = df.rename(columns={"Country/Region": "Country", "Province/State": "Province"})
deaths = deaths.rename(columns={"Country/Region": "Country", "Province/State": "Province"})
recovered = recovered.rename(columns={"Country/Region": "Country", "Province/State": "Province"})
arr = []

for date in range(4, len(df.columns)):
    total_list = df.groupby('Country')[df.columns[date]].sum().tolist()
    arr.append(total_list)

deathsarr = []
for date in range(4, len(deaths.columns)):
    total_list = deaths.groupby('Country')[deaths.columns[date]].sum().tolist()
    deathsarr.append(total_list)

recoveredarr = []
for date in range(4, len(recovered.columns)):
    total_list = recovered.groupby('Country')[recovered.columns[date]].sum().tolist()
    recoveredarr.append(total_list)

country_list = df["Country"].tolist()
country_set = set(country_list)
country_list = list(country_set)
country_list.sort()
arr1 = []
repeat_dates = []

for x in range(len(arr)):
    arr1.append(list(zip(country_list, arr[x], deathsarr[x], recoveredarr[x])))

for i in range(4, len(df.columns)):
    for x in range(len(arr1[0])):
        repeat_dates.append(df.columns[i])

data = []
for i in range(len(arr1)):
    for x in range(len(arr1[i])):
        data.append(arr1[i][x])

for i in range(len(data)):
    date = (repeat_dates[i],)
    update = data[i] + date
    data[i] = update

new_df = pd.DataFrame(data, columns=['Country', 'Total_Cases', 'Deaths', 'Recovered', 'Date'])

df_countrydate = new_df.groupby(['Country', 'Date']).sum().reset_index()

colors = ["#F9F9F5", "#FAFAE6", "#FCFCCB", "#FCFCAE", "#FCF1AE", "#FCEA7D", "#FCD97D",
          "#FCCE7D", "#FCC07D", "#FEB562", "#F9A648", "#F98E48", "#FD8739", "#FE7519",
          "#FE5E19", "#FA520A", "#FA2B0A", "#9B1803", "#861604", "#651104", "#570303", ]

fig = px.choropleth(df_countrydate,
                    locations="Country",
                    locationmode="country names",
                    color="Total_Cases",
                    hover_name="Country",
                    animation_frame="Date",
                    color_continuous_scale="Blues",
                    )
fig.update_layout(
    title_text='Global Spread of Coronavirus',
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=False,
    )
)

app = dash.Dash()
app.layout = html.Div([
    html.Div([
        html.Button('Total Cases', id='btn-nclicks-1', n_clicks=0),
        html.Button('Recovered', id='btn-nclicks-2', n_clicks=0),
        html.Button('Deaths', id='btn-nclicks-3', n_clicks=0),
        html.Div(id='container-button-timestamp')
    ]),
    html.Div([
        dcc.Graph(id='world_map', figure=fig)
    ]),
    html.Div([

    ]),
    html.Div([

    ])
])

@app.callback(
    Output(component_id='world_map', component_property='figure'),
    [Input('btn-nclicks-1', 'n_clicks'),
     Input('btn-nclicks-2', 'n_clicks'),
     Input('btn-nclicks-3', 'n_clicks')]
)
def displayClick(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        fig_up = px.choropleth(df_countrydate,
                               locations="Country",
                               locationmode="country names",
                               color="Total_Cases",
                               hover_name="Country",
                               animation_frame="Date",
                               color_continuous_scale="Blues",
                               )
        fig_up.update_layout(
            title_text='Global Spread of Coronavirus',
            title_x=0.5,
            geo=dict(
                showframe=False,
                showcoastlines=False,
            )
        )
    elif 'btn-nclicks-2' in changed_id:
        fig_up = px.choropleth(df_countrydate,
                               locations="Country",
                               locationmode="country names",
                               color="Recovered",
                               hover_name="Country",
                               animation_frame="Date",
                               color_continuous_scale="Greens",
                               )
        fig_up.update_layout(
            title_text='Recovered per Country',
            title_x=0.5,
            geo=dict(
                showframe=False,
                showcoastlines=False,
            )
        )
    elif 'btn-nclicks-3' in changed_id:
        fig_up = px.choropleth(df_countrydate,
                               locations="Country",
                               locationmode="country names",
                               color="Deaths",
                               hover_name="Country",
                               animation_frame="Date",
                               color_continuous_scale="OrRd",
                               )
        fig_up.update_layout(
            title_text='Deaths per Country',
            title_x=0.5,
            geo=dict(
                showframe=False,
                showcoastlines=False,
            )
        )
    else:
        fig_up = px.choropleth(df_countrydate,
                               locations="Country",
                               locationmode="country names",
                               color="Total_Cases",
                               hover_name="Country",
                               animation_frame="Date",
                               color_continuous_scale="Blues",
                               )
        fig_up.update_layout(
            title_text='Global Spread of Coronavirus',
            title_x=0.5,
            geo=dict(
                showframe=False,
                showcoastlines=False,
            )
        )

    return fig_up


app.run_server(debug=True, use_reloader=False)