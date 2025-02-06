# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create a dash application
app = dash.Dash(__name__)

# Get unique launch sites
launch_sites = spacex_df['Launch Site'].unique()

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown for selecting launch site
    html.Label('Launch Site:'),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',
        placeholder="Select a launch site",
        searchable=True
    ),
    
    # Pie chart for success/failure
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    # Payload range slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=spacex_df['Payload Mass (kg)'].min(),
        max=spacex_df['Payload Mass (kg)'].max(),
        step=100,
        marks={i: str(i) for i in range(int(spacex_df['Payload Mass (kg)'].min()), 
                                      int(spacex_df['Payload Mass (kg)'].max()) + 1, 1000)},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),
    
    # Scatter plot for payload vs success
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2: Callback function for Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Show success vs failure for all sites
        pie_data = spacex_df.groupby('class').size().reset_index(name='count')
        fig = px.pie(pie_data, names='class', values='count', title='Total Success vs Failure')
    else:
        # Filter data for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        pie_data = site_data.groupby('class').size().reset_index(name='count')
        fig = px.pie(pie_data, names='class', values='count', title=f'Success vs Failure for {selected_site}')
    
    return fig

# TASK 4: Callback function for Scatter Chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter by selected launch site
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    # Create scatter plot
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     title=f'Success vs Payload for {selected_site if selected_site != "ALL" else "All Sites"}',
                     labels={'class': 'Launch Success (1=Success, 0=Failure)', 
                             'Payload Mass (kg)': 'Payload Mass (kg)'})
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
