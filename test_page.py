import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
import data
from page import UrbanRoutesPage
from helpers import retrieve_phone_code
from wait_helpers import wait_for_element
from selenium.common.exceptions import NoSuchElementException


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # Configura el navegador con logging para capturar el código SMS
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    # Prueba: ingresar direcciones de origen y destino
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        # Verifica que el valor en los campos coincida
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # Prueba: seleccionar tarifa Comfort
    def test_select_tariff(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_tariff_comfort()
        wait_for_element(self.driver, (By.ID, 'order'))
        # assert que verifica que el botón para pedir taxi aparece
        assert self.driver.find_element(By.ID, 'order').is_displayed()

    # Prueba: ingreso de número de teléfono y código
    def test_enter_phone_and_code(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        # Primer paso configurar la ruta
        page.set_route(data.address_from, data.address_to)
        # Paso dos seleccionar la tarifa
        page.select_tariff_comfort()
        # Paso 3 ingresar el número y código
        page.enter_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        page.enter_phone_code(code)
        wait_for_element(self.driver, (By.ID, 'card'))
        # assert que el botón de agregar tarjeta aparece
        assert self.driver.find_element(By.ID, 'card').is_displayed()

    # Prueba: agregar tarjeta de crédito
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_tariff_comfort()
        page.enter_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        page.enter_phone_code(code)
        # Paso de agregar tarjeta
        page.add_credit_card(data.card_number, data.card_code)
        wait_for_element(self.driver, (By.ID, 'blanket'))
        # assert que aparecen los extras
        assert self.driver.find_element(By.ID, 'blanket').is_displayed()

    # Prueba: pedir manta y pañuelos
    def test_request_blanket(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_tariff_comfort()
        page.enter_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        page.enter_phone_code(code)
        page.add_credit_card(data.card_number, data.card_code)
        page.request_blanket_and_tissues()
        # assert muy simple, que el checkbox sigue presente
        assert self.driver.find_element(By.ID, "blanket").is_displayed()

    # Prueba: pedir 2 helados
    def test_request_ice_creams(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_tariff_comfort()
        page.enter_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        page.enter_phone_code(code)
        page.add_credit_card(data.card_number, data.card_code)
        page.request_ice_creams(2)
        # assert simple, que el counter incrementó
        assert self.driver.find_element(By.CLASS_NAME, "counter").is_displayed()

    # Prueba: flujo completo con mensaje al conductor y ordenar taxi
    def test_full_order(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_tariff_comfort()
        page.enter_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        page.enter_phone_code(code)
        page.add_credit_card(data.card_number, data.card_code)
        page.request_blanket_and_tissues()
        page.request_ice_creams(2)
        page.write_message_for_driver(data.message_for_driver)
        page.order_taxi()
        # assert para validar que después del click el botón ya no esté
        try:
            self.driver.find_element(By.ID, "order")
            assert False, "El botón 'order' sigue visible después de pedir el taxi"
        except NoSuchElementException:
            assert True

    @classmethod
    def teardown_class(cls):
        # Cierra el navegador al terminar las pruebas
        cls.driver.quit()
