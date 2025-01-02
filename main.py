import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
from PIL import Image
from datetime import datetime
import pytesseract

# Load environment variables
load_dotenv()


# Ensure the 'logs' directory exists
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Generate a timestamp-based filename in the format '%Y-%m-%d_%H:%M:%S'
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file = os.path.join(log_dir, f"{timestamp}.log")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize WebDriver
logging.info("Initializing WebDriver for Chrome")
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Test Case 1: Open IRCTC homepage
    logging.info("Opening IRCTC homepage")
    driver.get("https://www.irctc.co.in/nget/train-search")
    logging.info("Test Case 1 Passed")

    # Test Case 2: Login Process
    logging.info("Clicking on Login Button")
    login_button = driver.find_element(By.CLASS_NAME, 'search_btn')
    login_button.click()
    logging.info("Clicked on Login Button")

    # waiting for pop-up login window
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="login_header_disable"]/div/div/div[2]'))  
    )

    # Entering username
    logging.info("Locating and entering username")
    time.sleep(2)  # Wait for modal to appear
    user_input = driver.find_element(By.CSS_SELECTOR, '[formcontrolname="userid"]')
    user_input.send_keys(os.getenv("USER_NAME"))
    logging.info("Entered username")

    # Entering password
    logging.info("Locating and entering password")
    time.sleep(2)  # Ensure field is interactable
    password_input = driver.find_element(By.CSS_SELECTOR, '[placeholder="Password"]')
    password_input.send_keys(os.getenv("PASSWORD"))
    logging.info("Entered password")

    # Optional: Handle CAPTCHA here if needed
    logging.info("Finding the captcha code and storing in png file")
    captcha_element = driver.find_element(By.CLASS_NAME, 'captcha-img')
    logging.info("extracting the captcha code and saving in png file")
    captcha_image_path = "captcha.png"
    captcha_element.screenshot(captcha_image_path)
    logging.info("extracting the captcha code text")
    captcha_image = Image.open("captcha.png")
    captcha_text = pytesseract.image_to_string(captcha_image)
    logging.info("extracted the captcha code text")
    print(captcha_text)

    # Entering the Captcha code
    logging.info("Locating and entering Captcha") 
    captcha_input = driver.find_element(By.CSS_SELECTOR, '[formcontrolname="captcha"]')  # Replace with the correct ID or selector for the username input
    captcha_input.send_keys(captcha_text)
    logging.info("Entered Captcha")

    time.sleep(3)
    # submiting the Login Information
    submit = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
    submit.click()
    logging.info("Login Successfully !")
    logging.info("Test Case 2 Passed")

    # Test Case 3: Entering the form details
    logging.info("Enter the source ")
    source_input = driver.find_element(By.XPATH,'//*[@id="origin"]/span/input')
    source_input.send_keys(os.getenv("FROM"))
    clickable_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@class, 'ui-autocomplete-list-item') and contains(., 'LOKMANYATILAK T')]")
        )
    )
    clickable_element.click()
    logging.info("Entered Source")
    # .ng-tns-c57-8.ui-inputtext.ui-widget.ui-state-default.ui-corner-all.ui-autocomplete-input.ng-star-inserted

    # Entering the Destination
    logging.info("Enter the Destination ")
    destination_input = driver.find_element(By.XPATH,'//*[@id="destination"]/span/input')
    destination_input.send_keys(os.getenv("TO"))
    # Wait for the element to be clickable
    clickable_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@class, 'ui-autocomplete-list-item') and contains(., 'MIRZAPUR')]")
        )
    )
    clickable_element.click()
    logging.info("Entered Destination")

    time.sleep(3)
    # entering the date of journey
    logging.info("Entering the date")
    date_of_journey = driver.find_element(By.XPATH, '//*[@id="jDate"]/span/input')
    date_of_journey.click()
    date_selected = driver.find_element(By.XPATH,'//*[@id="jDate"]/span/div/div/div[2]/table/tbody/tr[1]/td[7]/a')
    date_selected.click()
    logging.info("Entered the date")
    time.sleep(3)
    # Entering the Class
    logging.info("Selecting the Class")
    class_of_journey = driver.find_element(By.XPATH, '//*[@id="journeyClass"]/div/div[2]/span')
    class_of_journey.click()
    class_selected = driver.find_element(By.XPATH,'//*[@id="journeyClass"]/div/div[4]/div/ul/p-dropdownitem[3]/li')
    class_selected.click()
    logging.info("Entered the Class")

    # Checking the railway consession check-box
    check_box = driver.find_element(By.CSS_SELECTOR, '[for="passBooking"]')
    check_box.click()
    logging.info("Clicked Checkbox")  

    # waiting for pop-up for check-box window
    logging.info("trying for closing popup window by ok")
    press_ok = driver.find_element(By.CLASS_NAME, "ui-button-text")
    press_ok.click()
    logging.info("closed popups")

    # Searching Train 
    button = driver.find_element(By.XPATH, "//button[@label='Find Trains' and @type='submit']")
    button.click()
    time.sleep(3)

    logging.info("Test Cases 3 passed")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    # Close the browser
    time.sleep(5)
    logging.info("Closing the browser")
    logging.info("-----------------------------$-------------------------$------------------------------------------")
    
    driver.quit()
# .ng-tns-c58-10.ui-inputtext.ui-widget.ui-state-default.ui-corner-all.ng-star-inserted