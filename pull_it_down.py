import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Set up Chrome driver
webdriver_service = Service('path/to/chromedriver')  # Replace with the actual path to chromedriver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Starting word
word_id = 32

while True:
    # Generate URL with the current word
    url = f"http://udb.gov.pk/result_details.php?word={word_id}"

    # Open the URL
    driver.get(url)

    # Find the "a_class" and "b_class" elements
    a_class_element = driver.find_element(By.CSS_SELECTOR, ".a_class")
    b_class_element = driver.find_element(By.CSS_SELECTOR, ".b_class")

    # Download the content of "a_class" and "b_class" elements
    a_class_content = a_class_element.get_attribute("innerHTML")
    b_class_content = b_class_element.get_attribute("innerHTML")

    # Print the downloaded content
    print("a_class content:", a_class_content)
    print("b_class content:", b_class_content)

    # Increment word
    word_id += 1

    # Rest for 2 minutes
    time.sleep(120)

# Close the browser
driver.quit()

