# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 12:33:15 2020

@author: healey
"""

# - OPENWEATHERMAP.PY ------------------------------------------------------#
#    Query list of cities to get min/max temperature for upcoming 5 days,   #
#    plus average of the 5-day forecast                                     #
#                                                                           #
# - Modification History: --------------------------------------------------#
#  When:            Who:                    Comments:                       #
#                                                                           #
#  08-Aug-2020      Christopher G. Healey   Initial implementation          #
#  24-Aug-2022      Christopher G. Healey   Fixed for timezone offset       #
#  27-Aug-2022      Christopher G. Healey   Removed timezone to simplify    #
#  05-Jul-2023      Christopher G. Healey   Added new geolocation code      #
# --------------------------------------------------------------------------#

#  Library imports

import csv
import requests
import statistics
import sys

from datetime import datetime
from datetime import timedelta


def K_to_C(k):
    return k - 273.15


def find_next_day(blk_list):
    """Find first entry for tomorrow in list of 3-hour blocks

    Arguments:
            blk_list (list):  List of block dates, format YYYY-mm-dd HH:MM:SS

    Returns:
            int -- index of first blk_list entry for tomorrow
    """

    dt = datetime.now()  #  Get current day
    day = dt.day

    for i, blk in enumerate(blk_list):
        if blk.find("00:00:00") != -1:
            return i  #  Return index of midnight

    return -1  #  No midnight found?


#  End function find_next_day


def get_min_max(city, country, unit=None):
    """Get 4-day min/max forecast temperature @ midnight, add average
    of 4-day forecast

    Arguments:
            city (string): City to query
            country (string):  City's country
    unit (string):  Unit conversion, default=Kelvin

    Returns:
            tuple -- (min,max), two 6-elements lists of min/max's plus avg
    """

    key = "a9e905e42c71ec13be586fa6c826bb98"

    #  Geolocate city

    URL = "http://api.openweathermap.org/geo/1.0/direct"
    geo = f"{URL}?q={city},{country}&limit=5&appid={key}"
    response = requests.get(geo)
    if response.status_code != 200:  #  Error?
        print(f"Error: Cannot geocode {city},{country}: {response.status_code}")
        return ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])

    if len(response.json()) == 0:  #  No such city?
        print(f"Error: Cannot locate {city},{country}")
        return ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])

    #  Since limit=5, a list of ciites (1 or more) is returned

    json = response.json()
    if type(json) == list:  #  List of cities?
        lat = json[0]["lat"]
        lon = json[0]["lon"]
    else:  #  Unknown response returned?
        print(f"Error: Invalid data returned for {city},{country}")
        return ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])

    URL = "http://api.openweathermap.org/data/2.5/forecast"
    URL = f"{URL}?lat={lat}&lon={lon}&appid={key}"
    if unit != None:
        URL = URL + "&" + unit

    min_temp = []  #  Initialize min, max arrays
    max_temp = []

    response = requests.get(URL)
    if response.status_code != 200:  #  Error?
        print(f"Error: Cannot query {city},{country}: {response.status_code}")
        return ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])

    data = response.json()  #  Pull data block

    #  Grab all text versions of block dates to search for first block
    #  representing tomorrow, specifically first midnight 00:00:00

    blk_list = [v["dt_txt"] for v in data["list"]]
    cur = find_next_day(blk_list)

    #  Forcast is in 3-hour steps, 8 hours per day, so setup a set of
    #  indicies from midnight tomorrow, midnight day after tomorrow, and
    #  so on for five days

    #  Setup an index of lists with [start,num_block] for each of the
    #  five days to forecast

    idx = []
    for i in range(cur, cur + (4 * 8), 8):
        block = data["list"][i : i + 8]
        day_min = min([v["main"]["temp_min"] for v in block])
        day_max = max([v["main"]["temp_max"] for v in block])

        if unit == None:
            day_min = K_to_C(day_min)
            day_max = K_to_C(day_max)

        min_temp.append(day_min)  #  Save lowest temp during day
        max_temp.append(day_max)  #  Save highest temp during day

    #  Append 4-day average to min/max temp lists

    min_temp.append(statistics.mean(min_temp))
    max_temp.append(statistics.mean(max_temp))

    return (min_temp, max_temp)


#  End function get_min_max


#  Mainline

loc_01 = [
    ["Anchorage", "Alaska"],
    ["Chennai", "India"],
    ["Jiangbei", "China"],
    ["Kathmandu", "Nepal"],
    ["Kothagudem", "India"],
    ["Lima", "Peru"],
    ["Manhasset", "New York"],
    ["Mexico City", "Mexico"],
    ["Nanaimo", "Canada"],
    ["Peterhead", "Scotland"],
    ["Polevskoy", "Russia"],
    ["Round Rock", "Texas"],
    ["Seoul", "South Korea"],
    ["Solihull", "England"],
    ["Tel Aviv", "Israel"],
]

loc_02 = [
    ["Anchorage", "USA"],
    ["Chennai", "India"],
    ["Jiangbei", "China"],
    ["Kathmandu", "Nepal"],
    ["Kothagudem", "India"],
    ["Lima", "Peru"],
    ["Manhasset", "USA"],
    ["Mexico City", "Mexico"],
    ["Nanaimo", "Canada"],
    ["Peterhead", "Scotland"],
    ["Polevskoy", "Russia"],
    ["Round Rock", "USA"],
    ["Seoul", "South Korea"],
    ["Solihull", "England"],
    ["Tel Aviv", "Israel"],
]

loc_03 = [
    ["Bengaluru", "India"],
    ["Glasgow", "Scotland"],
    ["Gumi", "South Korea"],
    ["Lagos", "Nigeria"],
    ["Nanaimo", "Canada"],
    ["Niskayuna", "New York"],
    ["Nizhny Novgorod", "Russia"],
    ["Olongapo", "Phillipines"],
    ["Peshawar", "Pakistan"],
    ["Peterhead", "Scotland"],
    ["Quito", "Equador"],
    ["Simmern", "Germany"],
    ["Tainan", "Taiwan"],
    ["Tbilisi", "Georgia"],
    ["Vinh Long", "Vietnam"],
    ["Xi'an, China", "China"],
]

loc_04 = [
    ["Guilin", "China"],
    ["Dissen", "Germany"],
    ["Guatemala City", "Guatemala"],
    ["Kandukur", "India"],
    ["Nanaimo", "British Columbia"],
    ["Uijeongbu-si", "South Korea"],
    ["Yangon", "Myanmar"],
    ["Jalpa de Mendez", "Mexico"],
    ["Enugu", "Nigeria"],
    ["Peterhead", "Scotland"],
    ["Lima", "Peru"],
    ["Singapore", "Singapore"],
    ["Kaohsiung", "Taiwan"],
    ["Grimesland", "North Carolina"],
    ["Visalia", "California"],
    ["Colonia del Sacramento", "Uruguay"],
]


"""
try:
    out = open("weather_01.out", "w", newline="")
except:
    print('Unable to open "weather_01.out" for writing')
    sys.exit(0)
writer = csv.writer(out)

writer.writerow(
    [
        "City",
        "Min 1",
        "Max 1",
        "Min 2",
        "Max 2",
        "Min 3",
        "Max 3",
        "Min 4",
        "Max 4",
        "Min 5",
        "Max 5",
        "Min Avg",
        "Max Avg",
    ]
)

for city in loc_01:
    min_v, max_v = get_min_max(city[0], city[1], "units=metric")

    row = [city[0] + ", " + city[1]]
    for i in range(0, 5):
        min_temp = f"{min_v[ i ]:.02f}"
        max_temp = f"{max_v[ i ]:.02f}"
        row = row + [min_temp, max_temp]

    writer.writerow(row)

out.close()

try:
    out = open("weather_02.out", "w", newline="")
except:
    print('Unable to open "weather_02.out" for writing')
    sys.exit(0)

writer = csv.writer(out)
writer.writerow(
    [
        "City",
        "Min 1",
        "Max 1",
        "Min 2",
        "Max 2",
        "Min 3",
        "Max 3",
        "Min 4",
        "Max 4",
        "Min 5",
        "Max 5",
        "Min Avg",
        "Max Avg",
    ]
)

for city in loc_02:
    min_v, max_v = get_min_max(city[0], city[1])

    row = [city[0] + ", " + city[1]]
    for i in range(0, 5):
        min_temp = f"{min_v[ i ]:.02f}"
        max_temp = f"{max_v[ i ]:.02f}"
        row = row + [min_temp, max_temp]

    writer.writerow(row)

out.close()

try:
    out = open("weather_03.out", "w", newline="")
except:
    print('Unable to open "weather_03.out" for writing')
    sys.exit(0)
writer = csv.writer(out)

writer.writerow(
    [
        "City",
        "Min 1",
        "Max 1",
        "Min 2",
        "Max 2",
        "Min 3",
        "Max 3",
        "Min 4",
        "Max 4",
        "Min 5",
        "Max 5",
        "Min Avg",
        "Max Avg",
    ]
)
"""

try:
    out = open("temp.csv", "w", newline="")
except:
    print('Unable to open "temp.csv" for writing')
    sys.exit(0)
writer = csv.writer(out)

writer.writerow(
    [
        "City",
        "Min 1",
        "Max 1",
        "Min 2",
        "Max 2",
        "Min 3",
        "Max 3",
        "Min 4",
        "Max 4",
        "Min 5",
        "Max 5",
        "Min Avg",
        "Max Avg",
    ]
)
for city in loc_04:
    min_v, max_v = get_min_max(city[0], city[1], "units=metric")

    row = [city[0] + ", " + city[1]]
    for i in range(0, 5):
        min_temp = f"{min_v[ i ]:.02f}"
        max_temp = f"{max_v[ i ]:.02f}"
        row = row + [min_temp, max_temp]

    writer.writerow(row)

out.close()

#  End mainline
