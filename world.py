# coding=utf-8
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

df = pd.read_csv(
    'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv')
df.drop(df.columns[[0, 2, 3]], axis=1, inplace=True)
country = df['Country/Region'].unique()
# print(df.columns[1]) colum name
# print(len(df.columns)) length of columns
# print(len(df[df.columns[1]])) row search
# print(df[df.columns[88]][3]) col/row search

arr1 = []
arr2 = []

app = dash.Dash()
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='countries1',
            options=[{'label': i, 'value': i} for i in country],
            value='Countries',
            placeholder="Select a country",
            clearable=False,
        ),
        dcc.Dropdown(
            id='countries2',
            options=[{'label': i, 'value': i} for i in country],
            value='Countries',
            placeholder="Select a country",
            clearable=False,
        ),
        dcc.Dropdown(
            id='countries3',
            options=[{'label': i, 'value': i} for i in country],
            value='Countries',
            placeholder="Select a country",
            clearable=False,
        )
    ], style={'width': '40%'}),

    html.Div([
        dcc.Graph(
            id='scatterplot',
        )
    ]),
])

@app.callback(
    dash.dependencies.Output('scatterplot', 'figure'),
    [dash.dependencies.Input('countries1', 'value'),
     dash.dependencies.Input('countries2', 'value'),
     dash.dependencies.Input('countries3', 'value')])
def update_graph(country_to_display1, country_to_display2, country_to_display3):
    if (country_to_display1 == "Countries") and (country_to_display2 == "Countries") and (
            country_to_display3 == "Countries"):
        traces = [go.Scatter(x=[0],
                             y=[0], )]

    elif (country_to_display1 != "Countries") and (country_to_display2 != "Countries") and (
            country_to_display3 != "Countries"):
        arr1 = []
        arr2 = []
        arr3 = []
        arr4 = []

        index1 = df.loc[df['Country/Region'] == str(country_to_display1)].index
        index2 = df.loc[df['Country/Region'] == str(country_to_display2)].index
        index3 = df.loc[df['Country/Region'] == str(country_to_display3)].index

        for i in range(1, len(df.columns)):
            arr1.append(df.columns[i])
            arr2.append(df[df.columns[i]][index1[0]])
            arr3.append(df[df.columns[i]][index2[0]])
            arr4.append(df[df.columns[i]][index3[0]])

        traces = [go.Scatter(x=arr1,
                             y=arr2,
                             name=country_to_display1),
                  go.Scatter(x=arr1,
                             y=arr3,
                             name=country_to_display2),
                  go.Scatter(x=arr1,
                             y=arr4,
                             name=country_to_display3), ]

    elif ((country_to_display1 != "Countries") and (country_to_display2 != "Countries")) or (
            (country_to_display1 != "Countries") and (country_to_display3 != "Countries")) or (
            (country_to_display3 != "Countries") and (country_to_display2 != "Countries")):
        arr1 = []
        arr2 = []
        arr3 = []
        if (country_to_display1 != "Countries" and country_to_display2 != "Countries"):
            target1 = country_to_display1
            target2 = country_to_display2
        elif (country_to_display2 != "Countries" and country_to_display3 != "Countries"):
            target1 = country_to_display2
            target2 = country_to_display3
        elif (country_to_display1 != "Countries" and country_to_display3 != "Countries"):
            target1 = country_to_display1
            target2 = country_to_display3

        index1 = df.loc[df['Country/Region'] == str(target1)].index
        index2 = df.loc[df['Country/Region'] == str(target2)].index
        for i in range(1, len(df.columns)):
            arr1.append(df.columns[i])
            arr2.append(df[df.columns[i]][index1[0]])
            arr3.append(df[df.columns[i]][index2[0]])

        traces = [go.Scatter(x=arr1,
                             y=arr2,
                             name=target1),
                  go.Scatter(x=arr1,
                             y=arr3,
                             name=target2)]

    elif (country_to_display1 != "Countries") or (country_to_display2 != "Countries") or (
            country_to_display3 != "Countries"):

        arr1 = []
        arr2 = []
        arr3 = []

        if (country_to_display1 != "Countries"):
            target = country_to_display1
        elif (country_to_display2 != "Countries"):
            target = country_to_display2
        elif (country_to_display3 != "Countries"):
            target = country_to_display3

        index = df.loc[df['Country/Region'] == str(target)].index

        for i in range(1, len(df.columns)):
            arr1.append(df.columns[i])
            arr2.append(df[df.columns[i]][index[0]])
        traces = [go.Scatter(x=arr1,
                             y=arr2,
                             name=country_to_display1)]

    return {
        'data': traces,
        'layout': go.Layout(title=country_to_display1)
    }

app.run_server(debug=True, use_reloader=False)