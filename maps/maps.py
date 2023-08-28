import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  maps.report import Report
import pandas as pd



class Maps(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\webdrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Maps, self).__init__()
        self.implicitly_wait(5)
        self.maximize_window()

    def __exit__(self, exc_type, exc, traceback):
        if self.teardown:
            self.quit()
   
    def land_first_page(self):
        self.get("https://www.google.com/maps/?entry=ttu&hl=en")

    def search(self, value):
        search_box = self.find_element(By.ID, "searchboxinput")
        search_box.clear()
        search_box.send_keys(value)
        search_box.send_keys(Keys.ENTER)
        WebDriverWait(self, 30).until(
            EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "a.hfpxzc")
        ))

    def click_card(self, number:int):
        cards = self.find_elements(By.CSS_SELECTOR, "a.hfpxzc")
        cards[number].click()
        WebDriverWait(self, 30).until(
            EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.lMbq3e")
        ))

    def current_cards_number(self):
        return len(self.find_elements(By.CSS_SELECTOR, "a.hfpxzc"))

    def is_end(self):
        try:
            self.find_element(By.XPATH, "//*[contains(text(), 'reached the end of the list.')]")
            return True
        except:
            return False

    def scroll_to_card(self, card_number:int):
        self.execute_script(f"document.querySelectorAll('a.hfpxzc')[{card_number}].scrollIntoView()")

    def scroll_to_top(self):
        self.execute_script("document.querySelector('div.kA9KIf > div.ecceSd').scrollTop = 0;")

    def scroll_to_end(self):
        self.execute_script("document.querySelector('div.kA9KIf > div.ecceSd').scrollTop = document.querySelector('div.kA9KIf > div.ecceSd').scrollHeight;")
    
    def parse_clinic(self):
        parser = Report(self.page_source)
        parser.append_to_csv()

    def convert_to_excel(self):
        csv_file = pd.read_csv(r"C:\Users\Ahmad\Desktop\projects\google maps scrapper\maps\data\dentists.csv", index_col=0)
        writer = pd.ExcelWriter(r"C:\Users\Ahmad\Desktop\projects\google maps scrapper\maps\data\dentists.xlsx")
        csv_file.to_excel(writer)
        writer.save()

