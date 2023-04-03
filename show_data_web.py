import dash
from dash import dcc, html
import plotly.graph_objs as go

"""
The function show_data() takes two dictionaries as inputs: algorithms and heuristics, and uses them to create a dashboard using the Dash framework. 
The dashboard displays the results of running various search algorithms and heuristics on different levels of a game.

The algorithms dictionary has keys for different levels of the game and values that are themselves dictionaries. 
These sub-dictionaries have keys for different measures (such as "time" or "nodes") and values that are dictionaries mapping algorithm names to the corresponding measure value.

The heuristics dictionary has similar structure, but with keys for different levels, measures, and algorithms, and values that are dictionaries mapping heuristic names to the corresponding measure value.

The function creates a separate bar chart for each level and measure in the algorithms dictionary, and a separate bar chart for each level, measure, and algorithm in the heuristics dictionary. 
The x-axis of each chart shows the algorithms or heuristics being compared, and the y-axis shows the corresponding measure value.

The function returns the constructed dashboard as a Dash object.
"""
def show_data(algorithms, heuristics):
    app = dash.Dash()

    graphs = []

    for level, measures in algorithms.items():
        for measure, algos in measures.items():
            a = []
            v = []
            for algo, value in algos.items():
                a.append(algo)
                v.append(value)

            g = dcc.Graph(
                id=level + '-' + measure,
                figure={
                    'data': [
                        go.Bar(
                            x=a,
                            y=v,
                            name=measure + ' on level ' + level
                        )
                    ],
                    'layout': go.Layout(
                        title=measure + ' on level ' + level,
                        xaxis={'title': 'Algorithms'},
                        yaxis={'title': measure}
                    )
                }
            )

            graphs.append(g)

    for level, measures in heuristics.items():
        for measure, algos in measures.items():
            for algo, heuristics in algos.items():
                h = []
                v = []
                for heuristic, value in heuristics.items():
                    h.append(heuristic)
                    v.append(value)

                g = dcc.Graph(
                    id=algo + '-' + level + '-' + measure,
                    figure={
                        'data': [
                            go.Bar(
                                x=h,
                                y=v,
                                name=measure + ' on level ' + level + ' for ' + algo
                            )
                        ],
                        'layout': go.Layout(
                            title=measure + ' on level ' + level + ' for ' + algo,
                            xaxis={'title': 'Heuristics'},
                            yaxis={'title': measure}
                        )
                    }
                )

                graphs.append(g)

    app.layout = html.Div(children=[html.H1(children='AI Search Algorithms')] + graphs)
    return app
