from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
import requests
import os
import folium
import json

# Create your views here.
def covidall(request):
    while True:
        try:
            world= requests.get('https://disease.sh/v3/covid-19/all/')
            countrie= requests.get('https://disease.sh/v3/covid-19/countries/')
            covid_all = world.json()
            countries=countrie.json()
        except ConnectionError:
            return render(request,'error.html',)
        content ={'covid_all':covid_all,
                'countries':countries,}
        return render(request,'all.html',content)

overly = os.path.join('data','world-countries.json')
def countries(request):
    try:
        query = request.GET['q']
        count = 'https://disease.sh/v3/covid-19/countries/'+query
        countries = requests.get(count).json()
        con = countries['country']
        lat= countries['countryInfo']['lat']
        lon= countries['countryInfo']['long']

        # print(lat,lon)
        # with open('data/world-countries.json') as handle:
        #     country_geo = json.loads(handle.read())

        # for i in country_geo['features']:
        #     if i['properties']['name'] == query.capitalize():
        #         country = i
        #         break
        maps= folium.Map(location=[lat,lon],zoom_start=5,)
        tooltip = con
        folium.Marker(
            location=[lat,lon],
            tooltip=tooltip,
            icon = folium.Icon(icon='cloud')
        ).add_to(maps)
        # folium.GeoJson(country,
        #        name=con).add_to(maps)
        maps=maps._repr_html_()
    except ConnectionError:
            return render(request,'error.html',)
    except KeyError:
        return render(request,'countries-not.html',)
                
    content ={'countries':countries,'maps':maps}
    return render(request,'countries.html',content)

def error_404(request,exception):
    return render(request,'404.html')