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


# emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
# employee = ['emp001', 'emp002', 'emp003', 'emp004', 'emp005']
# # date = '2022-03-15'
#
# for d in range(1, 31):
#     date = f'2022-03-{d}'
#     for e in employee:
#         predictions = make_predictions(date, e)
#         print(write_predictions(predictions))


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

        # dbc.Alert(id='update_alert', is_open=True, duration=15000),
        dbc.Alert(id='update_alert', is_open=True),

        dbc.Tabs(
            [
                dbc.Tab(tab1.content, id='tab1', label='All Analyze', activeTabClassName='fw-bold'),
                dbc.Tab(tab2.content, id='tab2', label='Employee Analyze', activeTabClassName='fw-bold'),
                # dbc.Tab(tab1.content, id='tab3', label='third tab', activeTabClassName='fw-bold'),
            ]
        ),


    ], id='container'
)


# callback functions ----------------------------------------------------------------------------------------------------

@dashboard.callback(Output('update_alert', 'children'),
                    Input('update_button', 'n_clicks')
                    )
def dashboard_update(update_button):
    db = Database('manager', 'zjlHHS5cNcCAT39C')
    db.make_connection()
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    employees = ['emp001', 'emp002', 'emp003', 'emp004', 'emp005']

    # emp_db = Database('find-user-type', 'PAvO0FAVjc4KXkiE')
    # emp_db.make_connection()
    # emp = Employees.objects.only('status')
    # for e in emp:
    #     if e.status == 'employee':
    #         employees.append(e.emp_id)
    # emp_db.close_connection()

    # for d in range(1, 31):
    #     date = f'2022-03-{d}'

    for employee in employees:
        predictions = make_predictions('2022-03-31', employee)
        print(write_predictions(predictions))
        # print(date)

    update_alert = "Dashboard successfully updated."

    return update_alert


@dashboard.callback(Output("line_graph", 'figure'),
                    Input("pie_chart7", 'figure'))
def bar_chart(pie_chart7):
    # db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
    # db.make_connection()

    date = DailyPredictions.objects.only('date')
    date_list = []
    for d in date:
        date_list.append(d.date)

    # print(f'date-------------{date_list}')

    avg_stress = DailyPredictions.objects.only('average_stress_percentage')
    avg_list = []
    for al in avg_stress:
        avg_list.append(al.average_stress_percentage)

    # db.close_connection()

    data = np.array([date_list, avg_list])
    # data = np.transpose(data)
    data = {'date': data[0], 'average stress': data[1]}

    df = pd.DataFrame(data)
    # print('----------------------------------------------------------------------------------------------------------')
    # print(df)

    fig = px.bar(df, x='date', y='average stress')

    return fig


@dashboard.callback(Output("pie_chart1", 'figure'),
                    Input('update_alert', 'children'))
def pie_current(update_alert):
    date = '2022-03-05'
    # db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
    # db.make_connection()

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    # db.close_connection()

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

    # data = {'emotion':daily_percentages_list[0][0], 'percentage':[daily_percentages_list[0][1], 100.0-daily_percentages_list[0][1]]}

    df = pd.DataFrame(data)
    fig1 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig1.update_traces(textfont_size=1,
                      marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig1.update_layout(title_text=data['Emotion'][0],
                      margin=dict(l=10, r=10, t=35, b=10),
                      annotations=[dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                      )
    return fig1


@dashboard.callback(Output("pie_chart2", 'figure'),
                    Input('pie_chart1', 'figure'))
def pie_current(pie_chart1):
    date = '2022-03-05'
    # db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
    # db.make_connection()

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    # db.close_connection()

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

    # data = {'emotion':daily_percentages_list[0][0], 'percentage':[daily_percentages_list[0][1], 100.0-daily_percentages_list[0][1]]}

    df = pd.DataFrame(data)
    fig2 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig2.update_traces(textfont_size=1,
                      marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig2.update_layout(title_text=data['Emotion'][0],
                      margin=dict(l=10, r=10, t=35, b=10),
                      annotations=[dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                      )
    return fig2


@dashboard.callback(Output("pie_chart3", 'figure'),
                    Input('pie_chart2', 'figure'))
def pie_current(pie_chart2):
    date = '2022-03-05'
    # db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
    # db.make_connection()

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    # db.close_connection()

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

    # data = {'emotion':daily_percentages_list[0][0], 'percentage':[daily_percentages_list[0][1], 100.0-daily_percentages_list[0][1]]}

    df = pd.DataFrame(data)
    fig3 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig3.update_traces(textfont_size=1,
                      marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig3.update_layout(title_text=data['Emotion'][0],
                      margin=dict(l=10, r=10, t=35, b=10),
                      annotations=[dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                      )
    return fig3


@dashboard.callback(Output("pie_chart4", 'figure'),
                    Input('pie_chart3', 'figure'))
def pie_current(pie_chart3):
    date = '2022-03-05'
    # db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
    # db.make_connection()

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    # db.close_connection()

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

    # data = {'emotion':daily_percentages_list[0][0], 'percentage':[daily_percentages_list[0][1], 100.0-daily_percentages_list[0][1]]}

    df = pd.DataFrame(data)
    fig4 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig4.update_traces(textfont_size=1,
                      marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig4.update_layout(title_text=data['Emotion'][0],
                      margin=dict(l=10, r=10, t=35, b=10),
                      annotations=[dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                      )
    return fig4

@dashboard.callback(Output("pie_chart5", 'figure'),
                    Input('pie_chart4', 'figure'))
def pie_current(pie_chart4):
    date = '2022-03-05'
    # db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
    # db.make_connection()

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    # db.close_connection()

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

    # data = {'emotion':daily_percentages_list[0][0], 'percentage':[daily_percentages_list[0][1], 100.0-daily_percentages_list[0][1]]}

    df = pd.DataFrame(data)
    fig5 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig5.update_traces(textfont_size=1,
                      marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig5.update_layout(title_text=data['Emotion'][0],
                      margin=dict(l=10, r=10, t=35, b=10),
                      annotations=[dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                      )
    return fig5


@dashboard.callback(Output("pie_chart6", 'figure'),
                    Input('pie_chart5', 'figure'))
def pie_current(pie_chart5):
    date = '2022-03-05'
    # db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
    # db.make_connection()

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    # db.close_connection()

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

    # data = {'emotion':daily_percentages_list[0][0], 'percentage':[daily_percentages_list[0][1], 100.0-daily_percentages_list[0][1]]}

    df = pd.DataFrame(data)
    fig6 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig6.update_traces(textfont_size=1,
                      marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig6.update_layout(title_text=data['Emotion'][0],
                      margin=dict(l=10, r=10, t=35, b=10),
                      annotations=[dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                      )
    return fig6


@dashboard.callback(Output("pie_chart7", 'figure'),
                    Input('pie_chart6', 'figure'))
def pie_current(pie_chart6):
    date = '2022-03-05'
    # db = Database('daily-predictions', 'b1xvQn1CBeoBf2a6')
    # db.make_connection()

    daily_percentages = DailyPredictions.objects.only('all_emo_percentages', 'date')
    daily_percentages_list = []
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    for dp in daily_percentages:
        day_percentages = [dp.date, dp.all_emo_percentages]
        daily_percentages_list.append(day_percentages)

    # db.close_connection()

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

    # data = {'emotion':daily_percentages_list[0][0], 'percentage':[daily_percentages_list[0][1], 100.0-daily_percentages_list[0][1]]}

    df = pd.DataFrame(data)
    fig7 = px.pie(df, values='percentage', hover_name='Emotion', hole=0.6, width=120, height=120)

    fig7.update_traces(textfont_size=1,
                      marker=dict(colors=['#0000ee', '#ffffff'], line=dict(color='rgba(0,0,238,0.3)', width=2)))

    fig7.update_layout(title_text=data['Emotion'][0],
                      margin=dict(l=10, r=10, t=35, b=10),
                      annotations=[dict(text=f'{round(data["percentage"][0])}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
                      )
    return fig7


#-------------------------------------------------------------------------------------------------------------------------------------------------
# Tab2 callbacks



# running the dashboard app
if __name__ == '__main__':
    dashboard.run_server(debug=False)
