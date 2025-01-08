from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login(username, password, url):
    driver = webdriver.Firefox()
    driver.get(url)

    time.sleep(3)  # Wait for the page to load

    username_field = driver.find_element(By.NAME, 'username')
    password_field = driver.find_element(By.NAME, 'password')
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    username_field.send_keys(username)
    time.sleep(2)
    password_field.send_keys(password)
    time.sleep(2)

    login_button.click()
    time.sleep(15)  # Wait for the login to complete

    return driver