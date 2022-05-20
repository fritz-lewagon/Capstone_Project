from pickle import TRUE
from dash import Dash
from dash.dependencies import Output, Input
import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns



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
df = df.fillna("No Information")




# dash starts here
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)




app.layout = html.Div([
    
        #header part
        html.Div([
            html.Img(src=("/assets/Logo.png")),
            html.H1(children="Start Up List"),
            html.P(children="Last scrape was the 12.12.12"),
        ], 
        id = "header-container"),


         # interactive part
        html.Div([
            
            html.Div([
                
                html.Div([
                    html.Label("Year", className='dropdown-labels'),
                    dcc.Dropdown(
                    options=[{"label": x, "value": x} for x in df["Year Founded"].unique()],
                    multi=True,
                    ),
                ], id = "drop-down-year",
                ),

                html.Div([
                    html.Label("Stage", className='dropdown-labels'),
                    dcc.Dropdown(
                    options=[{"label": x, "value": x} for x in df["Stage"].unique()],
                    multi=True,
                    ),
                ], id = "drop-down-stage",
                ),
        ],id = "drop-downs"
        ),



            # @Miron --> start working here
            html.Button("Update", id='update-button'),
        ], 
        id = "interactive-container"),


        #data part
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=20,
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_cell={
                    'textAlign': 'left', 
                    'padding': '5px'},
                style_header={
                    'fontWeight': 'bold'
                    },
                style_table={
                    'maxWidth': '1300px',
                    'maxHeight' : '500px',
                    'overflowY': 'scroll'
                    },
                ),
                
            ], 
            id = "data-container"),

        ], id='container'
    
)



### Callbacks to make the app interactive





if __name__ == '__main__':
    app.run_server(debug=True)