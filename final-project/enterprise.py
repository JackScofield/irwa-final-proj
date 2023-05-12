from datetime import datetime
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

url = "https://www.enterprise.com/en/home.html"


def get_results_from_enterprise(pickup_location, return_location, age, pickup_date, pickup_time, return_date,
                                return_time):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    # driver.maximize_window()
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    time.sleep(2)
    return_the_same_place = False
    if pickup_location == return_location:
        return_the_same_place = True

    # By default, return location and pick up location are the same
    # This is mainly for airport locations
    # Input the pickup and return location
    if not return_the_same_place:
        same_location = driver.find_element(By.NAME, 'sameLocation')
        same_location.click()

        driver.find_element(By.ID, 'dropoffLocationTextBox').send_keys(return_location)

        first_airport_entry = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".location-group:nth-child(2) .location-group__item:first-child"))
        )
        time.sleep(0.2)
        first_airport_entry.click()

    driver.find_element(By.ID, 'pickupLocationTextBox').send_keys(pickup_location)
    first_airport_entry = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".location-group:nth-child(2) .location-group__item:first-child"))
    )
    time.sleep(0.2)
    first_airport_entry.click()

    time.sleep(3)
    # Input the pickup and return date
    pickup_date_button = wait.until(
        EC.presence_of_element_located((By.ID, "pickupCalendarFocusable"))
    )

    pickup_year, pickup_month, pickup_day = pickup_date.split("-")
    return_year, return_month, return_day = return_date.split("-")

    month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

    driver.execute_script("window.scrollTo(0, 250)", "")
    # Click the pickup date button to show up the calendar
    pickup_date_button.click()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rs-calendar")))

    calenders = driver.find_elements(By.CLASS_NAME, "rs-calendar")
    count = 0
    for calender in calenders:
        count +=1
        calender_control = calender.find_element(By.CLASS_NAME, "calendar-controls")
        if month_name[int(pickup_month) - 1] in calender_control.text:
            break
        else:
            if count == 2:
                button = calender.find_element(By.CSS_SELECTOR, 'button[aria-label="Next Month"]')
                button.click()
            else:
                continue

    element_xpath = f"//button[contains(@class, 'rs-calendar__day') and .//*[contains(text(), '{pickup_day}')]]"


    element = wait.until(
        EC.element_to_be_clickable((By.XPATH, element_xpath))
    )
    element.click()

    # Click the pickup date button to show up the calendar
    date_obj = datetime.strptime(return_date, "%Y-%m-%d")

    # Convert the datetime object to the desired format
    formatted_date = date_obj.strftime("%m/%d/%Y")
    dropoff_date_button = wait.until(
        EC.presence_of_element_located((By.ID, "dropoffCalendarFocusable"))
    )
    dropoff_date_button.click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rs-date-time--dropoff-calendar")))

    element_selector = f'button[data-test-id="{formatted_date}"]'

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, element_selector))
    )

    # Click the element
    element.click()

    time.sleep(2)

    # click the search botton
    driver.find_element(By.CLASS_NAME, "booking-submit").click()

    time.sleep(10)
    html_content = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    vehicle_list = soup.find('ul', class_='vehicle-list')
    vehicles = vehicle_list.find_all('li', class_='vehicle-list__item')
    print("Number of vehicles:", len(vehicles))
    res = []
    for vehicle in vehicles:
        car_info = {}
        # Extract the car model
        car_model = vehicle.find('p', class_='vehicle-item__models').text.strip()

        # Extract the total price
        total_price = vehicle.find('div', class_='price-tile').find_next('div', class_='price-tile').find('span',
                                                                                                          class_='price-tile__amount').text.strip()
        car_info["model"] = car_model
        car_info["price_total"] = total_price
        res.append(car_info)

    time.sleep(2)

    driver.quit()
    return res


# get_results_from_enterprise("LAX", "LAX", 25, "2023-07-13", "10:00", "2023-07-30", "10:00")