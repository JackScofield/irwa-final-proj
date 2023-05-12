from flask import Blueprint, jsonify, request

from avis import get_results_from_avis
from enterprise import get_results_from_enterprise
from hertz import get_results_from_hertz

views = Blueprint("views", __name__)


@views.route("/search", methods=["GET", "POST"])
def crawler():
    data = request.get_json()
    pickup_location = data["pickupLocation"]
    if "returnLocation" in data:
        return_location = data["returnLocation"]
    else:
        return_location = pickup_location

    age = data["age"]
    pickup_date = data["pickupDate"]
    pickup_time = data["pickupTime"]
    return_date = data["returnDate"]
    return_time = data["returnTime"]
    car_companies = data["companies"]

    scraper_result = []
    for company in car_companies:
        if company == "Hertz":
            hertz_res = {"company": "Hertz", "results": get_results_from_hertz(pickup_location, return_location, age, pickup_date, pickup_time, return_date, return_time)}
            scraper_result.append(hertz_res)
        elif company == "Avis & Budget":
            avis_res = {"company": "Avis & Budget", "results": get_results_from_avis(pickup_location, return_location, age, pickup_date, pickup_time, return_date, return_time)}
            scraper_result.append(avis_res)
        else:
            enterprise_res = {"company": "Enterprise", "results": get_results_from_enterprise(pickup_location, return_location, age, pickup_date, pickup_time, return_date, return_time)}
            scraper_result.append(enterprise_res)

    return jsonify(scraper_result)
