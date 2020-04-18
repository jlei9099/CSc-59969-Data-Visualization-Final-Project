import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/jlei9099/CSc-59969-Data-Visualization-Final-Project/master/COVID-19%20Data%20Set%20-%20Sheet.csv')

pv = pd.pivot_table(df, index=['Country'], values=['Total Cases'], aggfunc=sum, fill_value=0)
trace1 = go.Bar(x=pv.index, y=pv[('Total Cases', 'Total Deaths')], name='Total Deaths')
trace2 = go.Bar(x=pv.index, y=pv[('Total Cases', 'Total Recovered')], name='Total Recovered')

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='COVID-19'),
    dcc.Graph(
        id='graph',
        figure={
            'data': [trace1, trace2],
            'layout':
            go.Layout(title='Recoveries vs. Deaths', barmode='stack')
        })
])

if __name__ == '__main__':
    app.run_server(debug=True)