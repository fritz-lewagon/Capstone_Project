import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv("data/startup_list.csv")

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Start Up List",className="header-title",),
        html.P(children="Last scrape was th 12.12.12",className="header-description",),
        
        
        
        dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
)])

if __name__ == '__main__':
        app.run_server(debug=True, use_reloader=False)