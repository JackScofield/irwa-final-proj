import time
from seleniumwire import webdriver

from selenium.webdriver.common.by import By
api_key = '7a3185df3ba004c59c7c43945cd988c7'
url = 'https://hertz.com'

# Configure Selenium Wire to use ScraperAPI as a proxy
options = {
    'proxy': {
        # http://scraperapi:7a3185df3ba004c59c7c43945cd988c7@proxy-server.scraperapi.com:8001
        'http': f'http://scraperapi:{api_key}@proxy-server.scraperapi.com:8001',
    }
}

# Initialize the WebDriver with the custom options
driver = webdriver.Chrome(seleniumwire_options=options)

# Navigate to the target URL
driver.get(url)
time.sleep(10)
# Interact with the web page using Selenium as you normally would
# Example: Find an element by its ID
# element = driver.find_element(By.ID, 'example-id')

# Don't forget to close the browser when you're done
driver.quit()
print("success")
