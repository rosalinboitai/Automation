from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from selenium.webdriver.common.action_chains import ActionChains
from login import login

def main(from_date, to_date):
    url = "https://scdash.ktclitms.com/auth/login"
    username = 'scadmin'
    password = 'demo123'
    
    # Perform login
    driver = login(username, password, url)

    # ENTER_DATE
    from_date_input = driver.find_element(By.XPATH, "//input[@name='from_date']")
    from_date_input.clear()
    from_date_input.send_keys(from_date)
    time.sleep(2)

    to_date_input = driver.find_element(By.XPATH, "//input[@name='to_date']")
    to_date_input.clear()
    to_date_input.send_keys(to_date)
    time.sleep(2)

    search_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
    search_button.click()

    wait = WebDriverWait(driver, 5)

    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element((By.CLASS_NAME, "preloader"))
        )
    except TimeoutException:
        print("Preloader did not disappear in time, continuing...")

    trip_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='tot_opr_trips']")))
    trip_box.click()

    time.sleep(1)

    action = ActionChains(driver)
    for _ in range(192):
        # action.send_keys(driver.find_element(By.TAG_NAME, 'body'), "\uE013").perform()  # Arrow down key
        action.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(0.1)
    # Locate dropdown items and extract values
    dropdown_items = driver.find_elements(By.XPATH, "//table[@class='table table-striped']//tbody/tr/td[4]")
    total = 0

    for item in dropdown_items:
        # Extract the text, which includes the trip count
        text = item.text.strip()
        # Extract the number from the text (assuming the format "Trip X: Y")
        try:
            trip_count = int(text)  # Convert to integer
            total += trip_count  # Add to total
        except ValueError:
            print(f"Could not convert '{text}' to an integer. Skipping this item.")

    # Print the total trips
    print(f'Total trips: {total}')

    cls_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-secondary' and text()='Close']")))
    cls_btn.click()

    tot_trips = driver.find_element(By.XPATH,"//div[@id='tot_opr_trips']//span[@class='count'][1]").text.strip()
    tot_trip_ = int(tot_trips.replace(',', ''))
    print("total trips = {}".format(tot_trip_))
    if total == tot_trip_:
        print("test case passed")
    else:
        print("test case failed")

    
    try:
        unique_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@src='http://scdash.ktclitms.com/assets/images/Final-Logo.png' and @alt='Iteration Logo']"))
        )
        print("Login successful!")
    except TimeoutException:
        print("Login failed! The Dashboard element was not found.")
    except NoSuchElementException:
        print("Login failed! The Dashboard element does not exist.")



    driver.quit()

if __name__ == "__main__":
    # You can change the dates dynamically here
    from_date = '2024-11-01'
    to_date = '2024-11-04'
    main(from_date, to_date)



