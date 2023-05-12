import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://www.hertz.com/rentacar/reservation/'

def get_results_from_hertz(pickup_location, return_location, age, pickup_date, pickup_time, return_date, return_time):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
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
        # Find the <select> element by its ID using the By class
        location_select = driver.find_element(By.ID, 'new-locSelect')

        # Create a Select object
        select = Select(location_select)

        # Select the "Different Drop-off Location" option by its value
        select.select_by_value('diffRL')

        time.sleep(3)
        driver.find_element(By.ID, 'dropoff-location').send_keys(return_location)

        # Find the label with the text "Airport Locations"
        airport_locations_label = driver.find_element(By.XPATH, '//label[contains(text(), "Airport Locations")]')

        first_airport_entry = airport_locations_label.find_element(By.XPATH,
                                                                   './following-sibling::div[contains(@class, '
                                                                   '"ww-item")]/div[contains(@class, "ww-name")]')
        first_airport_entry.click()

    driver.find_element(By.ID, 'pickup-location').send_keys(pickup_location)

    # Wait for the label with the text "Airport Locations" to be present and find it
    airport_locations_label = wait.until(
        EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "Airport Locations")]')))

    # Find the first ww-item div element after the label and then find the ww-name div within it
    first_airport_entry = airport_locations_label.find_element(By.XPATH,
                                                               './following-sibling::div[contains(@class, "ww-item")]/div[contains(@class, "ww-name")]')
    time.sleep(1.5)

    first_airport_entry.click()
    time.sleep(2)

    pickup_year, pickup_month, pickup_day = pickup_date.split("-")
    return_year, return_month, return_day = return_date.split("-")

    month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    # Input the pickup and return time
    driver.find_element(By.ID, 'pickup-date-box').click()
    time.sleep(0.5)
    # 2023-05-10

    # Click the next arrow until the correct month is displayed
    while True:
        calendar_month_element = driver.find_element(By.XPATH, '//table[contains(@class, "body")]/../..//header/h1')
        if f'{month_name[int(pickup_month) - 1]} {pickup_date.split("-")[0]}' in calendar_month_element.text:
            break
        next_arrows = driver.find_elements(By.XPATH, '//span[@class="next arrow"]/span')

        # Find the intractable next arrow and click it
        for arrow in next_arrows:
            if arrow.is_displayed():
                arrow.click()
                break

    # Find and click the date element
    date_element = driver.find_element(By.XPATH, f'//table[contains(@class, "body")]//td[text()="{int(pickup_day)}"]')
    date_element.click()

    time.sleep(1)

    driver.find_element(By.ID, 'dropoff-date-box').click()
    time.sleep(0.5)
    # Click the next arrow until the correct month is displayed
    while True:
        calendar_month_element = driver.find_element(By.XPATH, '//table[contains(@class, "body")]/../..//header/h1')
        if f'{month_name[int(return_month) - 1]} {return_date.split("-")[0]}' in calendar_month_element.text:
            break
        next_arrows = driver.find_elements(By.XPATH, '//span[@class="next arrow"]/span')

        # Find the intractable next arrow and click it
        for arrow in next_arrows:
            if arrow.is_displayed():
                arrow.click()
                break

    # Find and click the date element
    date_element = driver.find_element(By.XPATH, f'//table[contains(@class, "body")]//td[text()="{int(return_day)}"]')
    date_element.click()


    # Input the pickup and return time
    if len(pickup_time) == 4:
        pickup_time = "0" + pickup_time
    if len(return_time) == 4:
        return_time = "0" + return_time

    pickup_time_dropdown = driver.find_element(By.NAME, 'pickupTime')
    select = Select(pickup_time_dropdown)
    select.select_by_value(pickup_time)

    time.sleep(0.5)
    dropoff_time_dropdown = driver.find_element(By.NAME, 'dropoffTime')
    select = Select(dropoff_time_dropdown)
    select.select_by_value(return_time)


    # submit my search
    driver.find_element(By.CLASS_NAME,'res-submit').click()

    time.sleep(10)

    vehicle_grid_element = wait.until(
        EC.presence_of_element_located((By.ID, 'gtm-vehicle-grid'))
    )
    vehicle_grid_html = vehicle_grid_element.get_attribute('outerHTML')
    soup = BeautifulSoup(vehicle_grid_html, 'html.parser')

    vehicle_grid = soup.find('div', {'id': 'gtm-vehicle-grid'})

    car_info_list = []

    for vehicle in vehicle_grid.findAll('div', {'class': 'gtm-vehicle'}):
        car_info = {}
        car_info['model'] = vehicle.find('div', {'class': 'gtm-vehicle-type'}).text.strip()

        number_pattern = re.compile(r"(\d+\.\d+)")
        match = number_pattern.search(vehicle.find('div', {'class': 'gtm-total'}).text.strip())

        if match:
            number = match.group(1)
            car_info['price_total'] = number
        else:
            continue
        car_info_list.append(car_info)

    # car_info_res = []
    # for car_info in car_info_list:
    #     if car_info['price_total'] != '':
    #         car_info_res.append(car_info)
    driver.quit()

    for car in car_info_list:
        print(car)
    return car_info_list


# get_results_from_hertz("LAX", "LAX", 25, "2023-06-15", "14:00", "2023-06-20", "14:30")