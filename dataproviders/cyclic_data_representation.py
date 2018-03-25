import math


def day_in_year_sin_representation(no_day):
    return math.sin(2 * math.pi * no_day / 366)


def day_in_year_cos_representation(no_day):
    return math.cos(2 * math.pi * no_day / 366)


def day_in_week_sin_representation(no_day):
    return math.sin(2 * math.pi * (no_day + 1) / 7)


def day_in_week_cos_representation(no_day):
    return math.cos(2 * math.pi * (no_day + 1) / 7)


def hour_sin_representation(no_hour):
    return math.sin(2 * math.pi * no_hour / 24)


def hour_cos_representation(no_hour):
    return math.cos(2 * math.pi * no_hour / 24)
