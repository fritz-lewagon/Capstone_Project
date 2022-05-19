from pickle import TRUE
from dash import Dash
from dash.dependencies import Output, Input
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


# dash has problems with NAs, therefore they are filled with a string
df["Year Founded"] = df["Year Founded"].fillna("No Information")


# dash starts here
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)




app.layout = html.Div([
    
        #header part
        html.Div([
            html.Img(src=("/assets/Logo.png"),className="logo-title"),
            html.H1(children="Start Up List",className="header-title",),
            html.P(children="Last scrape was the 12.12.12",className="header-description",),
        ], id = "header-part"),

        html.Br(),

         # dropdown
        html.Div([
            dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in df["Year Founded"].unique()],
            multi=True,
            ),
        ], id = "dropdown-part"),

        html.Br(),

        #data part
        html.Div([
            dash_table.DataTable(
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    },
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=20,
                style_cell={
                    'textAlign': 'left', 
                    'padding': '5px'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                    },
                style_table={
                    'maxWidth': '1300px',
                    'overflowY' : 'scroll',}
                ),
            ], id = "data-part")
        ], id='container'
    
)



if __name__ == '__main__':
    app.run_server(debug=True)