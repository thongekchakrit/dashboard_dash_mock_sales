# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px 
import plotly.graph_objects as go

import pandas as pd
from sqlite3 import Error
import sqlite3
global master_df

# ################################################################################
'''
create connection with data warehouse
extract information of interest from data warehouse
'''

def create_connection():
    
    try:
        # create connection with data warehouse
        conn = sqlite3.connect(r'.\datasets\data_warehouse.db')
        return conn

    except Error as e:
        print(e)

def fetch_master_df(conn): 
    try:
        # create cursor to get data
        cursor = conn.cursor()

        # insert query into cursor
        cursor.execute('''
        SELECT * FROM MASTER_FILE
        ''')

        # convert query into dataframe
        return pd.DataFrame(cursor.fetchall(), columns=[i[0] for i in cursor.description])

    except Error as e:
        print(e)

# ################################################################################
# master file for satisfy visualization requirements

# create connection
conn = create_connection()

# get full data frame
master_df = fetch_master_df(conn)

# ------------------------------------------------------------------------------
# KPI and measures
def get_revenue(master_df):

    try:   
        return '$ {0:,.2f}K'.format((master_df['Sales'].sum()/1000))
        
    except Error as e:
        print(e)
        pass

def get_expenses(master_df):

    try: 
        return '$ {0:,.2f}K'.format((master_df['Cost'].sum()/1000))

    except Error as e:
        print(e)
        pass

def get_sales_quantity(master_df):
    try:
        return '{0:} Units'.format((master_df['Quantity'].sum()))
        
    except Error as e:
        print(e)
        pass

def get_discount(master_df):
    try:
        return '$ {0:,.2f}K'.format((master_df['Discount'].sum()/1000))
        
    except Error as e:
        print(e)
        pass

def get_profit(master_df):
    try:
        return '$ {0:,.2f}K'.format((master_df['Profit'].sum()/1000))
        
    except Error as e:
        print(e)
        pass

def get_sales_margin(master_df):
    try:
        return '{:,.2f}%'.format(((master_df['Profit'].sum())/(master_df['Sales'].sum()))*100)
        
    except Error as e:
        print(e)
        pass

# ------------------------------------------------------------------------------
# Scatter plot of Sales vs Profit by Category
requirement_iii = master_df[['Sales', 'Discount', 'Cost', 'Profit', 'ProductCategory']].groupby('ProductCategory').sum().reset_index()

viz_scatter_iii = px.scatter(requirement_iii, x="Sales", y="Profit", size="Profit", color="ProductCategory",
           hover_name="Profit", log_x=True, log_y=True, size_max=50, template="seaborn", title='SALES AGAINST PROFIT BY PRODUCT CATEGORY')

layout = viz_scatter_iii.update_layout(
            hoverlabel=dict(
                bgcolor="white", 
                font_size=16, 
                font_family="Open Sans"
            ),
            height=700,
            width=700,
            title={
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
                font=dict(
                size=16,
                color="#4a4a4a",
                ),paper_bgcolor="#f8f9fa")

viz_scatter_iii.update_traces(mode="markers", hovertemplate='Sales: %{x} <br>Profit: %{y}')

# ------------------------------------------------------------------------------
# Sales by City
# get sales from master file, aggregate on country 
city_sales = master_df[['Sales','Profit','Cost','Quantity','Discount','City']].groupby('City').sum()
lat_log_city = master_df[['City', 'Latitude', 'Longitude']].drop_duplicates().set_index('City')
requirement_ii = pd.concat([city_sales, lat_log_city], axis=1, join='inner').reset_index()
requirement_ii['Field'] = ' City' +'<br>' + requirement_ii['City'] + '<br>Sales ' + '$' + (requirement_ii['Sales'].round(2).astype(str))

mapbox_access_token = 'pk.eyJ1IjoiY2hha3JpdHRob25nZWsiLCJhIjoiY2tkdTAzd2hwMDBkZzJycWluMnFicXFhdCJ9.JjJhMoek5126u1B_kwYNiA'

px.set_mapbox_access_token(mapbox_access_token)

map_data = px.scatter_mapbox(requirement_ii, lat="Latitude", lon="Longitude", color="Sales", size="Sales",
                  color_continuous_scale=px.colors.cyclical.Edge, size_max=20, zoom=1,
                        center=dict(lon=-40.200033, lat=32.249974), 
                        hover_data={'City':False, 'Latitude':False, 'Longitude':False, 'Sales':False, 'Field':True}, title='SALES BY CITY', template="seaborn")

map_data.update_layout(
                hoverlabel=dict(
                    bgcolor="white", 
                    font_size=16, 
                    font_family="Open Sans"
                ),
                height=600,
                width=700,
                title={
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                size=16,
                color="#4a4a4a"),
                paper_bgcolor="#f8f9fa"
                    )

# --------------------------------------------------------------------------------
# Dash Table
data_table = master_df[['Year', 'Quarter', 'Country', 'City', 'CustomerName', 'ProfitType', 'ProductCategory', 'Sales', 'Profit', 'Cost']]

# ################################################################################
# initilize dash
# Bootstrap Javascript.

BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/litera/bootstrap.min.css"

app = dash.Dash(__name__, external_stylesheets=[BS])
server = app.server

app.title = 'Mock Company Dashboard'
# Define app layout

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                 html.H1(
                'Sales Department Data Analysis',
                style={
                    'fontSize':40,
                    'textAlign':'center',
                    'textDirection': 'vertical',
                    'dir':'rtl',
                    'padding': '20px',
                    'padding-top': '70px',
                    'color': '#41444b',
                    'margin-left':'auto',
                    'margin-right':'auto'
                    },                 
                        className='eight columns'),

                html.Img(
                    src="/assets/images/logo.png",
                    className='four columns',
                    style={
                        'height': '7%',
                        'width': '7%',
                        'float': 'left',
                        'position': 'relative',
                        'margin-top': 10,
                        'align':'center'
                    },
                ),
            ], className="row"
        ),

        dbc.Row([

            dbc.Col(html.Div(
                dbc.Alert("QUANTITY " + 
                    get_sales_quantity(master_df), color='light')), width=2),

                dbc.Col(html.Div(
                dbc.Alert("REVENUE " + 
                    get_revenue(master_df), color='light',)), width=2),

                dbc.Col(html.Div(
                    dbc.Alert("EXPENSES " + 
                        get_expenses(master_df), color='light')), width=2),

                dbc.Col(html.Div(
                    dbc.Alert("DISCOUNT " + 
                        get_discount(master_df), color='light')), width=2),

                dbc.Col(html.Div(
                    dbc.Alert("PROFIT " + 
                        get_profit(master_df), color='light')), width=2),

                dbc.Col(html.Div(
                    dbc.Alert("MARGIN " + 
                        get_sales_margin(master_df), color='light')), width=2),

        ], align="center",
            justify="center"),

        html.Div(
            [
            html.Div([
                dcc.Dropdown(
                            id = 'Cities',
                            options=[
                                {'label': 'Country', 'value': 'Country'},
                                {'label': 'Employee', 'value': 'EmployeeName'}
                            ],
                            value='Country',
                            style={'height': 'auto', 'width': '700px', 'align':'center'}
                        ),
                dcc.Graph(
                    id='bar_graph'
                )
                ], className= 'six columns',
                    style={'border-radius': '15px', 
                            'backgroundColor': '#f8f9fa', 
                            'box-shadow' : '4px 4px 2.5px #dddddd',
                            'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'} 
                ),

            html.Div([
                dcc.Graph(
                    id='graph-4',
                    figure=map_data
                )
                ], className= 'six columns', 
                    style={'border-radius': '15px', 
                            'backgroundColor': '#f8f9fa', 
                            'box-shadow' : '4px 4px 2.5px #dddddd',
                            'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'}
                )
            ], className="row"
        ),


        html.Div(
            [
            html.Div([
                dash_table.DataTable(
                        id='datatable-interactivity',
                        data=data_table.to_dict('records'),
                        columns=[{'name': i, 'id': i, "deletable":True,"selectable":True} for i in data_table.columns],
                        editable = True,
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable="single",
                        row_selectable="multi",
                        row_deletable=True,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current= 0,
                        page_size=55,
                        style_cell={
                        'textOverflow': 'ellipsis',
                        'overflow': 'hidden'
                        },
                        style_table={
                        'width':'700px',
                        'height':'600px',
                        'overflowY':'auto',
                        'overflowX': 'auto',
                        'align': 'center'
                        },
                        style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                        }       
                )
                ], className= 'six columns',
                    style={'border-radius': '15px', 
                                'backgroundColor': '#f8f9fa', 
                                'box-shadow' : '4px 4px 2.5px #dddddd',
                                'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'}),
            html.Div([
                dcc.Graph(
                    id='graph-1', figure=viz_scatter_iii
                )
                ],  className= 'six columns', 
                    style={'border-radius': '15px', 
                            'backgroundColor': '#f8f9fa', 
                            'box-shadow' : '4px 4px 2.5px #dddddd',
                            'padding':'20px', 'margin-left':'auto','margin-right':'auto', 'margin-top':'25px'}
                ),
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)

# ################################################################################
# Connect the Plotly graphs with Dash Components

# Interactivity with table

@app.callback(
    dash.dependencies.Output('bar_graph', 'figure'),
    [dash.dependencies.Input('Cities', 'value')])
def select_cat(selector):
    revenue_country = master_df[['Country','Sales', 'EmployeeName']]
    revenue_country = revenue_country.groupby(selector).sum().reset_index().sort_values('Sales')

    revenue_country_viz = px.bar(revenue_country, y=selector, x='Sales', text='Sales', template="seaborn",
            hover_data={'Sales':':.2f'}, title='REVENUE BY ' + str(selector).upper())

    revenue_country_viz.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    revenue_country_viz.update_layout(uniformtext_minsize=7, uniformtext_mode='hide', height=600)

    revenue_country_viz.update_layout(
                hoverlabel=dict(
                    bgcolor="white", 
                    font_size=16, 
                    font_family="Open Sans"
                ),
                title={
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                        font=dict(
                        size=16,
                        color="#4a4a4a"
                        ),
                        paper_bgcolor="#f8f9fa")
    return revenue_country_viz
# def update_table(input_value):
#     return generate_table(df_table.sort_values([input_value], ascending=[False]).reset_index())

# @app.callback(
#     Output(component_id='bar-chart', component_property='figure'),
#     [Input(component_id='bubble-chart', component_property='hoverData')]
# )

# def update_graph(master_df):
#    return bar(master_df)


# ################################################################################
if __name__ == '__main__':

    app.run_server(debug=True)
