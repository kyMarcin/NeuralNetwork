import csv
import datetime
import numpy as np
from dataproviders import cyclic_data_representation as cdr


class ElectricityData(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.max_consumption_value = 30000

        training_end_date = datetime.datetime(2016, 12, 31)
        validation_end_date = datetime.datetime(2017, 12, 31)

        self.training_set_input = []
        self.training_set_output = []

        self.validation_set_input = []
        self.validation_set_output = []

        with open(self.data_path) as csvfile:
            reader = csv.reader(csvfile)
            csv_list = list(reader)

            for i in range(1, csv_list.__len__()):
                components = csv_list[i][0].split(';')
                date = components[0]
                hour = components[1]

                current_datetime = datetime.datetime.strptime(date, "%Y%m%d")
                if current_datetime < validation_end_date:
                    x = [1,
                         cdr.day_in_year_sin_representation(int(current_datetime.strftime('%j'))),
                         cdr.day_in_year_cos_representation(int(current_datetime.strftime('%j'))),
                         cdr.day_in_week_sin_representation(int(current_datetime.weekday())),
                         cdr.day_in_week_cos_representation(int(current_datetime.weekday())),
                         cdr.hour_sin_representation(int(hour)),
                         cdr.hour_cos_representation(int(hour))]
                    y = []
                    for k in range(0, 24):
                        consumption = csv_list[i + k][0].split(';')[2]
                        y.append(consumption)

                    if current_datetime <= training_end_date:
                        self.training_set_input.append(x)
                        self.training_set_output.append(y)
                    else:
                        self.validation_set_input.append(x)
                        self.validation_set_output.append(y)
                else:
                    continue

    def get_training_set_input(self):
        return_set = np.array(self.training_set_input, dtype=float)
        return return_set

    def get_training_set_output(self):
        return_set = np.array(self.training_set_output, dtype=float)
        return_set = return_set / self.max_consumption_value
        return return_set

    def get_validation_set_input(self):
        return_set = np.array(self.validation_set_input, dtype=float)
        return return_set

    def get_validation_set_output(self):
        return_set = np.array(self.validation_set_output, dtype=float)
        return_set = return_set / self.max_consumption_value
        return return_set

    def set_max_consumption_value(self, value):
        self.max_consumption_value = value

    def get_max_consumption_value(self):
        return self.max_consumption_value
