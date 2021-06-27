import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import dash_table as dt
import pandas as pd
from dash.dependencies import Input, Output

from MongoConnector import MongoConnector as client


# use the test db if available if no parameters are passed
def app_start(username='', password=''):
    #########################################
    # Data Manipulation / Model #######
    ###############################

    # Ensure to update the above fields before executing this next line.
    cl = client(_user=username, _pass=password, _dbname='AAC', _cl='animals')

    #  Filter columns that may not be as useful
    keep = ['animal_id', 'age_upon_outcome', 'animal_type', 'breed', 'color', 'date_of_birth', 'name',
            'outcome_subtype', 'outcome_type', 'sex_upon_outcome', 'location_lat',
            'location_long', 'age_upon_outcome_in_weeks']

    #  Create dataframe containing all records from the database
    df = pd.DataFrame.from_records(cl.retrieveAllDocs())  # read all from db

    assert (len(df) == 10000)  # assert connection was successful and dataframe contains 10,000 documents

    df = df[keep] # filter out the columns we dont need. 
    dff = df      # assign dff ahead of time

    cl.client.close()  # close the connection, all data is in the pandas dataframe.

    ########################################
    # Dashboard Layout / View #######
    ###############################

    # relative pathing!
    logo = base64.b64encode(open('../images/logo.png', 'rb').read()).decode()

    # app title
    app = dash.Dash('Grazioso Salvare', meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
    app.layout = html.Div(children=[
        html.Center(html.Img(
            alt='missing', src='data:image/png;base64,{0}'.format(logo), width=400, height=400)),
        html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
        html.Center(html.B(html.H4('Student: Andy Place'))),
        html.Hr(),
        html.Div(
            # not functional, disabled by default
            dcc.Dropdown(id='filter-type',
                         options=[
                             {'label': 'Dog', 'value': 'Dog'},
                             {'label': 'Cat', 'value': 'Cat'},
                             {'label': 'Other', 'value': 'Other'}
                         ], disabled=True)),
        html.Hr(),
        dt.DataTable(id='table_id', data=dff.to_dict('records'),
                     columns=[{"name": i, "id": i, "deletable": False,
                               "selectable": True} for i in df],
                     editable=False,
                     filter_action="native",
                     sort_action="native",
                     sort_mode="multi",
                     column_selectable=False,
                     row_selectable=False,
                     row_deletable=False,
                     selected_columns=[],
                     selected_rows=[],
                     page_action="native",
                     page_current=0,
                     page_size=10,
                     style_as_list_view=False,
                     fill_width=True),
        html.Br(),
        html.Hr(), html.Div(className='row', style={'display': 'flex'}, children=[
            html.Div(id='graph_id', className='col s12 m6'),
            html.Div(id='map_id', className='col s12 m6', ),
        ]),
    ])

    ############################################################
    # Interaction Between Components / Controller #######
    #################################################
    # ^ Simplified: callbacks for html.

    #  Table row/column styling on select
    @app.callback(Output('table_id', 'style_data_conditional'), [Input('table_id', 'selected_columns')])
    def update_styles(selected_columns):
        return [{
            'if': {'column_id': i},
            'background_color': 'rgb(210, 243, 255)'
        } for i in selected_columns]

    @app.callback([Output('table_id', 'data'), Output('table_id', 'columns')], [Input('table_id', 'selected_columns')])
    def update_dashboard(viewData):
        columns = [{"name": i, "id": i, "deletable": False,
                    "selectable": True} for i in df.columns]
        data = df.to_dict('records')
        return data, columns

    # Graph Callback and function, (NOT FULLY IMPLEMENTED)
    @app.callback(Output('graph_id', "children"), [Input('table_id', "derived_viewport_data")])
    def update_graphs(viewData):
        return [dcc.Graph(figure={
            # not functional
        })]

    # Geolocation chart
    @app.callback(Output('map_id', "children"), [Input('table_id', "derived_viewport_data")])
    def update_map(view_data):
        # if the user deliberately messes up the table, it's on the client's side... at least...
        m_lat = view_data[0]['location_lat']
        m_long = view_data[0]['location_long']

        if view_data is not None:
            return [dl.Map(style={'width': '600px', 'height': '500px'}, center=[m_lat, m_long], zoom=8,
                           children=[
                           dl.TileLayer(id="derived_viewport_data"),
                           dl.Marker(position=[m_lat, m_long],
                                     children=[
                               dl.Tooltip(df.iloc[2, 6]),
                               dl.Popup([html.H1("Location"), html.P(df.iloc[2, 6])])])
                           ])]

    # run the app
    app.run_server(debug=True, port=27015)

# Fill in these fileds 
if __name__ == '__main__':
    db_username = ""
    db_password = ""
    app_start(db_username, db_password)
