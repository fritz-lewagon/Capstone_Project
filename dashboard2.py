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


#import data frame
df = pd.read_csv("data/final_list.csv")


# data cleaning - renaming
df.rename(columns={"Unnamed: 0": "Index", "comp_name": "Company", "description": "Description",
"business_model": "Business Model", "customer": "Target Customer", "keywords": "Keywords",
"stage": "Stage", "total_funding": "Total Funding (in M€)", "num_investors": "Number of Investors",
"date_founded": "Year Founded", "location": "Location", "employees": "Employees", "website": "website"}, 
inplace = TRUE)


# dash starts here
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        #header part
        html.Img(src=("/assets/Logo.png"),className="logo-title"),
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