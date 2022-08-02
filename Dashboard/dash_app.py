import dash
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import Output, Input
import plotly.express as px

from dashboard_contents import tab1, tab2
from Operations import Database, DailyPredictions, Employees, Predictions
from Predictions import make_predictions, write_predictions

dashboard = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # dashboard app instantiation

# dashboard layout start ------------------------------------------------------------------------------------------------
dashboard.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            [
                dbc.NavItem(
                    [
                        dbc.Button("Update Dashboard", id='update_button', color="success", className="me-1"),
                        dbc.Button("Logout", id='logout_button', color="warning", className="me-1"),
                    ]
                ),
            ], brand="Employee stress predictor", color="primary", dark=True,
        ),

        dbc.Alert(id='update_alert1', is_open=False, dismissable=True),
        dbc.Alert(id='update_alert2', is_open=False, dismissable=True),

        dbc.Tabs(
            [
                dbc.Tab(tab1.content, id='tab1', label='All Analyze', activeTabClassName='fw-bold'),
                dbc.Tab(tab2.content, id='tab2', label='Employee Analyze', activeTabClassName='fw-bold'),
            ]
        ),

    ], id='container'
)


# callback functions ----------------------------------------------------------------------------------------------------

@dashboard.callback((Output('update_alert1', 'children')),
                    Output('update_alert1', 'color'),
                    Output('update_alert1', 'is_open'),
                    Output('update_alert1', 'duration'),
                    Input('update_button', 'n_clicks')
                    )
def alert1(update_button):
    db = Database('manager', 'zjlHHS5cNcCAT39C')
    db.make_connection()
    children = 'Waiting for Dashboard updating...'
    color = 'primary'
    is_open = True
    duration1 = 57000
    return children, color, is_open, duration1


@dashboard.callback(Output('update_alert2', 'children'),
                    Output('update_alert2', 'color'),
                    Output('update_alert2', 'is_open'),
                    Output('update_alert2', 'duration'),
                    Input("line_graph", 'figure')
                    )
def dashboard_update(line_graph):
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    employees = ['emp001', 'emp002', 'emp003', 'emp004', 'emp005']

    for employee in employees:
        predictions = make_predictions('2022-03-31', employee)
        print(write_predictions(predictions))
        # print(date)

    children = "Dashboard successfully updated."
    color = 'success'
    is_open2 = True
    duration2 = 2500

    return children, color, is_open2, duration2


@dashboard.callback(Output("pie_chart1", 'figure'),
                    Input('update_alert1', 'children'))
def pie_current(update_alert1):
    date = '2022-03-05'

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    print(f'daily percentages-------------{daily_percentages_list}')

    for dpl in daily_percentages_list:
        new_dpl = str(dpl[0]).split(' ')
        print(new_dpl)
        if new_dpl[0] == date:
            today_percentages = dpl[1]
            print(f"today-----------{today_percentages}")
            break

    data = {'Emotion': ['Anger', 'Other'],
            'percentage': [today_percentages['Anger'], 100.0 - today_percentages['Anger']]}

    df = pd.DataFrame(data)
    fig1 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig1.update_traces(textfont_size=1,
                       marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig1.update_layout(title_text=data['Emotion'][0],
                       margin=dict(l=10, r=10, t=35, b=10),
                       annotations=[
                           dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                       )
    return fig1


@dashboard.callback(Output("pie_chart2", 'figure'),
                    Input('pie_chart1', 'figure'))
def pie_current(pie_chart1):
    date = '2022-03-05'

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    print(f'daily percentages-------------{daily_percentages_list}')

    for dpl in daily_percentages_list:
        new_dpl = str(dpl[0]).split(' ')
        print(new_dpl)
        if new_dpl[0] == date:
            today_percentages = dpl[1]
            print(f"today-----------{today_percentages}")
            break

    data = {'Emotion': ['Disgust', 'Other'],
            'percentage': [today_percentages['Disgust'], 100.0 - today_percentages['Disgust']]}

    df = pd.DataFrame(data)
    fig2 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig2.update_traces(textfont_size=1,
                       marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig2.update_layout(title_text=data['Emotion'][0],
                       margin=dict(l=10, r=10, t=35, b=10),
                       annotations=[
                           dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                       )
    return fig2


@dashboard.callback(Output("pie_chart3", 'figure'),
                    Input('pie_chart2', 'figure'))
def pie_current(pie_chart2):
    date = '2022-03-05'

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    print(f'daily percentages-------------{daily_percentages_list}')

    for dpl in daily_percentages_list:
        new_dpl = str(dpl[0]).split(' ')
        print(new_dpl)
        if new_dpl[0] == date:
            today_percentages = dpl[1]
            print(f"today-----------{today_percentages}")
            break

    data = {'Emotion': ['Fear', 'Other'],
            'percentage': [today_percentages['Fear'], 100.0 - today_percentages['Fear']]}

    df = pd.DataFrame(data)
    fig3 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig3.update_traces(textfont_size=1,
                       marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig3.update_layout(title_text=data['Emotion'][0],
                       margin=dict(l=10, r=10, t=35, b=10),
                       annotations=[
                           dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                       )
    return fig3


@dashboard.callback(Output("pie_chart4", 'figure'),
                    Input('pie_chart3', 'figure'))
def pie_current(pie_chart3):
    date = '2022-03-05'

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    print(f'daily percentages-------------{daily_percentages_list}')

    for dpl in daily_percentages_list:
        new_dpl = str(dpl[0]).split(' ')
        print(new_dpl)
        if new_dpl[0] == date:
            today_percentages = dpl[1]
            print(f"today-----------{today_percentages}")
            break

    data = {'Emotion': ['Happy', 'Other'],
            'percentage': [today_percentages['Happy'], 100.0 - today_percentages['Happy']]}

    df = pd.DataFrame(data)
    fig4 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig4.update_traces(textfont_size=1,
                       marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig4.update_layout(title_text=data['Emotion'][0],
                       margin=dict(l=10, r=10, t=35, b=10),
                       annotations=[
                           dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                       )
    return fig4


@dashboard.callback(Output("pie_chart5", 'figure'),
                    Input('pie_chart4', 'figure'))
def pie_current(pie_chart4):
    date = '2022-03-05'

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    print(f'daily percentages-------------{daily_percentages_list}')

    for dpl in daily_percentages_list:
        new_dpl = str(dpl[0]).split(' ')
        print(new_dpl)
        if new_dpl[0] == date:
            today_percentages = dpl[1]
            print(f"today-----------{today_percentages}")
            break

    data = {'Emotion': ['Neutral', 'Other'],
            'percentage': [today_percentages['Neutral'], 100.0 - today_percentages['Neutral']]}

    df = pd.DataFrame(data)
    fig5 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig5.update_traces(textfont_size=1,
                       marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig5.update_layout(title_text=data['Emotion'][0],
                       margin=dict(l=10, r=10, t=35, b=10),
                       annotations=[
                           dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                       )
    return fig5


@dashboard.callback(Output("pie_chart6", 'figure'),
                    Input('pie_chart5', 'figure'))
def pie_current(pie_chart5):
    date = '2022-03-05'

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    print(f'daily percentages-------------{daily_percentages_list}')

    for dpl in daily_percentages_list:
        new_dpl = str(dpl[0]).split(' ')
        print(new_dpl)
        if new_dpl[0] == date:
            today_percentages = dpl[1]
            print(f"today-----------{today_percentages}")
            break

    data = {'Emotion': ['Sad', 'Other'],
            'percentage': [today_percentages['Sad'], 100.0 - today_percentages['Sad']]}

    df = pd.DataFrame(data)
    fig6 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig6.update_traces(textfont_size=1,
                       marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig6.update_layout(title_text=data['Emotion'][0],
                       margin=dict(l=10, r=10, t=35, b=10),
                       annotations=[
                           dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                       )
    return fig6


@dashboard.callback(Output("pie_chart7", 'figure'),
                    Input('pie_chart6', 'figure'))
def pie_current(pie_chart6):
    date = '2022-03-05'

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    print(f'daily percentages-------------{daily_percentages_list}')

    for dpl in daily_percentages_list:
        new_dpl = str(dpl[0]).split(' ')
        print(new_dpl)
        if new_dpl[0] == date:
            today_percentages = dpl[1]
            print(f"today-----------{today_percentages}")
            break

    data = {'Emotion': ['Surprise', 'Other'],
            'percentage': [today_percentages['Surprise'], 100.0 - today_percentages['Surprise']]}

    df = pd.DataFrame(data)
    fig7 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig7.update_traces(textfont_size=1,
                       marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig7.update_layout(title_text=data['Emotion'][0],
                       margin=dict(l=10, r=10, t=35, b=10),
                       annotations=[
                           dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                       )
    return fig7


@dashboard.callback(Output("line_graph", 'figure'),
                    Input("pie_chart7", 'figure'))
def bar_chart(pie_chart7):

    date = DailyPredictions.objects.only('date')
    date_list = []
    for d in date:
        date_list.append(d.date)

    avg_stress = DailyPredictions.objects.only('average_stress_percentage')
    avg_list = []
    for al in avg_stress:
        avg_list.append(al.average_stress_percentage)

    data = np.array([date_list, avg_list])
    data = {'date': data[0], 'average stress': data[1]}

    df = pd.DataFrame(data)

    fig = px.bar(df, x='date', y='average stress')

    return fig


# -------------------------------------------------------------------------------------------------------------------------------------------------
# Tab2 callbacks
@dashboard.callback(Output("pie_chart1e", 'figure'),
                    Input('search_emp_id', 'value'))
def pie_current(search_emp_id):
    emp_id_dropdown = search_emp_id

    date = '2022-03-05'

    daily_personal_percentages = Predictions.objects.only('emp_id', 'emo_percentages', 'date')

    for dpp in daily_personal_percentages:
        if (emp_id_dropdown == dpp.emp_id) and (date == str(dpp.date).split(' ')[0]):
            today_personal_percentages = dpp.emo_percentages

    data = {'Emotion': ['Anger', 'Other'],
            'percentage': [today_personal_percentages['Anger'], 100.0 - today_personal_percentages['Anger']]}

    df = pd.DataFrame(data)

    fig1e = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig1e.update_traces(textfont_size=1,
                        marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig1e.update_layout(title_text=data['Emotion'][0],
                        margin=dict(l=10, r=10, t=35, b=10),
                        annotations=[
                            dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig1e


# ----------------------------------------------------------------------------------------------------------------------

@dashboard.callback(Output("pie_chart2e", 'figure'),
                    Input('search_emp_id', 'value'))
def pie_current(search_emp_id):
    emp_id_dropdown = search_emp_id

    date = '2022-03-05'

    daily_personal_percentages = Predictions.objects.only('emp_id', 'emo_percentages', 'date')

    for dpp in daily_personal_percentages:
        if (emp_id_dropdown == dpp.emp_id) and (date == str(dpp.date).split(' ')[0]):
            today_personal_percentages = dpp.emo_percentages

    data = {'Emotion': ['Disgust', 'Other'],
            'percentage': [today_personal_percentages['Disgust'], 100.0 - today_personal_percentages['Disgust']]}

    df = pd.DataFrame(data)

    fig2e = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig2e.update_traces(textfont_size=1,
                        marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig2e.update_layout(title_text=data['Emotion'][0],
                        margin=dict(l=10, r=10, t=35, b=10),
                        annotations=[
                            dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig2e


# ----------------------------------------------------------------------------------------------------------------------

@dashboard.callback(Output("pie_chart3e", 'figure'),
                    Input('search_emp_id', 'value'))
def pie_current(search_emp_id):
    emp_id_dropdown = search_emp_id

    date = '2022-03-05'

    daily_personal_percentages = Predictions.objects.only('emp_id', 'emo_percentages', 'date')

    for dpp in daily_personal_percentages:
        if (emp_id_dropdown == dpp.emp_id) and (date == str(dpp.date).split(' ')[0]):
            today_personal_percentages = dpp.emo_percentages

    data = {'Emotion': ['Fear', 'Other'],
            'percentage': [today_personal_percentages['Fear'], 100.0 - today_personal_percentages['Fear']]}

    df = pd.DataFrame(data)

    fig3e = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig3e.update_traces(textfont_size=1,
                        marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig3e.update_layout(title_text=data['Emotion'][0],
                        margin=dict(l=10, r=10, t=35, b=10),
                        annotations=[
                            dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig3e


# ----------------------------------------------------------------------------------------------------------------------

@dashboard.callback(Output("pie_chart4e", 'figure'),
                    Input('search_emp_id', 'value'))
def pie_current(search_emp_id):
    emp_id_dropdown = search_emp_id

    date = '2022-03-05'

    daily_personal_percentages = Predictions.objects.only('emp_id', 'emo_percentages', 'date')

    for dpp in daily_personal_percentages:
        if (emp_id_dropdown == dpp.emp_id) and (date == str(dpp.date).split(' ')[0]):
            today_personal_percentages = dpp.emo_percentages

    data = {'Emotion': ['Happy', 'Other'],
            'percentage': [today_personal_percentages['Happy'], 100.0 - today_personal_percentages['Happy']]}

    df = pd.DataFrame(data)

    fig4e = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig4e.update_traces(textfont_size=1,
                        marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig4e.update_layout(title_text=data['Emotion'][0],
                        margin=dict(l=10, r=10, t=35, b=10),
                        annotations=[
                            dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig4e


# ----------------------------------------------------------------------------------------------------------------------

@dashboard.callback(Output("pie_chart5e", 'figure'),
                    Input('search_emp_id', 'value'))
def pie_current(search_emp_id):
    emp_id_dropdown = search_emp_id

    date = '2022-03-05'

    daily_personal_percentages = Predictions.objects.only('emp_id', 'emo_percentages', 'date')

    for dpp in daily_personal_percentages:
        if (emp_id_dropdown == dpp.emp_id) and (date == str(dpp.date).split(' ')[0]):
            today_personal_percentages = dpp.emo_percentages

    data = {'Emotion': ['Neutral', 'Other'],
            'percentage': [today_personal_percentages['Neutral'], 100.0 - today_personal_percentages['Neutral']]}

    df = pd.DataFrame(data)

    fig5e = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig5e.update_traces(textfont_size=1,
                        marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig5e.update_layout(title_text=data['Emotion'][0],
                        margin=dict(l=10, r=10, t=35, b=10),
                        annotations=[
                            dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig5e


# ----------------------------------------------------------------------------------------------------------------------

@dashboard.callback(Output("pie_chart6e", 'figure'),
                    Input('search_emp_id', 'value'))
def pie_current(search_emp_id):
    emp_id_dropdown = search_emp_id

    date = '2022-03-05'

    daily_personal_percentages = Predictions.objects.only('emp_id', 'emo_percentages', 'date')

    for dpp in daily_personal_percentages:
        if (emp_id_dropdown == dpp.emp_id) and (date == str(dpp.date).split(' ')[0]):
            today_personal_percentages = dpp.emo_percentages

    data = {'Emotion': ['Sad', 'Other'],
            'percentage': [today_personal_percentages['Sad'], 100.0 - today_personal_percentages['Sad']]}

    df = pd.DataFrame(data)

    fig6e = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig6e.update_traces(textfont_size=1,
                        marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig6e.update_layout(title_text=data['Emotion'][0],
                        margin=dict(l=10, r=10, t=35, b=10),
                        annotations=[
                            dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig6e


# ----------------------------------------------------------------------------------------------------------------------

@dashboard.callback(Output("pie_chart7e", 'figure'),
                    Input('search_emp_id', 'value'))
def pie_current(search_emp_id):
    emp_id_dropdown = search_emp_id

    date = '2022-03-05'

    daily_personal_percentages = Predictions.objects.only('emp_id', 'emo_percentages', 'date')

    for dpp in daily_personal_percentages:
        if (emp_id_dropdown == dpp.emp_id) and (date == str(dpp.date).split(' ')[0]):
            today_personal_percentages = dpp.emo_percentages

    data = {'Emotion': ['Surprise', 'Other'],
            'percentage': [today_personal_percentages['Surprise'], 100.0 - today_personal_percentages['Surprise']]}

    df = pd.DataFrame(data)

    fig7e = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig7e.update_traces(textfont_size=1,
                        marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig7e.update_layout(title_text=data['Emotion'][0],
                        margin=dict(l=10, r=10, t=35, b=10),
                        annotations=[
                            dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
    return fig7e


# ----------------------------------------------------------------------------------------------------------------------

@dashboard.callback(Output("line_graph_e", 'figure'),
                    Input('search_emp_id', 'value'))
def bar_chart(search_emp_id):
    emp_id_dropdown = search_emp_id
    date_list = []
    stress_percentage_list = []

    daily_personal_stress = Predictions.objects.only('emp_id', 'stress_percentage', 'date')

    for dps in daily_personal_stress:
        if emp_id_dropdown == dps.emp_id:
            date_list.append(dps.date)
            stress_percentage_list.append(dps.stress_percentage)

            data = np.array([date_list, stress_percentage_list])
            data = {'date': data[0], 'stress percentage': data[1]}

            df = pd.DataFrame(data)

            fig = px.bar(df, x='date', y='stress percentage')

    return fig


# running the dashboard app
if __name__ == '__main__':
    dashboard.run_server(debug=True)
