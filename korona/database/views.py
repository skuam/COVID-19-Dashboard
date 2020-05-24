# Create your views here.
from django.shortcuts import render

from .models import Country

from .plots import *
from .preproces import Update_Day
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
import numpy as np
import pandas as pd

def mainpage(request):
    Update_Day()
    return render(request, "mainpage/mainpage.html")


def wykres(request,country = "Poland"):
    df = Get_Full_Data_Frame()
    # filtter to selected country
    df = df.loc[df['Country'] == country]
    fig = go.Figure()
    Dead = go.Scatter(x=df["Date"], y=df["Dead"], name='Deaths')
    Inf = go.Scatter(x=df["Date"], y=df["Infected"], name='Confirmed')
    Rec = go.Scatter(x=df["Date"], y=df["Recovered"], name='Recovered')
    fig.add_traces([Dead, Inf, Rec])
    #plotly.offline.plot(fig, filename="database/static_plots/wykers1" + '.html')
    graph = fig.to_html(default_height=1000, default_width=1000)
    context = {'graph': graph, 'Countries': Country.objects.all()}
    return render(request, 'graph/graph.html', context)


def trend(request):
    country = "Poland"
    df = Get_Full_Data_Frame()
    df = df.loc[df['Country'] == country]

    fig = make_subplots(rows=3, cols=1, subplot_titles=("Deaths", "Confirmed", "Recovered"))
    date = df["Date"]

    LowerBund = 10
    UpperBound = 14
    predictionrange = np.arange(LowerBund, UpperBound+date.index[-1])

    last = date.tail(1).values[0]
    upper = last + datetime.timedelta(days=UpperBound)
    daterange = pd.date_range(last, upper)

    #prediction for dead
    yD = df["Dead"]
    poly = np.polyfit(yD.index[10:], yD[10:], 4)
    predictionsDead = np.polyval(poly, predictionrange)
    Dead = go.Scatter(x=date, y=df["Dead"], name='Deaths')
    DeadPred = go.Scatter(x=daterange, y=predictionsDead[date.index[-12]:], name='Predictions')
    fig.append_trace(Dead, row=1, col=1)
    fig.append_trace(DeadPred, row=1, col=1)

    #prediction for infected
    yI = df["Infected"]
    poly = np.polyfit(yI.index[10:], yI[10:], 4)
    predictionsInf = np.polyval(poly, predictionrange)
    Inf = go.Scatter(x=date, y=df["Infected"], name='Confirmed')
    InfPred = go.Scatter(x=daterange, y=predictionsInf[date.index[-12]:], name='Prediction')
    fig.append_trace(Inf, row=2, col=1)
    fig.append_trace(InfPred, row=2, col=1)

    #prediction for Recoverd
    yR = df["Recovered"]
    poly = np.polyfit(yR.index[10:], yR[10:], 3)
    predictionsRec = np.polyval(poly, predictionrange)
    Rec = go.Scatter(x=date, y=df["Recovered"], name='Recovered')
    RecPred = go.Scatter(x=daterange, y=predictionsRec[date.index[-12]:], name='Prediction')
    fig.append_trace(Rec, row=3, col=1)
    fig.append_trace(RecPred, row=3, col=1)


    graph = fig.to_html(default_height=1500, default_width=1000)
    context = {'graph': graph}
    return render(request, 'graph/trend.html', context)
