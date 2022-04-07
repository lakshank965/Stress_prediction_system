import dash
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import Output, Input
import plotly.express as px

from dashboard_contents import tab1
from Operations import Database, DailyPredictions
from Predictions import make_predictions, write_predictions

# emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
# employee = ['emp001', 'emp002', 'emp003', 'emp004', 'emp005']
# date = '2022-03-15'
#
# predictions = make_predictions(date, 'emp001')
# print(write_predictions(predictions))


dashboard = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # dashboard app instantiation

# dashboard layout start ------------------------------------------------------------------------------------------------
dashboard.layout = dbc.Container(
    [
        html.H1('Hello, World!'),

        dbc.Button("Update Dashboard", id='update_button', color="primary", className="me-1"),

        dbc.Alert(id='update_alert', is_open=True, duration=15000),

        dbc.Tabs(
            [
                dbc.Tab(tab1.content, id='tab1', label='first tab', activeTabClassName='fw-bold'),
                # dbc.Tab(tab1.content, id='tab2', label='Second tab', activeTabClassName='fw-bold'),
                # dbc.Tab(tab1.content, id='tab3', label='third tab', activeTabClassName='fw-bold'),
            ]
        )
    ], id='container'
)


# callback functions ----------------------------------------------------------------------------------------------------

@dashboard.callback(Output('update_alert', 'children'),
                    Input('update_button', 'n_clicks'))
def dashboard_update(update_button):
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    employee = ['emp001', 'emp002', 'emp003', 'emp004', 'emp005']
    date = '2022-03-16'

    predictions = make_predictions(date, 'emp001')
    print(write_predictions(predictions))

    update_alert = "Dashboard successfully updated."

    return update_alert


@dashboard.callback(Output("line_graph", 'figure'),
                    Input('container', 'children'))
def bar_chart(container):
    db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
    db.make_connection()

    date = DailyPredictions.objects.only('date')
    date_list = []
    for d in date:
        date_list.append(d.date)

    # print(f'date-------------{date_list}')

    avg_stress = DailyPredictions.objects.only('average_stress_percentage')
    avg_list = []
    for al in avg_stress:
        avg_list.append(al.average_stress_percentage)

    data = np.array([date_list, avg_list])
    # data = np.transpose(data)
    data = {'date': data[0], 'average stress': data[1]}

    df = pd.DataFrame(data)
    # print('----------------------------------------------------------------------------------------------------------')
    # print(df)

    fig = px.bar(df, x='date', y='average stress')
    return fig


# running the dashboard app
if __name__ == '__main__':
    dashboard.run_server(debug=True)
