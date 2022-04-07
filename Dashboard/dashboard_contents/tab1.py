import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.express as px

from Operations import Database, Predictions



# tab1 content design
content = [
    html.Div(
        [
            # Row 1 start----------------------------------------------------------
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        html.H5("Card title", className="card-title"),
                                        html.P(
                                            "This is some card content that we'll reuse",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ], color="primary", inverse=True
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        html.H5("Card title", className="card-title"),
                                        html.P(
                                            "This is some card content that we'll reuse",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ], color="primary", inverse=True
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        html.H5("Card title", className="card-title"),
                                        html.P(
                                            "This is some card content that we'll reuse",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ], color="primary", inverse=True
                        )
                    ),
                ], className="mb-4",
            ),  # Row 1 end --------------------------------------------------------

            # Row 2 start ----------------------------------------------------------
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Card header"),
                                dbc.CardBody(
                                    [
                                        dcc.Graph(id="line_graph"),
                                    ]
                                ),
                            ], color="primary", inverse=True
                        )
                    ),
                ], className="mb-4",
            ),  # Row 2 end --------------------------------------------------------
        ],
    )  # Div end
]  # content end
