from . import models

import plotly.graph_objects as go
import plotly
import datetime
import numpy as np
import pandas as pd

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




def Predict(country = "Poland", fitfor= "Dead",LowerBund = 10,UpperBound = 14 ):
    df = Get_Full_Data_Frame()
    # filtter to selected country
    df = df.loc[df['Country'] == country]

    date = df["Date"]
    y = df[fitfor]

    predictionrange = np.arange(LowerBund, UpperBound+y.index[-1])
    last = date.tail(1).values[0]
    upper = last + datetime.timedelta(days=UpperBound)
    daterange = pd.date_range(date[0]+datetime.timedelta(days=LowerBund), upper)
    bestfit = 3
    if fitfor == "Dead" : bestfit = 4

    #ignore intial 10 days
    poly = np.polyfit(y.index[10:], y[10:], bestfit)
    #make predictions
    predictions_poly = np.polyval(poly, predictionrange)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x = date, y=y, name=fitfor))

    fig.add_trace(go.Scatter(x = daterange, y=predictions_poly, name="polynomial fit"))

   # fig.update_xaxes( tick0 = date[0], dtick = 86400000)
    plotly.offline.plot(fig, filename=f"database/static_plots/wykers" + '.html')