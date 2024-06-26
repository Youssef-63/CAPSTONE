# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=int(min_payload),
                                                max=int(max_payload),
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                marks={i: str(i) for i in range(int(min_payload), int(max_payload)+1, 10000)}),

                                # Display selected payload range
                                html.Div(id='payload-range-output'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart', 'figure'),
              [Input('site-dropdown', 'value')])
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        rslt = spacex_df['class'].value_counts().reset_index()
        fig = px.pie(rslt, values='count', names='class', title='Total Success Launches for All Sites')
    else:
        selected_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(selected_data, names='class', title=f'Success Launches for {selected_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    if selected_site == 'ALL':
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        selected_data = filtered_data[filtered_data['Launch Site'] == selected_site]
        fig = px.scatter(selected_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload vs. Outcome for {selected_site}')
    return fig

# Display selected payload range
@app.callback(Output('payload-range-output', 'children'),
              [Input('payload-slider', 'value')])
def display_payload_range(payload_range):
    return f"Selected Payload Range: {payload_range[0]} kg to {payload_range[1]} kg"

# Run the app
if __name__ == '__main__':
    app.run_server()



# # Import required libraries
# import pandas as pd
# import dash
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output
# import plotly.express as px

# # Read the airline data into pandas dataframe
# spacex_df = pd.read_csv("spacex_launch_dash.csv")
# max_payload = spacex_df['Payload Mass (kg)'].max()
# min_payload = spacex_df['Payload Mass (kg)'].min()

# # Create a dash application
# app = dash.Dash(__name__)

# # Create an app layout
# app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
#                                         style={'textAlign': 'center', 'color': '#503D36',
#                                                'font-size': 40}),
#                                 # TASK 1: Add a dropdown list to enable Launch Site selection
#                                 # The default select value is for ALL sites
#                                 dcc.Dropdown(id='site-dropdown',
#                                              options=[{'label': 'All Sites', 'value': 'ALL'},
#                                                       {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
#                                                       {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
#                                                       {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
#                                                       {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
#                                              value='ALL',
#                                              placeholder="Select a Launch Site here",
#                                              searchable=True),
#                                 html.Br(),

#                                 # TASK 2: Add a pie chart to show the total successful launches count for all sites
#                                 # If a specific launch site was selected, show the Success vs. Failed counts for the site
#                                 html.Div(dcc.Graph(id='success-pie-chart')),
#                                 html.Br(),

#                                 html.P("Payload range (Kg):"),
#                                 # TASK 3: Add a slider to select payload range
#                                 dcc.RangeSlider(id='payload-slider',
#                                                 min=int(min_payload),
#                                                 max=int(max_payload),
#                                                 step=1000,
#                                                 value=[min_payload, max_payload],
#                                                 marks={i: str(i) for i in range(int(min_payload), int(max_payload)+1, 10000)}),

#                                 # TASK 4: Add a scatter chart to show the correlation between payload and launch success
#                                 html.Div(dcc.Graph(id='success-payload-scatter-chart')),
#                                 ])

# # TASK 2:
# # Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# @app.callback(Output('success-pie-chart', 'figure'),
#               [Input('site-dropdown', 'value')])
# def update_pie_chart(selected_site):
#     if selected_site == 'ALL':
#         fig = px.pie(spacex_df, values='class', names='class', title='Total Success Launches for All Sites')
#     else:
#         selected_data = spacex_df[spacex_df['Launch Site'] == selected_site]
#         fig = px.pie(selected_data, names='class', title=f'Success Launches for {selected_site}')
#     return fig

# # TASK 4:
# # Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# @app.callback(Output('success-payload-scatter-chart', 'figure'),
#               [Input('site-dropdown', 'value'),
#                Input('payload-slider', 'value')])
# def update_scatter_chart(selected_site, payload_range):
#     low, high = payload_range
#     filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
#     if selected_site == 'ALL':
#         fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
#                          title='Payload vs. Outcome for All Sites')
#     else:
#         selected_data = filtered_data[filtered_data['Launch Site'] == selected_site]
#         fig = px.scatter(selected_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
#                          title=f'Payload vs. Outcome for {selected_site}')
#     return fig

# # Run the app
# if __name__ == '__main__':
#     app.run_server()
