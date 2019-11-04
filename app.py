import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
import pandas as pd

# Read in the USA counties shape files
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

########### Define a few variables ######

tabtitle = 'PR Deployment'
sourceurl = 'https://plot.ly/python/scattermapbox/'
githublink = 'https://github.com/regina-avila/pr-deployment-map-ra'
mapbox_access_token = open("assets/mytoken.mapbox_token").read()
df = pd.read_csv('resources/hm_deploy_201808.csv', index_col='Unnamed: 0')
#makes for a quicker run with fewer Properties
varlist=[20180823, 20180824, 20180825]

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########## Figure
#this is a density mapbox. mapbox is a company that specializes in providing underlying maps for other startups to use in mapbuilding
#plotly reached out for built-in mapbox functions. lots of go.mapbox functions available. will require lattitude and LONGITUDE
#NOw turn this into a function
def myfunc(some_value):
    fig = go.Figure(go.Scattermapbox(
        lat=df['latitude'],
        lon=df['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            colorscale='grays',
            color=df[value]
        ),
        text=df['date']

        ),
    )
    return fig

app.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
#must register for an access token on the mapbox website. this has to be saved. this one is in resources folder
#mytoken.mapbox_access_token
#gitignore - use this to ignore the filename with your token to hide it on github
        accesstoken=mapbox_access_token,
        bearing=0,
#this centers on PR !
        center=go.layout.mapbox.Center(
            lat=18.146,
            lon=-66.235
        ),
        pitch=0,
        zoom=10
    ),
)



########### Layout

app.layout = html.Div(children=[
    html.H1('Puerto Rico Deployment Map'),
    # Dropdowns
    html.Div(children=[
        # left side
        html.Div([
                html.H6('Select a photo shoot date'),
                dcc.Dropdown(
                    id='dates-drop',
                    #options=[{'label': i, 'value': i} for i in varlist],
                    value='date'
                ),
        ], className='three columns'),
        # right side
        html.Div([
            dcc.Graph(id='pr-map', figure=fig)
        ], className='nine columns'),
    ], className='twelve columns'),

    # Footer
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Callbacks
@app.callback(Output('pr-map', 'figure'),
             [Input('dates-drop', 'value')])
def generate_map(dropdown_chosen_value):
    return make_my_cool_figure(dropdown_chosen_value)


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
