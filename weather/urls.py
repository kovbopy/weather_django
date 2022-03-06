from django.urls import path
from .views import now,by_3_hours,by_day


urlpatterns = [
    path('now/<city>/', now),# to see current weather
    path('hours/<period>/<city>/', by_3_hours),# hours/7-9/minsk/ (7-9 april) -- shows stats for every 3 hours
    path('day/<period>/<city>/', by_day),# day/9/minsk/ -- shows stats for the whole day
]




