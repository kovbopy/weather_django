from django.urls import path
from .views import now,by_3_hours,by_day


urlpatterns = [
    path('now/<city>/', now),
    path('hours/<period>/<city>/', by_3_hours),
    path('day/<period>/<city>/', by_day),
]

