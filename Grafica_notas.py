import pandas as pd
import dash
from dash import html,dcc, Input,Output
import plotly.express as px

#cargar los datos
df = pd.read_csv("Notaslimpias.csv")
#print(df.head())

#iniciar la aplicacion
app = dash.Dash(__name__)
app.title = "Dashboard de Notas"
 
 #crear el layout
app.layout = html.Div([
    html.H1("Dashboard de notas de estudiantes",style={"textAlign":"center"}),
    html.Label("Seleccionar una carrera:"),
    dcc.Dropdown(id="filtro-carrera",
                 options=[{"label":carrera,"value":carrera}for 
                                   carrera in sorted(df["Carrera"].unique())],
                                   value=df["Carrera"].unique()[0],
                                             clearable=False
                                    ),
                                     html.Br(),
                                     dcc.Tabs([
                                    dcc.Tab(label='Grafico de promedios',children=[
                                        dcc.Graph(id='grafico-histografa')
                                    ]), 
                                    dcc.Tab(label="Edad vs Promedio",children=[
                                        dcc.Graph(id='grafico-dispersion')
                                    ]),
                                    dcc.Tab(label="Desempeño",children=[
                                        dcc.Graph(id='grafico-pie')
                                    ]),
                                    dcc.Tab(label="Promedio de notas por carrera",children=[
                                        dcc.Graph(id='grafico-barras')
                                    ])    
                                    
                                    ])

])

#actualizar el grafico
@app.callback(Output("grafico-histografa","figure"),
              Output("grafico-dispersion","figure"),
              Output("grafico-pie","figure"),
              Output("grafico-barras","figure"),
              Input("filtro-carrera",'value'))

#crear funcion
def actualizar_grafico(seleccion_carrera):

   filtrado = df[df["Carrera"] == seleccion_carrera]

   hist = px.histogram(filtrado,x="Promedio",nbins=10,title=f" Distribucción de promedios -{seleccion_carrera}")
   scatter = px.scatter(filtrado,x="Edad",y="Promedio",color="Desempeño",title=f" Edad vs promedio -{seleccion_carrera}")
   pie = px.pie(filtrado,names="Desempeño",title=f" Desempeño-{seleccion_carrera}")
   #agrupar por carrera y calcular promedio
   promedios = df.groupby("Carrera")["Promedio"].mean().reset_index()
   fig =px.bar(promedios,x="Carrera",y="Promedio",title='Promedio de notas por carrera',color="Carrera",
               color_discrete_sequence=px.colors.qualitative.Dark2)

   return hist,scatter,pie,fig



#ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)