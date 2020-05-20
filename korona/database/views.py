# Create your views here.
from django.shortcuts import render

from .models import Country

from .plots import *


def mainpage(request):
    data = Country.objects.last()
    stu = {
        "Country": {
            'Infected': data.Infected,
            'Recovered': data.Recovered,
            'Dead': data.Dead
        }
    }
    return render(request, "mainpage/mainpage.html", stu)


def wykres(request):
    country = "Poland"
    df = Get_Full_Data_Frame()
    # filtter to selected country
    df = df.loc[df['Country'] == country]
    fig = go.Figure()
    Dead = go.Scatter(x=df["Date"], y=df["Dead"], name='Deaths')
    Inf = go.Scatter(x=df["Date"], y=df["Infected"], name='Confirmed')
    Rec = go.Scatter(x=df["Date"], y=df["Recovered"], name='Recovered')
    fig.add_traces([Dead, Inf, Rec])
    #plotly.offline.plot(fig, filename="database/static_plots/wykers1" + '.html')
    graph = fig.to_html(default_height=500, default_width=700)
    context = {'graph': graph}
    return render(request, 'graph/graph.html', context)
