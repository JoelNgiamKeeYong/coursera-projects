import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
data = pd.read_csv(url)

# Initialize the Dash app
app = dash.Dash(__name__)

# Dropdown options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024, 1)]

# Layout
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard"),
    
    html.Label("Select Statistics:"),
    dcc.Dropdown(
        id='dropdown-statistics',
        options=dropdown_options,
        placeholder='Select a report type',
        style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
    ),
    
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select-year',
        style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
    )),
    
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
])

# Callback to enable/disable year selection
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

# Callback for generating plots
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_stat, selected_year):
    if selected_stat == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales During Recession")
        )
        
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Sales by Vehicle Type")
        )
        
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Advertisement Expenditure by Vehicle Type during Recessions"
            )
        )
        
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'Unemployment_Rate': 'Unemployment Rate', 'Automobile_Sales': 'Avg Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type Sales')
        )
        
        return [
            # First row: Charts 1 and 2
            html.Div(
                className='chart-item',
                children=[
                    html.Div(children=R_chart1, style={'flex': 1, 'margin': '10px'}),  # Ensure each chart takes equal space
                    html.Div(children=R_chart2, style={'flex': 1, 'margin': '10px'})
                ],
                style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'}
            ),
            
            # Second row: Charts 3 and 4
            html.Div(
                className='chart-item',
                children=[
                    html.Div(children=R_chart3, style={'flex': 1, 'margin': '10px'}),  # Ensure each chart takes equal space
                    html.Div(children=R_chart4, style={'flex': 1, 'margin': '10px'})
                ],
                style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between', 'margin-top': '20px'}
            )
        ]
    
    elif selected_stat == 'Yearly Statistics' and selected_year:
        yearly_data = data[data['Year'] == selected_year]
        
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales")
        )
        
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales')
        )
        
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title=f'Avg Vehicles Sold in {selected_year}')
        )
        
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Advertisement Expenditure')
        )
        
        return [
            # First row: Charts 1 and 2
            html.Div(
                className='chart-item',
                children=[
                    html.Div(children=Y_chart1, style={'flex': 1, 'margin': '10px'}),  # Ensure each chart takes equal space
                    html.Div(children=Y_chart2, style={'flex': 1, 'margin': '10px'})
                ],
                style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'}
            ),
            
            # Second row: Charts 3 and 4
            html.Div(
                className='chart-item',
                children=[
                    html.Div(children=Y_chart3, style={'flex': 1, 'margin': '10px'}),  # Ensure each chart takes equal space
                    html.Div(children=Y_chart4, style={'flex': 1, 'margin': '10px'})
                ],
                style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between', 'margin-top': '20px'}
            )
        ]
    
    return None

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
