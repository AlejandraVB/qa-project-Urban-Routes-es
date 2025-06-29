from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class UrbanRoutesPage:
    # Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    phone_input = (By.ID, 'phone')
    code_input = (By.ID, 'code')
    card_button = (By.ID, 'card')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.CLASS_NAME, 'card-input')
    card_link_button = (By.ID, 'submit-card')
    blanket_checkbox = (By.ID, 'blanket')
    ice_cream_plus_button = (By.CLASS_NAME, 'increment')
    ice_cream_counter = (By.CLASS_NAME, 'counter')
    message_input = (By.ID, 'comment')
    order_button = (By.ID, 'order')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)
        self.driver.find_element(*self.to_field).send_keys(Keys.TAB)

    def select_tariff_comfort(self):
        self.driver.find_element(By.CLASS_NAME, 'tariff__card').click()

    def enter_phone_number(self, phone):
        self.driver.find_element(*self.phone_input).send_keys(phone)
        self.driver.find_element(*self.phone_input).send_keys(Keys.TAB)

    def enter_phone_code(self, code):
        self.driver.find_element(*self.code_input).send_keys(code)

    def add_credit_card(self, number, code):
        self.driver.find_element(*self.card_button).click()
        self.driver.find_element(*self.card_number_input).send_keys(number)
        self.driver.find_element(*self.card_code_input).send_keys(code)
        self.driver.find_element(*self.card_code_input).send_keys(Keys.TAB)
        self.driver.find_element(*self.card_link_button).click()

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_checkbox).click()

    def request_ice_creams(self, quantity):
        for _ in range(quantity - 1):
            self.driver.find_element(*self.ice_cream_plus_button).click()

    def write_message_for_driver(self, message):
        self.driver.find_element(*self.message_input).send_keys(message)

    def order_taxi(self):
        self.driver.find_element(*self.order_button).click()