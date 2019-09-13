#DCDAT35 Midcourse Project
#Isaac Dorfman
#September 7, 2019

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os
from pathlib import Path

#import and prepare the data for mapping
home = Path.cwd()

filepath = Path.joinpath(home, 'data', 'master.csv')
df1 = pd.read_csv(filepath)
df1.rename(columns={'suicides/100k pop':'per100'}, inplace=True)
df1['country'].replace('Russian Federation','Russia', inplace=True)

filepath2 = Path.joinpath(home, 'data', 'd3-world-map.csv')
df2 = pd.read_csv(filepath2)
df2.drop(columns='z', inplace=True)
df2.rename(columns={'text':'country'}, inplace=True)

df3 = pd.merge(df1, df2, on='country')

df4 = df3[['country','year','per100','locations']]

df5 = df4.groupby(['country','locations','year']).agg(sum).reset_index()

#Set up for information about ther data set used and github repository
mygraphtitle = 'Suicide Rates by Country by Year'
mycolorscale = 'plasma' # Note: The error message will list possible color scales.
mycolorbartitle = "Suicides per 100k"
tabtitle = 'Global Mental Health'
sourceurl = 'https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016'
githublink = 'https://github.com/ihdorfman/DCDAT35midcourse'


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


#MAIN APP GUTS GO HERE!!!!









############ Deploy
if __name__ == '__main__':
    app.run_server()
