import urllib.parse
import requests
import json
from datetime import datetime, timedelta


def write_to_json_file(path, file_name, data):
    file_path_name = './' + path + '/' + file_name + '.json'
    with open(file_path_name, 'w') as fp:
        json.dump(data, fp)


def temperatures_json_by_city_name(city_name, start_date, end_date):
    data = {}
    data['cityName'] = city_name
    days = data['days'] = []

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    start = start - timedelta(days=1)
    while start < end:
        start = start + timedelta(days=1)
        current_start_date = datetime.strftime(start, "%Y-%m-%d")
        start = start + timedelta(days=30)
        if start > end:
            start = end
        current_end_date = datetime.strftime(start, "%Y-%m-%d")

        api_key = 'f56b50156a4c4ae6aee192530180703'
        main_url = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?'
        url = main_url + urllib.parse.urlencode({'key': api_key,
                                                 'q': city_name,
                                                 'format': 'json',
                                                 'date': current_start_date,
                                                 'enddate': current_end_date})

        json_data = requests.get(url).json()
        days_json_list = json_data['data']['weather']
        for current_day in days_json_list:
            date = current_day['date']
            day = {}
            day['date'] = date
            day['maxTempC'] = current_day['maxtempC']
            day['minTempC'] = current_day['mintempC']
            hours = day['hours'] = []
            hours_json_list = current_day['hourly']
            for hour in hours_json_list:
                hour_info = {}
                hour_info['time'] = hour['time']
                hour_info['tempC'] = hour['tempC']
                hour_info['FeelsLikeC'] = hour['FeelsLikeC']
                hours.append(hour_info)
            days.append(day)
    write_to_json_file('./', city_name + ' ' + start_date + ' - ' + end_date, data)


temperatures_json_by_city_name('Warsaw', '2017-08-02', '2017-11-03')
