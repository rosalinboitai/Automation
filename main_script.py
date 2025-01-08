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

    #scrolldown the page
    # driver.execute_script("window.scrollTo(0, 4000);")
    for i in range(0, 4001, 200):  # Scroll in increments of 200 pixels
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.2)
    time.sleep(2)

    # driver.execute_script("window.scrollTo(0, 0);")
    for i in range(4000, -1, -200):  # Scroll back in increments of 200 pixels
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.1)
    time.sleep(2)


    wait = WebDriverWait(driver, 2)
    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element((By.CLASS_NAME, "preloader"))
        )
    except TimeoutException:
        print("Preloader did not disappear in time, continuing...")

    trip_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='tot_opr_trips']")))
    trip_box.click()

    # Optional: wait for the dropdown to become visible
    time.sleep(1)

    action = ActionChains(driver)
    for _ in range(35):
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

    # tot_trips = driver.find_element(By.XPATH,"//div[@id='tot_opr_trips']//span[@class='count'][1]").text.strip()
    # tot_trip_ = int(tot_trips)
    # print("total trips = {}".format(tot_trip_))
    # if total == tot_trip_:
    #     print("test case passed")
    # else:
    #     print("test case failed")

    opt_trips =driver.find_elements(By.XPATH,"//table[@class='table table-striped']//tbody/tr/td[5]")
    total = 0
    for digit in opt_trips:
        text = digit.text.strip()
        try:
            opt_count = int(text)
            total += opt_count
        except ValueError:
            print("could not convert '{}' to an integer !".format(text))
    print("Operated trips= {}".format(total))


    cls_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @data-dismiss='modal']")))
    cls_btn.click()


    # REVENUE COLLECTION
    wait = WebDriverWait(driver, 5)
    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element((By.CLASS_NAME, "preloader"))
        )
    except TimeoutException:
        print("Preloader did not disappear in time, continuing...")

    revenue = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "tot_revenue")))
    driver.execute_script("arguments[0].click();", revenue)

    action = ActionChains(driver)
    for _ in range(35):
        action.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(0.2)

    #TOTAL REVENUE
    tot_rev = driver.find_elements(By.XPATH, "//table[@class='table table-striped']//tbody/tr/td[4]")

    total = 0
    for rev in tot_rev:
        text = rev.text.strip().replace('₹', '').replace(',', '')
        # print("processing:{}".format(text))
        try:
            rev_count = int(text)
            total += rev_count
        except ValueError:
            print("could not convert '{}' to an integer !".format(text))
    print("Total Revenue = {}".format(total))

    dig_rev = driver.find_elements(By.XPATH, "//table[@class= 'table table-striped']//tbody/tr/td[5]")

    total_dig_rev = 0
    for rev in dig_rev:
        text = rev.text.strip().replace('₹', '').replace(',', '')
        # print("processing:{}".format(text))
        try:
            dig_rev_count = int(text)
            total_dig_rev += dig_rev_count
        except ValueError:
            print("could not convert '{}' to an integer !". format(text))
    print("Digital Revenue = {}".format(total_dig_rev))

    cash_rev = driver.find_elements(By.XPATH, "//table[@class = 'table table-striped']//tbody/tr/td[6]")

    total_cash_rev = 0
    for rev in cash_rev:
        text = rev.text.strip().replace('₹', '').replace(',', '')
        # print("processing:{}".format(text))
        try:
            cash_rev_count = int(text)
            total_cash_rev += cash_rev_count
        except ValueError:
            print("could not convert '{}' to an integer !". format(text))
    print("Cash Revenue = {}".format(total_cash_rev))

    tot_rev = total_dig_rev + total_cash_rev
    print("GRAND TEVENUE ={} + {} = {}".format(total_dig_rev,total_cash_rev, tot_rev))

    clo_btn_rev = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-secondary' and @data-dismiss='modal']")))
    clo_btn_rev.click()

    time.sleep(1)



    wait = WebDriverWait(driver, 2)
    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element((By.CLASS_NAME, "preloader"))
        )
    except TimeoutException:
        print("Preloader did not disappear in time, continuing...")

    passngr_count = driver.find_element(By.XPATH, "//div[@id='passenger_count']//span[@class='count1']")
    passngr_count.click()

    action = ActionChains(driver)
    for _ in range(35):
        action.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(0.2)

    tot_passngr = driver.find_elements(By.XPATH, "//table[@class = 'table table-striped']//tbody/tr/td[4]")
    
    tot_passanger = 0
    for p in tot_passngr:
        text = p.text.strip()

        try:
            tot_pass = int(text)
            tot_passanger += tot_pass
        except ValueError:
            print("could not convert '{}' to an integer !". format(text))
    print("Total passanger = {}".format(tot_passanger))

    cls_btn_pass = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class = 'btn btn-secondary'and @data-dismiss='modal']")))
    cls_btn_pass.click()



    

    try:
        unique_element = driver.find_element(By.XPATH, "//img[@src='https://scdash.ktclitms.com/assets/images/Final-Logo.png' and @alt='Iteration Logo']")
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