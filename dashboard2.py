from pickle import TRUE
from dash import Dash
import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]



df = pd.read_csv("data/final_list.csv")

df.rename(columns={"Unnamed: 0": "Index", ""}, inplace = TRUE)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        #header part
        html.Img(src=("/assets/Logo.png")),
        html.H1(children="Start Up List",className="header-title",),
        html.P(children="Last scrape was the 12.12.12",className="header-description",),
        
        #data part
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            )
    ], className="wrapper",
)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)