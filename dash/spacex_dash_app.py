# Plotly Dash dashboard for SpaceX launch records (IBM Data Science Capstone, Module 3)
# Run: python spacex_dash_app.py  → open http://127.0.0.1:8050
import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Optional start values (used only to take screenshots of a selected site / payload range)
START_SITE = os.environ.get('START_SITE', 'ALL')

app = dash.Dash(__name__)
sites = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': s, 'value': s} for s in sorted(spacex_df['Launch Site'].unique())]

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 1: launch site dropdown
    dcc.Dropdown(id='site-dropdown', options=sites, value=START_SITE,
                 placeholder='Select a Launch Site here', searchable=True),
    html.Br(),
    # TASK 2: success pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P('Payload range (Kg):'),
    # TASK 3: payload range slider
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 2500)},
                    value=[min_payload, max_payload]),
    # TASK 4: payload vs success scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# TASK 2 callback: pie chart for all sites or a selected site
@app.callback(Output('success-pie-chart', 'figure'), Input('site-dropdown', 'value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        df = spacex_df[spacex_df['class'] == 1]
        return px.pie(df, names='Launch Site', title='Total Successful Launches by Site')
    df = spacex_df[spacex_df['Launch Site'] == entered_site]
    counts = df['class'].value_counts().rename({1: 'Success', 0: 'Failure'}).reset_index()
    counts.columns = ['Outcome', 'Count']
    return px.pie(counts, values='Count', names='Outcome', title=f'Success vs Failure for site {entered_site}')


# TASK 4 callback: scatter chart filtered by site and payload range
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site != 'ALL':
        df = df[df['Launch Site'] == entered_site]
    title = 'Correlation between Payload and Success for ' + ('all Sites' if entered_site == 'ALL' else entered_site)
    return px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=title)


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8050)))
