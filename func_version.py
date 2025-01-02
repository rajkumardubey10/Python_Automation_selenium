import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import time
from PIL import Image
from datetime import datetime
import pytesseract

# Load environment variables
load_dotenv()

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
# chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional, for older systems)
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (useful in Docker)
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--window-size=1920,1080")  # Set a default window size

# Ensure the 'logs' directory exists
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Generate a timestamp-based filename
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file = os.path.join(log_dir, f"{timestamp}.log")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def initialize_driver():
    logging.info("Initializing WebDriver for Chrome")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def open_homepage(driver):
    try:
        logging.info("Opening IRCTC homepage")
        driver.get("https://www.irctc.co.in/nget/train-search")
        logging.info("Homepage opened successfully")
        logging.info("Test Case 1 Passed")
    except Exception as e:
        logging.error(f"Error opening homepage: {e}")
        raise

def login(driver):
    try:
        # logging.info("Clicking on Login Button")
        # login_button = driver.find_element(By.CLASS_NAME, 'search_btn')
        # login_button.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login_header_disable"]/div/div/div[2]'))
        )

        logging.info("Entering username")
        time.sleep(2)
        user_input = driver.find_element(By.CSS_SELECTOR, '[formcontrolname="userid"]')
        user_input.send_keys(os.getenv("USER_NAME"))
        logging.info("Entered username")

        logging.info("Entering password")
        time.sleep(2)
        password_input = driver.find_element(By.CSS_SELECTOR, '[placeholder="Password"]')
        password_input.send_keys(os.getenv("PASSWORD"))
        logging.info("Entered password")

        logging.info("Handling CAPTCHA")
        captcha_element = driver.find_element(By.CLASS_NAME, 'captcha-img')
        captcha_image_path = "captcha.png"
        captcha_element.screenshot(captcha_image_path)

        captcha_image = Image.open("captcha.png")
        captcha_text = pytesseract.image_to_string(captcha_image).strip()
        logging.info(f"Extracted CAPTCHA text: {captcha_text}")
        print(captcha_text)

        logging.info("Locating and entering Captcha")
        captcha_input = driver.find_element(By.CSS_SELECTOR, '[formcontrolname="captcha"]')
        captcha_input.send_keys(captcha_text)
        # captcha_input.submit()
        logging.info("Entered Captcha")

        time.sleep(3)
            # WebDriverWait(driver, 10).until(
        #     EC.invisibility_of_element((By.CLASS_NAME, "ui-dialog-mask"))
        # )
        sign_in_button = driver.find_element(By.XPATH, '//*[@id="login_header_disable"]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/form/span/button')
        sign_in_button.click()
        # form[class='ng-valid ng-touched ng-dirty'] button[type='submit']
        logging.info("Login successful")
        logging.info("Test Case 3 Passed")
    except Exception as e:
        logging.error(f"Error during login: {e}")
        raise

def enter_journey_details(driver):
    try:
        logging.info("Entering source station")
        source_input = driver.find_element(By.XPATH, '//*[@id="origin"]/span/input')
        source_input.send_keys(os.getenv("FROM"))
        clickable_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'ui-autocomplete-list-item') and contains(., 'LOKMANYATILAK T')]")
            )
        )
        clickable_element.click()

        logging.info("Entering destination station")
        destination_input = driver.find_element(By.XPATH, '//*[@id="destination"]/span/input')
        destination_input.send_keys(os.getenv("TO"))
        clickable_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'ui-autocomplete-list-item') and contains(., 'MIRZAPUR')]")
            )
        )
        clickable_element.click()

        logging.info("Entering journey date")
        date_of_journey = driver.find_element(By.XPATH, '//*[@id="jDate"]/span/input')
        date_of_journey.click()
        date_selected = driver.find_element(By.XPATH, '//*[@id="jDate"]/span/div/div/div[2]/table/tbody/tr[2]/td[1]')
        date_selected.click()

        logging.info("Selecting class of journey")
        class_of_journey = driver.find_element(By.XPATH, '//*[@id="journeyClass"]/div/div[2]/span')
        class_of_journey.click()
        class_selected = driver.find_element(By.XPATH, '//*[@id="journeyClass"]/div/div[4]/div/ul/p-dropdownitem[3]/li')
        class_selected.click()

        logging.info("Checking concession checkbox")
        check_box = driver.find_element(By.CSS_SELECTOR, '[for="passBooking"]')
        check_box.click()

        logging.info("Closing concession popup")
        press_ok = driver.find_element(By.CLASS_NAME, "ui-button-text")
        press_ok.click()

        logging.info("Finding trains")
        find_trains_button = driver.find_element(By.XPATH, "//button[@label='Find Trains' and @type='submit']")
        find_trains_button.click()
        logging.info("Test Case 2 passed")
    except Exception as e:
        logging.error(f"Error entering form details: {e}")
        raise

def select_train_and_proceed(driver):
    try:
        logging.info("Selecting train")
        train_name = os.getenv("TRAIN_NAME")
        train_element = driver.find_element(By.XPATH, f"//div[contains(@class, 'train-heading')]//strong[contains(text(), '{train_name}')]")
        highligth = driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", train_element)

        # Highlight the element (optional, for debugging purposes)
        element = driver.execute_script("arguments[0].style.border='3px solid red'", train_element)

        print(f"Found and scrolled to train: {train_element.text}")
        time.sleep(3)  # Pause to observe the result
        logging.info("Find the Train Name")

        logging.info("Refreshing and selecting date")
        refresh = driver.find_element(By.XPATH, '//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[6]/div[1]/app-train-avl-enq/div[1]/div[5]/div[1]/table/tr/td[5]/div/div[2]')
        refresh.click()
        logging.info("refreshing done")
        time.sleep(2)

        # Selecting date for journey
        logging.info("Selecting date for journey")
        select_date = driver.find_element(By.XPATH, '//*[@id="divMain"]/div/app-train-list/div[4]/div/div[5]/div[6]/div[1]/app-train-avl-enq/div[1]/div[7]/div[1]/div[3]/table/tr/td[2]/div')
        select_date.click()
        logging.info("Selected date")

        # pressing book button
        logging.info("pressing book button")
        book_ticket = driver.find_element(By.CSS_SELECTOR, "button[class='btnDefault train_Search ng-star-inserted']").click()
        logging.info("pressed book button")
        logging.info("Test Case 4 passed")
    except Exception as e:
        logging.error(f"Failed to book train: {e}")

def passanger_details(driver):
    try:
        # Test case 5: Entering the Passenger Details

        # Entering passenger details
        logging.info("Entering the passenger name")
        P_name = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Name']")
        P_name.send_keys(os.getenv("P_NAME"))
        # input[placeholder='Name']

        # Entering Age
        time.sleep(2)
        logging.info("Entering Age")
        P_age = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Age']")
        P_age.send_keys(os.getenv("P_AGE"))

        # Selecting Gender
        time.sleep(2)
        logging.info("Selecting Gender")
        P_gender = driver.find_element(By.CSS_SELECTOR, '[formcontrolname="passengerGender"]')
        P_gender.send_keys(os.getenv("P_GENDER"))

        # Selecting Berth preference
        time.sleep(2)
        logging.info("Selecting Berth preference")
        P_preference = driver.find_element(By.CSS_SELECTOR, '[formcontrolname="passengerBerthChoice"]')
        P_preference.send_keys(os.getenv("P_PREFERENCE"))
        

        # Selecting concession
        time.sleep(2)
        logging.info("Selecting concession")
        P_concession = driver.find_element(By.CSS_SELECTOR, '[formcontrolname="passConcessionType"]')
        P_concession.send_keys(os.getenv("P_CONCESSION"))

        # Entering the UPN Number
        time.sleep(2)
        logging.info("Entering the UPN Number")
        P_upn_number = driver.find_element(By.CSS_SELECTOR, '[formcontrolname="passUPN"]')
        P_upn_number.send_keys(os.getenv("P_UPN"))

        # Entering the pass code
        logging.info("Entering the pass code")
        P_code =driver.find_element(By.CSS_SELECTOR, '[formcontrolname="passBookingCode"]')
        P_code.send_keys(os.getenv("P_CODE"))

        # Enabling the AutoUpgradation ticket
        time.sleep(2)
        logging.info("Enabling the AutoUpgradation Ticket")
        autoupgradation = driver.find_element(By.CSS_SELECTOR, "label[for='autoUpgradation']")
        autoupgradation.click()

        # payment mode through
        time.sleep(2)
        logging.info("Payment mode through")
        payment_mode = driver.find_element(By.CSS_SELECTOR, "label[for='2']")
        payment_mode.click()

        # confirm the detail 
        time.sleep(2)
        logging.info("Confirming the Details")
        confirm = driver.find_element(By.XPATH, '//*[@id="psgn-form"]/form/div/div[1]/div[16]/div/button[2]')
        confirm.click()
        logging.info("Test Case 5 passed")
    except Exception as e:
        logging.error(f"Failed to book train: {e}")

def main():
    driver = initialize_driver()
    try:
        open_homepage(driver)
        time.sleep(3)
        enter_journey_details(driver)
        time.sleep(3)
        select_train_and_proceed(driver)
        time.sleep(3)
        login(driver)
        time.sleep(3)
        passanger_details(driver)
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        time.sleep(5)
        logging.info("Closing the browser")
        driver.quit()

if __name__ == "__main__":
    main()
