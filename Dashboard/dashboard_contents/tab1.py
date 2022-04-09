import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.express as px

from Operations import Database, Predictions



# tab1 content design
content = [
    html.Br(),
    html.Div(
        [
            html.H3('Current predicted emotions percentages'),
            html.Br(),
            # Row 1 start----------------------------------------------------------
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                # dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(id="pie_chart1"),
                                    ], style={"padding": "0px"}
                                ),
                            ],
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                # dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(id="pie_chart2"),
                                    ], style={"padding": "0px"}
                                ),
                            ],#color="primary", inverse=True
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                # dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(id="pie_chart3"),
                                    ], style={"padding": "0px"}
                                ),
                            ], #color="primary", inverse=True
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                # dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(id="pie_chart4"),
                                    ], style={"padding": "0px"}
                                ),
                            ], #color="primary", inverse=True
                        )
                    ),


                # ], className="mb-4",
            # ),  # Row 1 end --------------------------------------------------------

            # dbc.Row(
            #     [
                    dbc.Col(
                        dbc.Card(
                            [
                                # dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(id="pie_chart5"),
                                    ], style={"padding": "0px"}
                                ),
                            ], #color="primary", inverse=True
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                # dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(id="pie_chart6"),
                                    ], style={"padding": "0px"}
                                ),
                            ], #color="primary", inverse=True
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                # dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(id="pie_chart7"),
                                    ], style={"padding": "0px"}
                                ),
                            ], #color="primary", inverse=True
                        )
                    ),
                ],  style={"display": "flex"}
            ),

            html.Br(),
            html.H3("All employees' average stress levels changing chart."),
            # Row 2 start ----------------------------------------------------------
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                # dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(id="line_graph"),
                                    ]
                                ),
                            ], #color="primary", inverse=True
                        )
                    ),
                ], className="mb-4",
            ),  # Row 2 end --------------------------------------------------------
        ],
    )  # Div end
]  # content end
