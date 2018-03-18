import glob
import json
import urllib.parse
import requests
from datetime import datetime, timedelta


def write_to_json_file(path, file_name, data):
    file_path_name = './' + path + '/' + file_name + '.json'
    with open(file_path_name, 'w') as fp:
        json.dump(data, fp)


def generate_city_temperatures_json(city_name, start_date, end_date, path):
    api_key = 'f56b50156a4c4ae6aee192530180703'
    main_url = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?'
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

        url = main_url + urllib.parse.urlencode({'key': api_key,
                                                 'q': city_name,
                                                 'format': 'json',
                                                 'date': current_start_date,
                                                 'enddate': current_end_date})

        json_data = requests.get(url).json()
        main_data_json = json_data['data']
        days_json_list = main_data_json['weather']
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
    write_to_json_file(path, city_name + ' ' + start_date + ' - ' + end_date, data)


def generate_average_temperatures_json(files_path, file_name, destination_path):
    json_files = glob.glob(files_path + '*.json')
    return_json = {}
    with open(json_files[0]) as json_data:
        first_city_json = json.load(json_data)
        return_json['days'] = first_city_json['days']

    json_files.remove(json_files[0])
    output_days = return_json['days']
    for json_file in json_files:
        with open(json_file) as json_data:
            current_json = json.load(json_data)
            days = current_json['days']

            i = 0
            for day in days:
                output_days[i]['maxTempC'] = int(output_days[i]['maxTempC']) + int(day['maxTempC'])
                output_days[i]['minTempC'] = int(output_days[i]['minTempC']) + int(day['minTempC'])
                current_output_hours = output_days[i]['hours']

                hours = day['hours']
                j = 0
                for hour in hours:
                    current_output_hours[j]['tempC'] = int(current_output_hours[j]['tempC']) + int(hour['tempC'])
                    current_output_hours[j]['FeelsLikeC'] = int(current_output_hours[j]['FeelsLikeC']) + int(
                        hour['FeelsLikeC'])
                    j = j + 1

                i = i + 1

    print(return_json['days'][160])
    no_cities = json_files.__len__() + 1  # +1 cuz i removed one city at the beginning
    for day in return_json['days']:
        day['maxTempC'] = int(day['maxTempC']) / no_cities
        day['minTempC'] = int(day['minTempC']) / no_cities
        hours = day['hours']
        for hour in hours:
            hour['tempC'] = int(hour['tempC']) / no_cities
            hour['FeelsLikeC'] = int(hour['FeelsLikeC']) / no_cities
    print(return_json['days'][160])
    write_to_json_file(destination_path, file_name, return_json)


cities = ['Bialystok', 'Bydgoszcz', 'Cracow', 'Gdańsk', 'Katowice', 'Lodz', 'Lublin', 'Poznan', 'Szczecin', 'Warsaw',
          'Wroclaw']

city_json_destination_path = '../resources/cities temperature/'

for city in cities:
    generate_city_temperatures_json(city, '2013-01-01', '2017-12-31', city_json_destination_path)

cities_files_path = city_json_destination_path
average_temperatures_destination_path = '../resources'

generate_average_temperatures_json(cities_files_path, 'Average temperatures', average_temperatures_destination_path)
