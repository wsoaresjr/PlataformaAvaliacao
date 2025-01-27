from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Carregue os dados
df = pd.read_csv('dados_proficiencia.csv')

# Registre o aplicativo Dash
app = DjangoDash("grafico_geral")

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Painel de Proficiência"),
    dcc.Dropdown(
        id="filtro_escola",
        options=[{"label": escola, "value": escola} for escola in df["Nome da Escola"].unique()],
        placeholder="Selecione uma Escola",
    ),
    dcc.Graph(id="grafico")
])

# Callback para atualizar o gráfico com base no filtro
@app.callback(
    Output("grafico", "figure"),
    [Input("filtro_escola", "value")]
)
def atualizar_grafico(escola):
    if escola:
        dados_filtrados = df[df["Nome da Escola"] == escola]
    else:
        dados_filtrados = df

    fig = px.bar(
        dados_filtrados,
        x="Turma",
        y=["ProficienciaLinguagens", "ProficienciaMatematica", "ProficienciaCH", "ProficienciaCN"],
        title="Proficiência por Turma",
        barmode="group",
    )
    return fig
