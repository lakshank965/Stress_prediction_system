import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

employees = ['emp001', 'emp002', 'emp003', 'emp004', 'emp005']

content = [
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H5('Employee ID : ', style={'display': 'flex', 'justify-content': 'flex-end'}),
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='search_emp_id',
                            options=[{'label': employee, 'value': employee}
                                     for employee in employees]
                        ),
                    ),
                ]
            ),

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
                                                dcc.Graph(id="pie_chart1e"),
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
                                                dcc.Graph(id="pie_chart2e"),
                                            ], style={"padding": "0px"}
                                        ),
                                    ],  # color="primary", inverse=True
                                )
                            ),

                            dbc.Col(
                                dbc.Card(
                                    [
                                        # dbc.CardHeader("Card header"),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(id="pie_chart3e"),
                                            ], style={"padding": "0px"}
                                        ),
                                    ],  # color="primary", inverse=True
                                )
                            ),

                            dbc.Col(
                                dbc.Card(
                                    [
                                        # dbc.CardHeader("Card header"),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(id="pie_chart4e"),
                                            ], style={"padding": "0px"}
                                        ),
                                    ],  # color="primary", inverse=True
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
                                                dcc.Graph(id="pie_chart5e"),
                                            ], style={"padding": "0px"}
                                        ),
                                    ],  # color="primary", inverse=True
                                )
                            ),

                            dbc.Col(
                                dbc.Card(
                                    [
                                        # dbc.CardHeader("Card header"),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(id="pie_chart6e"),
                                            ], style={"padding": "0px"}
                                        ),
                                    ],  # color="primary", inverse=True
                                )
                            ),

                            dbc.Col(
                                dbc.Card(
                                    [
                                        # dbc.CardHeader("Card header"),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(id="pie_chart7e"),
                                            ], style={"padding": "0px"}
                                        ),
                                    ],  # color="primary", inverse=True
                                )
                            ),
                        ], style={"display": "flex"}
                    ),

                    html.Br(),
                    html.H3("Employee's stress levels changing chart."),
                    # Row 2 start ----------------------------------------------------------
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    [
                                        # dbc.CardHeader("Card header"),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(id="line_graph_e"),
                                            ]
                                        ),
                                    ],  # color="primary", inverse=True
                                )
                            ),
                        ], className="mb-4",
                    ),  # Row 2 end --------------------------------------------------------
                ],
            )  # Div end

        ]
    )
]
