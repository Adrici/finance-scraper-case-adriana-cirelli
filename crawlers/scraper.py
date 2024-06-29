import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager  

class YahooFinanceCrawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Opcional: rodar em modo headless
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.url = "https://finance.yahoo.com/screener/new"

    def navigate(self):
        self.driver.get(self.url)

    def wait_for_element(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            print(f"Element not found: {value}")
            self.driver.quit()
            raise

    def remove_filter(self):
        criteria_div = self.wait_for_element(By.CSS_SELECTOR, "div[data-test='screener-criteria']")
        field_section_div = criteria_div.find_element(By.CSS_SELECTOR, 'div[data-test="field-section"]')
        label_filter_list = field_section_div.find_element(By.CSS_SELECTOR, 'ul[data-test="label-filter-list"]')
        remove_us_button = label_filter_list.find_element(By.XPATH, './/li/button[@title="Remove United States"]')
        remove_us_button.click()

    def apply_new_filter(self, filter_text):
        time.sleep(5)
        label_filter_list = self.wait_for_element(By.CSS_SELECTOR, 'ul[data-test="label-filter-list"]')
        remaining_li_button = label_filter_list.find_element(By.XPATH, './/li/button')
        remaining_li_button.click()
        filter_add_div = self.wait_for_element(By.CLASS_NAME, 'filterAdd')
        dropdown_menu = filter_add_div.find_element(By.ID, 'dropdown-menu')
        itm_menu_cntr = dropdown_menu.find_element(By.CSS_SELECTOR, 'div[data-test="itm-menu-cntr"]')
        find_filters_input = itm_menu_cntr.find_element(By.XPATH, './/input[@placeholder="Find filters"]')
        find_filters_input.send_keys(filter_text)
        time.sleep(5)
        argentina_checkbox = itm_menu_cntr.find_element(By.XPATH, './/input[@type="checkbox"]')
        argentina_checkbox.click()

    def click_find_stock_button(self):
        time.sleep(7)
        find_stock_button = self.wait_for_element(By.CSS_SELECTOR, "button[data-test='find-stock']")
        find_stock_button.click()

    def extract_data(self):
        all_data = []
        page = 1
        headers = []

        while True:
            # Wait for the screener-results section to be visible
            self.wait_for_element(By.ID, "screener-results")
            print(f"Found screener-results section on page {page}")
            # Wait until the table is loaded
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )

            # Extract headers if not already extracted
            if not headers:
                headers = [header.text for header in self.driver.find_elements(By.XPATH, "//table/thead/tr/th")]

            # Extract rows
            rows = self.driver.find_elements(By.XPATH, "//table/tbody/tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                cell_data = [cell.text for cell in cells]
                # Select only Symbol, Name, and Price (Intraday) columns
                selected_data = [cell_data[headers.index("Symbol")], cell_data[headers.index("Name")], cell_data[headers.index("Price (Intraday)")]]
                all_data.append(selected_data)

            # Move to the next page
            try:
                next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
                parent_button = next_button.find_element(By.XPATH, "..")
                if "disabled" in parent_button.get_attribute("class"):
                    break  # No more pages
                else:
                    parent_button.click()
                    page += 1
                    time.sleep(5)  # Wait for the next page to load
            except Exception as e:
                print(f"Error while navigating to next page: {e}")
                break

        return ["Symbol", "Name", "Price (Intraday)"], all_data

    def close(self):
        self.driver.quit()

    def save_to_csv(self, headers, data, filename):
        results_dir = 'results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        full_path = os.path.join(results_dir, filename)
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

    def run(self, filter_text, filename):
        self.navigate()
        self.remove_filter()
        self.apply_new_filter(filter_text)
        self.click_find_stock_button()
        headers, data = self.extract_data()
        self.save_to_csv(headers, data, f"{filename}.csv")
        self.close()

