#DCDAT35 Midcourse Project
#Isaac Dorfman
#September 14, 2019
#Portions of code adapted from: https://towardsdatascience.com/a-gentle-invitation-to-interactive-visualization-with-dash-a200427ccce9

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go


# Step 0. Set up informational variables
sourceurl = 'https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016'
githublink = 'https://github.com/ihdorfman/DCDAT35midcourse'
tabtitle = 'Global Mental Health'

# Step 1. Launch the application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

# Step 2. Import the dataset
df1 = pd.read_csv('data/master.csv')
df1.rename(columns={'suicides/100k pop':'per100'}, inplace=True)
df1['country'].replace('Russian Federation','Russia', inplace=True)


df4 = df1[['country','year','per100']]

df5 = df4.groupby(['country','year']).agg(sum).reset_index()


# year slider options
YEARS = [1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, \
            1994, 1995, 1996, 1997, 1998, 1999,2000, 2001, 2002,\
            2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, \
            2012, 2013, 2014, 2015, 2016]


# Step 3. Create a plotly figure
trace_1 = go.Choropleth(
            locations=df5[df5['year']==1985]['country'], # Spatial coordinates
            z = df5[df5['year']==1985]['per100'].astype(float), # Data to be color-coded
            locationmode = 'country names', # set of locations match entries in `locations`
            colorscale = 'Blues',
            colorbar_title = 'Suicides per 100K')

fig = go.Figure(data = [trace_1])

fig.update_layout(
    geo_scope='world',
    width=1200,
    height=800
)


# Step 4. Create a Dash layout
app.layout = html.Div([
                # a header and a paragraph
                html.Div([
                    html.H4('Suicide Rate by Country per 100K Residents 1985-2016'),
                    html.P("Isaac Dorfman - DCDAT35 Midcourse Project")
                         ],
                     style = {'padding' : '15px' ,
                              'backgroundColor' : '#8DA1A0', 'width':1050}),
                # range slider
                html.P([
                    html.Label("Year:"),
                    dcc.Slider(id='slider',
					               min=min(YEARS),
                                   max=max(YEARS),
                                   value=min(YEARS),
                                   marks={str(year): str(year) for year in YEARS},),
			            ], style={'width':1000, 'margin':25}),

                # adding a plot
                dcc.Graph(id = 'plot', figure = fig),


                    html.A('Code on Github', href=githublink),
                    html.Br(),
                    html.A("Data Source", href=sourceurl)


                      ])


# Step 5. Add callback functions
@app.callback(Output('plot', 'figure'),
             [Input('slider', 'value')])
def update_figure(input):

    # updating the plot
    trace_1 = go.Choropleth(
                locations=df5[df5['year']==input]['country'], # Spatial coordinates
                z = df5[df5['year']==input]['per100'].astype(float), # Data to be color-coded
                locationmode = 'country names', # set of locations match entries in `locations`
                colorscale = 'Blues',
                colorbar_title = 'Suicides per 100K')

    fig = go.Figure(data = [trace_1])

    fig.update_layout(
        geo_scope='world',
        width=1200,
        height=800
    )
    return fig

# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug = True)
