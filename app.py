import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
import pandas as pd

# Read in the USA counties shape files
#from urllib.request import urlopen
#import json
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)

########### Define a few variables ######

tabtitle = 'DC Properties'
sourceurl = 'https://plot.ly/python/scattermapbox/'
githublink = 'https://github.com/austinlasseter/dc-properties-map'
mapbox_access_token = open("assets/mytoken.mapbox_token").read()
df = pd.read_csv('resources/DC_Properties.csv', index_col='Unnamed: 0')
#makes for a quicker run with fewer Properties
df = df.sample(500)
varlist=['BATHRM', 'HF_BATHRM', 'ROOMS', 'BEDRM', 'STORIES',  'PRICE']

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
    passig = go.Figure(go.Scattermapbox(
        lat=df['LATITUDE'],
        lon=df['LONGITUDE'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            colorscale='grays',
            color=df[value]
        ),
        text=df['ASSESSMENT_SUBNBHD']

    ))
return fig


fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
#must register for an access token on the mapbox website. this has to be saved. this one is in resources folder
#mytoken.mapbox_access_token
#gitignore - use this to ignore the filename with your token to hide it on github
        accesstoken=mapbox_access_token,
        bearing=0,
#this centers on DC !
        center=go.layout.mapbox.Center(
            lat=38.92,
            lon=-77.07
        ),
        pitch=0,
        zoom=10
    ),
)



########### Layout

app.layout = html.Div(children=[
    html.H1('DC Properties'),
    # Dropdowns
    html.Div(children=[
        # left side
        html.Div([
                html.H6('Select a variable for colorscale:'),
                dcc.Dropdown(
                    id='stats-drop',
                    options=[{'label': i, 'value': i} for i in varlist],
                    value='Price'
                ),
        ], className='three columns'),
        # right side
        html.Div([
            dcc.Graph(id='dc-map', figure=fig)
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
@app.callback(Output('dc-map', 'figure'),
             [Input('stats-drop', 'value')])
def generate_map(dropdown_chosen_value):
    return make_my_cool_figure(dropdown_chosen_value)


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
