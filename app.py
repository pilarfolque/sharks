from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc 
from dash import dcc, html
import pandas as pd
from src.etl import cargar_datos
from src.graphics import create_graph, create_graphs_2
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64 




app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Análisis Ataques Tiburones"

file_path = 'SharkIncidents-Cleaned.csv'
shark_data = cargar_datos(file_path)

file_path_fatal = 'fatal_shark_attacks.csv'
shark_data_fatal=cargar_datos(file_path_fatal)

file_path_gsaf5 = 'GSAF5.csv'

gsaf5_data=cargar_datos(file_path_gsaf5)

gsaf5_data = gsaf5_data.dropna(subset=['Country', 'Activity','Year', 'Type'])


gsaf5_data['Year'] = pd.to_numeric(gsaf5_data['Year'], errors='coerce')
gsaf5_data['Type'] = gsaf5_data['Type'].astype(str)
gsaf5_data['Country'] = gsaf5_data['Country'].astype(str)
gsaf5_data['Activity'] = gsaf5_data['Activity'].astype(str)


gsaf5_normalized = gsaf5_data[['Year', 'Time', 'Country', 'Activity', 'Fatal (Y/N)']].dropna()


probabilidad_year = gsaf5_normalized['Year'].value_counts(normalize=True)
probabilidad_country = gsaf5_normalized['Country'].value_counts(normalize=True)
probabilidad_activity = gsaf5_normalized['Activity'].value_counts(normalize=True)
probabilidad_time = gsaf5_normalized['Time'].value_counts(normalize=True)


def calcular_probabilidad(year, country, activity,time):
    print(gsaf5_data.columns)

    prob_year = probabilidad_year.get(year, 0)
    prob_country = probabilidad_country.get(country, 0)
    prob_activity = probabilidad_activity.get(activity, 0)
    prob_time = probabilidad_activity.get(time, 0)
   
    

    return ((prob_country + prob_activity+ prob_time+prob_year) / 4)




app.layout = html.Div([
    
    html.H1(
        "Análisis Ataques Tiburones", 
        style={
            'text-align': 'center', 
            'color': '#007bff', 
            'margin-bottom': '30px', 
            'text-shadow': '2px 2px 8px rgba(0, 123, 255, 0.7)',
            'font-family': 'Arial, sans-serif', 
            'font-weight': 'bold',
            'font-size': '40px',
            'transition': 'all 0.3s ease-in-out'
        }
    ),

    
    dcc.Tabs([
        
        dcc.Tab(
            label='Pricipales factores de ataque',
            children=[
                html.Div([
                    html.Img(id="graph", src="data:image/png;base64,{}".format(create_graph(shark_data)), style={'width': '100%'})
                ], style={'padding': '20px'})
            ],
            style={'backgroundColor': '#f8f9fa', 'color': '#5a5a5a', 'border': 'none'},
            selected_style={'backgroundColor': '#007bff', 'color': '#fff'}
        ),
        
        dcc.Tab(
            label='Edad y tipo de lesión',
            children=[
                html.Div([
                    html.Img(id="graph1", src="data:image/png;base64,{}".format(create_graphs_2(shark_data_fatal)[0]), style={'width': '100%'}),
                    html.Img(id="graph2", src="data:image/png;base64,{}".format(create_graphs_2(shark_data_fatal)[1]), style={'width': '100%'}),
                    html.Img(id="graph3", src="data:image/png;base64,{}".format(create_graphs_2(shark_data_fatal)[2]), style={'width': '100%'})
                ], style={'padding': '20px'})
            ],
            style={'backgroundColor': '#f8f9fa', 'color': '#5a5a5a', 'border': 'none'},
            selected_style={'backgroundColor': '#007bff', 'color': '#fff'}
        ),
        
        dcc.Tab(
            label='Calculador de riesgo',
            children=[
                html.Div([
                    dbc.Card([
                        dbc.CardHeader(
                            "Formulario para predecir el riesgo de ataques de tiburón",
                            style={'font-weight': 'bold', 'font-size': '20px', 'color': '#fff', 'background-color': '#007bff'}
                        ),
                        dbc.CardBody([
                            html.Label("País:", style={'font-weight': 'bold', 'font-size': '16px'}),
                            dcc.Dropdown(
                                id='dropdown-pais',
                                options=[{'label': country, 'value': country} for country in sorted(gsaf5_data['Country'].dropna().unique())],
                                placeholder="Seleccionar país",
                                style={
                                    'width': '100%', 
                                    'padding': '10px',
                                    'font-family': 'Arial, sans-serif',
                                    'font-size': '14px',
                                    'border-radius': '5px',
                                    'border': '1px solid #ddd',
                                    'box-shadow': '0 2px 5px rgba(0, 0, 0, 0.1)'
                                },
                                
                                className='dropdown-input'
                            ),
                            html.Label("Actividad:", style={'font-weight': 'bold', 'font-size': '16px', 'margin-top': '10px'}),
                            dcc.Dropdown(
                                id='dropdown-actividad',
                                options=[{'label': activity, 'value': activity} for activity in sorted(gsaf5_data['Activity'].dropna().unique())],
                                placeholder="Seleccione una actividad",
                                style={
                                    'width': '100%', 
                                    'padding': '10px',
                                    'font-family': 'Arial, sans-serif',
                                    'font-size': '14px',
                                    'border-radius': '5px',
                                    'border': '1px solid #ddd',
                                    'box-shadow': '0 2px 5px rgba(0, 0, 0, 0.1)'
                                },
                                className='dropdown-input'
                            ),
                            html.Label("Año:", style={'font-weight': 'bold', 'font-size': '16px', 'margin-top': '10px'}),
                            dcc.Input(
                                id='input-year',
                                type='number',
                                placeholder="Añadir un año (entre 1900 y 2023)",
                                min=1900,
                                max=2023,
                                style={
                                    'width': '100%',
                                    'padding': '10px',
                                    'font-family': 'Arial, sans-serif',
                                    'font-size': '14px',
                                    'border-radius': '5px',
                                    'border': '1px solid #ddd',
                                    'box-shadow': '0 2px 5px rgba(0, 0, 0, 0.1)'
                                }
                            ),
                            html.Label("Hora (0-23):", style={'font-weight': 'bold', 'font-size': '16px', 'margin-top': '10px'}),
                            dcc.Input(
                                id='input-hora',
                                type='number',
                                placeholder="Ingrese una hora",
                                min=0,
                                max=23,
                                style={
                                    'width': '100%',
                                    'padding': '10px',
                                    'font-family': 'Arial, sans-serif',
                                    'font-size': '14px',
                                    'border-radius': '5px',
                                    'border': '1px solid #ddd',
                                    'box-shadow': '0 2px 5px rgba(0, 0, 0, 0.1)',
                                }
                            ),
                            html.Button('Calcular Probabilidad', id='calcular-btn', n_clicks=0,
                                        style={'margin-top': '20px', 'backgroundColor': '#28a745', 'color': '#fff', 'width': '100%', 'font-size': '16px'}),
                            html.Div(id='resultado-probabilidad',
                                     style={'margin-top': '20px', 'font-size': '18px', 'font-weight': 'bold', 'color': '#333', 'text-align': 'center'})
                        ])
                    ], style={'padding': '20px', 'backgroundColor': '#f4f4f9', 'borderRadius': '8px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'})
                ], style={'padding': '20px', 'backgroundColor': '#f4f4f9'})
            ],
            style={'backgroundColor': '#f8f9fa', 'color': '#5a5a5a', 'border': 'none'},
            selected_style={'backgroundColor': '#007bff', 'color': '#fff'}
        )
    ])
], style={'backgroundColor': '#f4f4f9', 'padding': '30px'})




@app.callback(
    Output('resultado-probabilidad', 'children'),
    [Input('calcular-btn', 'n_clicks')],
    [Input('dropdown-pais', 'value'),
     Input('dropdown-actividad', 'value'),
     Input('input-year', 'value'),
     Input('input-hora', 'value')]
)
def estimar_riesgo(n_clicks, pais, actividad, year, hora):
    if n_clicks > 0 and pais and actividad and year and hora is not None:
        
        probabilidad = calcular_probabilidad(year, pais, actividad,hora) 
        
        if probabilidad > 0.1:
            probabilidad = probabilidad*100
            return f"Alta probabilidad de ataque de tiburón en {pais}, durante {actividad}, en el año {year} a las {hora}:00 con probabilidad de {probabilidad:.2f}%."
        else:
            return f"Baja probabilidad de ataque de tiburón en {pais}, durante {actividad}, en el año {year} a las {hora}:00 con probabilidad de {probabilidad:.2f}%."
    return "Introduce los datos para calcular la probabilidad."


if __name__ == '__main__':
    app.run_server(debug=True)
