# This file is going to include method that will parse
# The specific data that we need from each one of clinics.

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

class Report:
    def __init__(self, source_page):
        self.page = source_page
        self.soup = self.soup_page()
        self.record = self.pull_data()

    def soup_page(self):
        return BeautifulSoup(self.page, "lxml")
    
    def pull_data(self):
        record = []
        try:
            name = self.soup.find("h1", {"class", "DUwDvf"}).text
        except:
            name = np.nan

        try:
            div_website = self.soup.find("img", {"src":"//www.gstatic.com/images/icons/material/system_gm/2x/public_gm_blue_24dp.png"}).parent.parent.parent
            website = div_website.find("div", {"class": "Io6YTe"}).text
        except:
            website = np.nan

        try:
            div_phone = self.soup.find("img", {"src":"//www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png"}).parent.parent.parent
            phone = div_phone.find("div", {"class": "Io6YTe"}).text
        except:
            phone = np.nan

        try:
            div_address = self.soup.find("img", {"src":"//www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png"}).parent.parent.parent
            address = div_address.find("div", {"class": "Io6YTe"}).text
        except:
            address = np.nan

        try:
            div_location = self.soup.find("img", {"src":"//maps.gstatic.com/mapfiles/maps_lite/images/2x/ic_plus_code.png"}).parent.parent.parent
            location = div_location.find("div", {"class": "Io6YTe"}).text
        except:
            location = np.nan

        try:
            city = address.split(",")[-3]
        except:
            city = np.nan

        try:
            state = address.split(",")[-2]
            state = ''.join(filter(lambda z: not z.isdigit(), state))
            state = state.strip()
        except:
            state = np.nan

        try:
            rate = self.soup.find("div", {"class", "F7nice"}).find("span").find("span").text
        except:
            rate = np.nan

        try:
            reviews = self.soup.find("div", {"class", "F7nice"}).find("span").find_next_sibling("span").text.lstrip("(").rstrip(")")
        except:
            reviews = np.nan

        record = [name, website, phone, address, location, city, state, rate, reviews]
        return record

    def append_to_csv(self):
        csv_file = pd.read_csv(r"C:\Users\Ahmad\Desktop\projects\google maps scrapper\maps\data\dentists.csv", index_col=0)
        record = self.record
        new_record = pd.DataFrame({"Name": [record[0]],
                                    "Website": [record[1]],
                                    "Phone": [record[2]],
                                    "Address": [record[3]],
                                    "Location":[record[4]],
                                    "City":[record[5]],
                                    "State":[record[6]],
                                    "Rating":[record[7]],
                                    "Reviews":[record[8]]})
        csv_file = pd.concat([csv_file, new_record], ignore_index=True)
        csv_file.to_csv(r"C:\Users\Ahmad\Desktop\projects\google maps scrapper\maps\data\dentists.csv")
