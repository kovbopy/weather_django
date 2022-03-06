import os
from statistics import mean
from dotenv import load_dotenv, find_dotenv
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


load_dotenv(find_dotenv())
key = os.environ['KEY']

@api_view(["GET"])
def now(request, city):
    api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + key
    data = requests.get(api).json()

    key_time = os.environ["KEY_TIME"]
    api_time = "https://timezone.abstractapi.com/v1/current_time/?api_key=" + key_time + "&location=" + city
    time = requests.get(api_time).json()['datetime']

    response = {"city": city,
                "time": time[-8:],
                "temperature": float(str(data['main']['temp'] - 273.15)[0:5]),
                'humidity': f"{data['main']['humidity']}%"
               }
    return Response(response)


@api_view(["GET"])
def by_3_hours(request, period, city):
    api = "https://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=" + key
    data = requests.get(api).json()

    if period == "today":
        today = data['list'][0]['dt_txt'][8:10]

        response = {
            city: [
                {"time": i['dt_txt'][-8:],
                 "temperature": round(i['main']['temp'] - 273.15, 1),
                 "humidity": f"{i['main']['humidity']}%"}
                 for i in data['list'][0:] if i['dt_txt'][8:10] == today or
                                              (int(i['dt_txt'][8:10]) == int(today) + 1 and
                                               i['dt_txt'][11:] == '00:00:00')
            ]
        }
        return Response(response)

    elif "-" in period:
       p_list = [i for i in period]
       hyphen_index = p_list.index("-")
       start_date = int(period[:hyphen_index])
       end_date = int(period[hyphen_index + 1:])

       response={
           city: [
                  {"time": i['dt_txt'],
                   "temperature": round(i['main']['temp'] - 273.15, 1),
                   "humidity": f"{i['main']['humidity']}%"}
                   for i in data['list'][0:] if int(i['dt_txt'][8:10]) in
                                                range(start_date, end_date+1)
            ]
       }
       return Response(response)


@api_view(["GET"])
def by_day(request, period, city):
    api = "https://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid="+ key
    data = requests.get(api).json()

    main = [i for i in data['list'][0:] if i['dt_txt'][9:10] == period or
                                         (int(i['dt_txt'][9:10]) == int(period) + 1 and
                                          i['dt_txt'][11:] == '00:00:00')
            ]

    main_temp = [i['main']['temp'] - 273.15 for i in main]
    avr_temp = round(sum(main_temp) / len(main_temp), 1)
    avr_humid = str(round(mean([i['main']['humidity'] for i in main]), 1)) + "%"
    max_temp = round(max(main_temp), 1)
    min_temp = round(min(main_temp), 1)

    main_day_temp = [i['main']['temp'] - 273.15 for i in main
                     if int(i["dt_txt"][-8:-6]) in range(6, 19)]# from 6 am to 6 pm
    avr_day_temp = round(sum(main_day_temp) / len(main_day_temp),1)
    avr_night_temp = round(mean( [i['main']['temp'] - 273.15 for i in main
                           if not int(i["dt_txt"][-8:-6]) in range(6, 19)] ), 1)

    response={"city": city,
              "date": period,
              "avr_temp": avr_temp,
              "avr_humid": avr_humid,
              "avr_day_temp": avr_day_temp,
              "avr_night_temp": avr_night_temp,
              "max_temp": max_temp,
              "min_temp": min_temp
              }

    return Response(response)
