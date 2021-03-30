from django.urls import path
from django.conf.urls import include, url
from .import views
urlpatterns = [
    path('', views.covidall, name='covid-all'),
    path('countries/',views.countries,name='countries')
]
