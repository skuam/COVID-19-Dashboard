from . import models

import plotly.graph_objects as go
import plotly


def Get_Full_Data_Frame():
    return models.Country.objects.all().to_dataframe()

def PlotAll(country = "Poland"):
    df = Get_Full_Data_Frame()
    # filtter to selected country
    df = df.loc[df['Country'] == country]
    fig = go.Figure()
    Dead = go.Scatter(x = df["Date"], y = df["Dead"], name='Deaths')
    Inf = go.Scatter(x=df["Date"], y=df["Infected"],name='Confirmed')
    Rec = go.Scatter(x=df["Date"], y=df["Recovered"],name='Recovered')
    fig. add_traces([Dead,Inf,Rec])
    plotly.offline.plot(fig, filename="database/static_plots/wykers1" + '.html')
