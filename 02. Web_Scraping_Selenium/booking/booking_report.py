# This file is going to include methods that will parse
# The specific data that we need from each one of the deal boxes
from selenium.webdriver.remote.webdriver import WebDriver

class BookingReport:
    def __init__(self, boxes_section_element:WebDriver):
        self.boxes_section_element = boxes_section_element

    def pull_titles(self):
        hotel_boxes = self.boxes_section_element.find_elements_by_css_selector(
            'div[data-testid="title"]'
        )
        hotel_names = []
        for hotel_box in hotel_boxes:
            hotel_names.append(hotel_box.get_attribute('innerHTML').strip())
        return hotel_names

    def pull_ratings(self):
        ratings = self.boxes_section_element.find_elements_by_css_selector(
            'div[data-testid="review-score"]'
        )
        ratings_list = []
        for rating in ratings:
            final_rating = rating.find_elements_by_css_selector('*')[0].get_attribute('innerHTML')
            ratings_list.append(final_rating)
        return ratings_list

    def pull_final_prices(self):
        prices_elements = self.boxes_section_element.find_elements_by_css_selector(
            'div[data-testid="price-and-discounted-price"]'
        )
        prices_list = []
        for price in prices_elements:
            try:
                final_price = price.find_elements_by_css_selector('*')[1].get_attribute('innerHTML')
            except:
                final_price = price.find_elements_by_css_selector('*')[0].get_attribute('innerHTML')
            prices_list.append(final_price.replace("US$", 'USD '))
        return prices_list

    def pull_deal_box_attributes(self):
        hotel_names = self.pull_titles()
        hotel_ratings = self.pull_ratings()
        hotel_prices = self.pull_final_prices()
        collection = []
        for hotel_name, hotel_rating, hotel_price in zip(hotel_names, hotel_ratings, hotel_prices):
            collection.append([hotel_name, hotel_rating, hotel_price])

        return collection