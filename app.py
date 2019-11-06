import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd


########### Variables ######

tabtitle = 'PR Deployment'
sourceurl = 'https://plot.ly/python/scattermapbox/'
githublink = 'https://github.com/regina-avila/pr-deployment-map-ra'
mapbox_access_token = open("assets/mytoken.mapbox_token").read()
df = pd.read_csv('resources/hm_deploy_201808.csv', index_col='Unnamed: 0')

#this is the list of dates to select for map plot points
datelist=list(df['date'].value_counts().index)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########## Figure
#this function creates the mapbox using scattermapbox --
# see 'https://plot.ly/python/scattermapbox/'

def getPlots(value):
    df2 = df[df['date']==value]
    fig = go.Figure(go.Scattermapbox(
        lat=df2['latitude'],
        lon=df2['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,

        ),
#This pulls in the hover text for each plot point
        text=df['filename']

        ))
    fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox=go.layout.Mapbox(
                accesstoken=mapbox_access_token,
                bearing=0,
        #this centers on Puerto Rico where photos were shot
                center=go.layout.mapbox.Center(
                    lat=18.185,
                    lon=-66.162
                ),
                pitch=0,
                zoom=8
            ),
        )
    return fig


########### Layout

app.layout = html.Div(children=[
    html.H1('Puerto Rico Deployment Map'),
    # dropdown layout
    html.Div(children=[
        # left side
        html.Div([
                html.H6('Select a photo shoot date'),
                dcc.Dropdown(
                    id='dates-drop',
                    options=[{'label': i, 'value': i} for i in datelist],
                    #value=datelist[0]
                ),
        ], className='three columns'),
        #right side
        html.Div([
            dcc.Graph(id='pr-map')
        ], className='nine columns'),
    ], className='twelve columns'),

    # Footer
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

# ############ Callbacks
#
@app.callback(Output('pr-map', 'figure'),
             [Input('dates-drop', 'value')])
def generate_map(dropdown_chosen_value):
    return getPlots(dropdown_chosen_value)


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
