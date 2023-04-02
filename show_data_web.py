import dash
from dash import dcc, html
import plotly.graph_objs as go


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
