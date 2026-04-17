import json
import time
import sys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

def send_discord_message(webhook_url, message):
    data = {"content": message}
    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"Failed to send Discord message: {e}")

# Load the configuration file
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("ERROR: Could not find config.json!")
    sys.exit()

settings = config['search_settings']
locators = config['website_locators']
discord = config['discord_settings']

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--window-size=1920,1080")

print("Bot started! Running in visible mode (Minimize it now!)...")

while True:
    driver = webdriver.Chrome(options=chrome_options)
    print(f"\n[{time.strftime('%H:%M:%S')}] Checking availability...")
    found = False

    try:
        driver.get("https://reservations.ahlsmsworld.com/Yosemite/Plan-Your-Trip/")
        wait = WebDriverWait(driver, 15)

        # Set Dropdowns
        lodge_drop = wait.until(EC.presence_of_element_located((By.ID, locators['dropdown_lodge_id'])))
        driver.execute_script(f"arguments[0].value = '{settings['lodging_type']}'; arguments[0].dispatchEvent(new Event('change'));", lodge_drop)

        rooms_drop = driver.find_element(By.ID, locators['dropdown_rooms_id'])
        driver.execute_script(f"arguments[0].value = '{settings['rooms']}'; arguments[0].dispatchEvent(new Event('change'));", rooms_drop)

        adults_drop = driver.find_element(By.ID, locators['dropdown_adults_id'])
        driver.execute_script(f"arguments[0].value = '{settings['adults']}'; arguments[0].dispatchEvent(new Event('change'));", adults_drop)

        # Type Dates
        checkin_box = wait.until(EC.element_to_be_clickable((By.ID, locators['input_checkin_id'])))
        checkin_box.clear()
        checkin_box.send_keys(settings['checkin_date'])

        checkout_box = driver.find_element(By.ID, locators['input_checkout_id'])
        checkout_box.clear()
        checkout_box.send_keys(settings['checkout_date'])
        
        time.sleep(1)
        checkout_box.send_keys(Keys.ESCAPE)
        time.sleep(1)
        checkout_box.send_keys(Keys.ENTER)

        # Results Check
        wait.until(EC.url_contains("Results"))
        time.sleep(4)
        
        if "We couldn't find any results for your search!" in driver.page_source:
            print("Status: No availability found.")
        else:
            print("Status: RESERVATION FOUND!")
            found = True
            msg = f"🌲 **Yosemite Alert!** 🌲\nRooms found for {settings['checkin_date']}! The browser is open and waiting for you."
            send_discord_message(discord['webhook_url'], msg)
            
    except Exception as e:
        print(f"An error occurred during this check: {e}")

    # FINAL LOGIC: Decide whether to kill the browser or keep it open
    if found:
        print("Stopping loop. Take over the browser window now!")
        break 
    else:
        driver.quit() # Ensures the window closes even if an error happened
        print(f"Waiting {discord['check_interval_minutes']} minutes for the next check...")
        time.sleep(discord['check_interval_minutes'] * 60)