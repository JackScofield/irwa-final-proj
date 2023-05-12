import time
import re
from flask import jsonify
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

cities_airports_dict = {
    "New York": "JFK",
    "Los Angeles": "LAX",
    "Chicago": "ORD",
    "Houston": "IAH",
    "Phoenix": "PHX",
    "Philadelphia": "PHL",
    "San Antonio": "SAT",
    "San Diego": "SAN",
    "Dallas": "DFW",
    "San Jose": "SJC",
    "Austin": "AUS",
    "Jacksonville": "JAX",
    "Fort Worth": "DFW",
    "Columbus": "CMH",
    "Charlotte": "CLT",
    "San Francisco": "SFO",
    "Indianapolis": "IND",
    "Seattle": "SEA",
    "Denver": "DEN",
    "Washington": "DCA",
    "Boston": "BOS",
    "El Paso": "ELP",
    "Nashville": "BNA",
    "Detroit": "DTW",
    "Oklahoma City": "OKC",
    "Portland": "PDX",
    "Las Vegas": "LAS",
    "Memphis": "MEM",
    "Louisville": "SDF",
    "Baltimore": "BWI",
    "Milwaukee": "MKE",
    "Albuquerque": "ABQ",
    "Tucson": "TUS",
    "Fresno": "FAT",
    "Sacramento": "SMF",
    "Mesa": "PHX",  # Mesa is served by Phoenix Sky Harbor International Airport
    "Kansas City": "MCI",
    "Atlanta": "ATL",
    "Long Beach": "LGB",
    "Omaha": "OMA",
    "Raleigh": "RDU",
    "Colorado Springs": "COS",
    "Miami": "MIA",
    "Oakland": "OAK",
    "Minneapolis": "MSP",
    "Arlington": "DFW",  # Arlington is served by Dallas/Fort Worth International Airport
    "Tampa": "TPA",
    "Tulsa": "TUL",
    "New Orleans": "MSY"
}

CLIENT_ID = "f5efa63a"
CLIENT_SECRET = "27bf434eae2ffa30c7516b5ed5b0c429"
api_url = "https://stage.abgapiservices.com/cars/locations"


def get_token():
    url = 'https://stage.abgapiservices.com/oauth/token/v1'
    headers = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        token = response.json().get('access_token')
        return token
    else:
        return 'Failed to get token', 400


def get_vehicles(token, pickup_location_airport, return_location_airport, pickup_date, return_date):
    url = 'https://stage.abgapiservices.com:443/cars/catalog/v1/vehicles'

    params = {
        'country_code': 'US',
        'brand': 'Avis',
        'pickup_location': pickup_location_airport,
        'dropoff_location': return_location_airport,
        'pickup_date': pickup_date,
        'dropoff_date': return_date,
    }
    headers = {
        'client_id': CLIENT_ID,
        'authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 400:
        return response.json()['vehicles']
    else:
        return response.json()


def get_price_rate(age, token, vehicle_class_code, rate_code, pickup_location_airport, return_location_airport,
                   pickup_date_time, return_date_time):
    url = 'https://stage.abgapiservices.com:443/cars/catalog/v1/vehicles/rates'

    if age == '25+':
        age = 25
    elif age == '20-24':
        age = 22
    else:
        age = 19
    params = {
        'age': age,
        'country_code': 'US',
        'brand': 'Avis',
        'pickup_location': pickup_location_airport,
        'dropoff_location': return_location_airport,
        'pickup_date': pickup_date_time,
        'dropoff_date': return_date_time,
        'vehicle_class_code': vehicle_class_code,
        'rate_code': rate_code
    }
    headers = {
        'client_id': CLIENT_ID,
        'authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 400:
        return response.json()['reservation']['rate_totals']['totals']['vehicle_total']
    else:
        return response.json()


def get_results_from_avis(pickup_location, return_location, age, pickup_date, pickup_time, return_date, return_time):
    if len(pickup_time) == 4:
        pickup_time = '0' + pickup_time
    if len(return_time) == 4:
        return_time = '0' + return_time

    if pickup_location in cities_airports_dict:
        pickup_location_airport = cities_airports_dict[pickup_location]
    else:
        pickup_location_airport = pickup_location
    if return_location in cities_airports_dict:
        return_location_airport = cities_airports_dict[return_location]
    else:
        return_location_airport = return_location

    pickup_date_time = pickup_date + 'T' + pickup_time + ':00'
    return_date_time = return_date + 'T' + return_time + ':00'

    token = get_token()
    vehicles = get_vehicles(token, pickup_location_airport, return_location_airport, pickup_date_time, return_date_time)
    car_info_list = []
    for vehicle in vehicles:
        car_info = {}
        car_info['model'] = vehicle['category']['name'][10:]
        vehicle_class_code = vehicle['category']['vehicle_class_code']
        rate_code = vehicle['rate_totals']['rate']['rate_code']
        car_info['price_total'] = get_price_rate(age, token, vehicle_class_code, rate_code, pickup_location_airport,
                                                 return_location_airport, pickup_date_time, return_date_time)

        car_info_list.append(car_info)

        print(car_info)

    return car_info_list

# get_results_from_avis('Denver', 'Denver', 25, '2023-05-15','9:00', '2023-05-20','9:00')
