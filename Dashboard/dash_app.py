import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dashboard_contents import tab1

dashboard = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) # dashboard app instantiation

# dashboard layout start ------------------------------------------------------------------------------------------------
dashboard.layout = dbc.Container(
    [
        html.H1('Hello, World!'),

        dbc.Tabs(
            [
                dbc.Tab(tab1.content, id='tab1', label='first tab', activeTabClassName='fw-bold'),
                dbc.Tab(tab1.content, id='tab2', label='Second tab', activeTabClassName='fw-bold'),
                dbc.Tab(tab1.content, id='tab3', label='third tab', activeTabClassName='fw-bold'),
            ]
        )
    ]
)




# dashboard layout end --------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

# callback functions ----------------------------------------------------------------------------------------------------
# @dashboard.callback()



# running the dashboard app
if __name__ == '__main__':
    dashboard.run_server(debug=True)

