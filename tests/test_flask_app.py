from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def test_flask_app():
    # Initialize WebDriver
    driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
    driver.get("http://127.0.0.1:8080")  # Flask app's URL

    # 1. Check page title
    assert "Nifty50 Stocks" in driver.title, "Page title does not match"

    # 2. Test dropdown functionality
    dropdown = driver.find_element(By.ID, "stock-select")
    dropdown.click()

    # Select an option from the dropdown (e.g., "-- All Stocks --")
    option = driver.find_element(By.XPATH, "//option[@value='all']")
    option.click()

    # Click the "Show" button
    show_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Show')]")
    show_button.click()

    # Wait for the table to load and validate the presence of stock data
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "stocks-table"))
    )
    stocks_table = driver.find_element(By.ID, "stocks-table").get_attribute("innerHTML")
    assert "table" in stocks_table, "Stocks table not displayed"

    print("Test passed!")
    driver.quit()

# Run the test
if __name__ == "__main__":
    test_flask_app()