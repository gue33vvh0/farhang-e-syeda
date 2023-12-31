import random
import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os

# Session cookie value
session_cookie = "s8h4k1hb6rij2l9rgn6cui21j6"

# Start and end words for the loop
start_word = 37645
end_word = 263454

# Random jitter duration range in seconds
jitter_min = 3  # 3 seconds
jitter_max = 15  # 15 seconds

# Initialize the Chrome browser
driver = webdriver.Chrome()

# Set the session cookie
driver.get("http://udb.gov.pk/result_details.php?word={}".format(start_word))
driver.add_cookie({"name": "PHPSESSID", "value": session_cookie})

# Initialize the last_word variable to start_word
last_word = start_word

# Initialize last execution timestamp for the apology_element block
last_execution_timestamp = 1693144777.8785644

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

            # Update timestamp within try loop, within for loop, within try loop - lol
            current_datetime = datetime.datetime.now()
            timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Get the page source
            page_source = driver.page_source

            # Use BeautifulSoup to extract the specific fields
            soup = BeautifulSoup(page_source, 'html.parser')

            apology_element = soup.find('h1', string='很抱歉')
            if apology_element:
                print("Captcha is required. Updating the 'session_cookie' variable.", timestamp)
                session_cookie_path = "/home/ak92/Desktop/temp_lughat_project/farhang-e-syeda-bot/farhang_e_syeda_bot/php_session_id.txt"
                if os.path.exists(session_cookie_path):
                    file_timestamp = os.path.getmtime(session_cookie_path)
                    if last_execution_timestamp is not None and last_execution_timestamp == file_timestamp:
                        wait_time = 10800
                        print(f"Waiting for {wait_time/60:.2f} minutes before proceeding...", timestamp)
                        time.sleep(wait_time)

                    # Update the last execution timestamp
                    last_execution_timestamp = file_timestamp

                    with open(session_cookie_path, "r") as session_file:
                        session_cookie = session_file.read().strip()
                        print("Updated, new session cookie is:", session_cookie)
                        driver.quit()
                        # Initialize the Chrome browser with the updated session_cookie
                        driver = webdriver.Chrome()
                        driver.get("http://udb.gov.pk/result_details.php?word={}".format(last_word))
                        driver.add_cookie({"name": "PHPSESSID", "value": session_cookie})
                        continue
                else:
                    print("php_session_id.txt file not found.", timestamp)


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


            print(f"Word {word} data saved.", timestamp)

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
            print(f"Error occurred for word {word}: {e}", timestamp)
            print("Pausing for 3 hours and continuing...", timestamp)
            time.sleep(10800)

except KeyboardInterrupt:
    print("Keyboard interrupt received. Saving fetched data to words_data.json...", timestamp)

finally:
    # Close all tabs and the browser
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        driver.close()

    driver.quit()

    print("All words' data fetched and saved to their respective json files.", timestamp)
