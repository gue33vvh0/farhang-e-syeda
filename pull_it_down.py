import random
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import json

# Session cookie value
session_cookie = "dpui00sdvfusf3ieutm66judq0"

# Start and end words for the loop
start_word = 3320
end_word = 263454

# Random jitter duration range in seconds
jitter_min = 60  # 1 minutes
jitter_max = 180  # 3 minutes

# Initialize the Chrome browser
driver = webdriver.Chrome()

# Set the session cookie
driver.get("http://udb.gov.pk/result_details.php?word={}".format(start_word))
driver.add_cookie({"name": "PHPSESSID", "value": session_cookie})

# Initialize the last_word variable to start_word
last_word = start_word

try:
    # Loop from start_word to end_word
    for word in range(start_word, end_word + 1):
        try:
            # Open the webpage for the current word in a new tab
            driver.execute_script("window.open('http://udb.gov.pk/result_details.php?word={}', '_blank');".format(word))

            # Wait for the new tab to load completely
            time.sleep(2)

            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])

            # Get the page source
            page_source = driver.page_source

            # Use BeautifulSoup to extract the specific fields
            soup = BeautifulSoup(page_source, 'html.parser')

            apology_element = soup.find('h1', string='很抱歉')
            if apology_element:
                print("Captcha is likely required. Please update the 'session_cookie' variable with a valid session cookie.")
                session_cookie = input("Enter the updated 'session_cookie' value: ")
                driver.quit()
                # Initialize the Chrome browser with the updated session_cookie
                driver = webdriver.Chrome()
                driver.get("http://udb.gov.pk/result_details.php?word={}".format(last_word))
                driver.add_cookie({"name": "PHPSESSID", "value": session_cookie})
                continue


            # find the word
            xpaths = [
                "/html/body/div[3]/div[1]/h1",
                "/html/body/div[2]/div[1]/h1/text()",
                "/html/body/div[2]/div[1]/h1"
            ]

            field1_element = None
            for xpath in xpaths:
                try:
                    field1_element = driver.find_element("xpath", xpath)
                    break  # Exit the loop if the element is found
                except:
                    pass  # Continue to the next XPath
                
            if field1_element:
                field1 = field1_element.get_attribute("outerHTML")
            else:
                print("Word element not found.")


            # find all the definitions
            gold_color_elements = soup.find_all('b', class_='gold_color')
            field2 = " / ".join(element.text.strip() for element in gold_color_elements)
            
            

            # Create a dictionary for the current word data
            word_data = {
                "word": field1,
                "meaning": field2,
                "source": "udb.gov.pk"
            }

            # Save the data to a JSON file for the current word
            with open(f"word_{word}_data.json", "w", encoding="utf-8") as json_file:
                json.dump(word_data, json_file, ensure_ascii=False, indent=4)


            print(f"Word {word} data saved.")

            # Close the previous word's tab
            if word != start_word:
                driver.switch_to.window(driver.window_handles[0])
                driver.close()

            # Switch back to the new tab for the next iteration
            driver.switch_to.window(driver.window_handles[-1])

            # Random jitter before proceeding to the next word
            jitter_duration = random.randint(jitter_min, jitter_max)
            time.sleep(jitter_duration)

            # Update the last_word variable after successful iteration
            last_word = word

        except Exception as e:
            print(f"Error occurred for word {word}: {e}")
            print("Pausing for 5 seconds and continuing...")
            time.sleep(5)

except KeyboardInterrupt:
    print("Keyboard interrupt received. Saving fetched data to words_data.json...")

finally:
    # Close all tabs and the browser
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        driver.close()

    driver.quit()

    print("All words' data fetched and saved to their respective json files.")
