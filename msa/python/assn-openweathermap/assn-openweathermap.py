import csv
import requests
import sys

import datetime
from statistics import mean


api_key = "a9e905e42c71ec13be586fa6c826bb98"

city_list = [
    "Buenos Aires, Argentina",
    "Guangzhou, China",
    "Wichita, Kansas",
    "Niskayuna, New York",
    "Gwangmyeong, South Korea",
    "Taipei, Taiwan",
    "Nanaimo, British Columbia",
    "Chennai, India",
    "Barrington, Illinois",
    "Littleton, Colorado",
    "Peterhead, Scotland",
    "Vizag, India",
    "Des Moines, Iowa",
    "Bejing, China",
    "Killeen, Texas",
    "Morehead City, North Carolina",
]


def find_min_max_avg(data, beg):
    temp = []  #  Output CSV line

    min_sum = 0  #  Daily min/max sums
    max_sum = 0

    for i in range(beg, beg + 32, 8):  #  Loop over four days
        #  For each day, pull the six min and max temps as a list comprehension

        min_temp = [dt["main"]["temp_min"] for dt in data["list"][i : i + 8]]
        max_temp = [dt["main"]["temp_max"] for dt in data["list"][i : i + 8]]

        min_day = round(min(min_temp), 2)  #  Compute daily min/max
        max_day = round(max(max_temp), 2)

        temp += [f"{min_day:.02f}", f"{max_day:.02f}"]
        min_sum += min_day
        max_sum += max_day

    #  Add overall min/max average

    min_sum /= 4
    max_sum /= 4
    temp += [f"{min_sum:.02f}", f"{max_sum:.02f}"]

    return temp


#  End function find_min_max_avg


def find_tomorrow(data):
    for i, dt in enumerate(data["list"]):
        #        dt_tm = datetime.datetime.utcfromtimestamp(dt["dt"])
        dt_tm = datetime.datetime.fromtimestamp(dt["dt"], datetime.UTC)
        if dt_tm.hour == 0:  #  Midnight? If yes, return index
            return i

    return -1  #  No midnight found?


#  End function find_tomorrow


def write_temp(temp, fname="temp.csv"):
    out = open(fname, "w", newline="", encoding="utf8")
    writer = csv.writer(out)

    header = [
        "City",
        "Min 1",
        "Max 1",
        "Min 2",
        "Max 2",
        "Min 3",
        "Max 3",
        "Min 4",
        "Max 4",
        "Min Avg",
        "Max Avg",
    ]
    writer.writerow(header)

    for i, t in enumerate(temp):
        t = [city_list[i]] + t
        writer.writerow(t)

    out.close()


#  End function write_temp


#  Mainline

city_temp = []

for city in city_list:
    geo_URL = "http://api.openweathermap.org/geo/1.0/direct"
    geo = f"{geo_URL}?q={city}&limit=1&appid={api_key}"
    resp = requests.get(geo)

    if resp.status_code != 200:  # Failure?
        print(f"Error geocoding {city}: {resp.status_code}")
        sys.exit(1)

    if len(resp.json()) == 0:
        print(f"Error locating city {city}: {resp.status_code}")
        sys.exit(2)

    #  Since limit=5, a list of cities (1 or more) is returned

    json = resp.json()
    if type(json) == list:  # List of cities?
        lat = json[0]["lat"]
        lon = json[0]["lon"]
    else:  #  Unknown city?
        print(f"Error, invalid data returned for {city}: {resp.status_code}")
        sys.exit(3)

    forecast_URL = "http://api.openweathermap.org/data/2.5/forecast"
    forecast = (
        f"{forecast_URL}?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    )

    resp = requests.get(forecast)
    if resp.status_code != 200:  # Failure
        print(f"Error retrieving data: {resp.status_code}")
        sys.exit(4)
    data = resp.json()

    print(f"{city}:")

    beg = find_tomorrow(data)
    if beg == -1:
        print(f"{city}: Could not find midnight?")
        continue

    city_temp = city_temp + [find_min_max_avg(data, beg)]

write_temp(city_temp)
