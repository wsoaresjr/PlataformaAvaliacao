import dash
from dash import html
from django_plotly_dash import DjangoDash

# Registre a aplicação Dash
app = DjangoDash("grafico_geral")

# Layout do Dash
app.layout = html.Div("Este é um gráfico interativo!")
