# Create your views here.
from django.shortcuts import render

from .models import Country
from django import forms

from .plots import *
from .preproces import Update_Day
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
import numpy as np
import pandas as pd

selected_country = "Poland"


def mainpage(request):
    Update_Day()
    return render(request, "mainpage/mainpage.html")


def wykres(request):
    global selected_country
    if request.GET and request.GET['country']:
        selected_country = request.GET['country']
    Update_Day(selected_country)
    df = Get_Full_Data_Frame()
    country_list = df['Country'].unique()
    df = df.loc[df['Country'] == selected_country]
    context = {
        'graph': getGraph(df),
        'Countries': getCountries(df),
        'country_list': sorted(country_list),
        'selectedCountry': selected_country
    }
    return render(request, 'graph/graph.html', context)


def trend(request):
    global selected_country
    if request.GET and request.GET['country']:
        selected_country = request.GET['country']
    print(selected_country)
    df = Get_Full_Data_Frame()
    country_list = df['Country'].unique()
    df = df.loc[df['Country'] == selected_country]

    fig = make_subplots(rows=3, cols=1, subplot_titles=(
        "Deaths", "Confirmed", "Recovered"))
    date = df["Date"]

    UpperBound = 14
    predictionrange = np.arange(5, UpperBound+date.index[-1])

    last = date.tail(1).values[0]
    upper = last + datetime.timedelta(days=UpperBound)
    daterange = pd.date_range(last, upper)

    # prediction for dead
    yD = df["Dead"]
    poly = np.polyfit(yD.index[10:], yD[10:], 1)
    predictionsDead = np.polyval(poly, predictionrange)
    Dead = go.Scatter(x=date, y=df["Dead"], name='Deaths')
    DeadPred = go.Scatter(
        x=daterange, y=predictionsDead[date.index[-14]:], name='Predictions')
    fig.append_trace(Dead, row=1, col=1)
    fig.append_trace(DeadPred, row=1, col=1)

    # prediction for infected
    yI = df["Infected"]
    poly = np.polyfit(yI.index[10:], yI[10:], 1)
    predictionsInf = np.polyval(poly, predictionrange)
    Inf = go.Scatter(x=date, y=df["Infected"], name='Confirmed')
    InfPred = go.Scatter(
        x=daterange, y=predictionsInf[date.index[-14]:], name='Prediction')
    fig.append_trace(Inf, row=2, col=1)
    fig.append_trace(InfPred, row=2, col=1)

    # prediction for Recoverd
    yR = df["Recovered"]
    poly = np.polyfit(yR.index[30:], yR[30:], 1)
    predictionsRec = np.polyval(poly, predictionrange)
    Rec = go.Scatter(x=date, y=df["Recovered"], name='Recovered')
    RecPred = go.Scatter(
        x=daterange, y=predictionsRec[date.index[-14]:], name='Prediction')
    fig.append_trace(Rec, row=3, col=1)
    fig.append_trace(RecPred, row=3, col=1)

    graph = fig.to_html(default_height=1500, default_width=1000)
    context = {
        'graph': graph,
        'country_list': sorted(country_list),
        'selectedCountry': selected_country
    }
    return render(request, 'graph/trend.html', context)


def getGraph(df):
    fig = go.Figure()
    Dead = go.Scatter(x=df["Date"], y=df["Dead"], name='Deaths')
    Inf = go.Scatter(x=df["Date"], y=df["Infected"], name='Confirmed')
    Rec = go.Scatter(x=df["Date"], y=df["Recovered"], name='Recovered')
    fig.add_traces([Dead, Inf, Rec])
    graph = fig.to_html()
    return graph


def getCountries(df):
    countryList = []
    for index, row in df.iterrows():
        countryList.append(
            {
                'confirmed': row['Infected'],
                'recovered': row['Recovered'],
                'dead': row['Dead'],
                'date': row['Date'],
            })
    return countryList
