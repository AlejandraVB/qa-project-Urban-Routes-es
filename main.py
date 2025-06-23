import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

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

#Click en la tarifa 'Comfort'
    def select_tariff_comfort(self):
        tariff=self.driver.find_element(By.CLASS_NAME,'tariff__card')
        tariff.click()

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)
        self.driver.find_element(*self.to_field).send_keys(Keys.TAB)


#Ingreso de Phone number y código
    phone_input= (By.ID, 'phone')
    code_input = (By.ID, 'code')
    def enter_phone_number(self, phone):
        self.driver.find_element(*self.phone_input).send_keys(phone)
        self.driver.find_element(*self.phone_input).send_keys(Keys.TAB)
    def enter_phone_code(self, code):
        self.driver.find_element(*self.code_input).send_keys(code)

# Agregar Tarjeta de crédito
    #Localizadores
    card_button=(By.ID,'card')
    card_number_input=(By.ID,'number')
    card_code_input = (By.CLASS_NAME,'card-input')
    card_link_button = (By.ID, 'submit-card')

    def add_credit_card (self,number,code):
        self.driver.find_element(*self.card_button).click()
        self.driver.find_element(*self.card_number_input).send_keys(number)
        self.driver.find_element(*self.card_code_input).send_keys(code)
        #Presionar TAB para quitar el foco del campo CVV y activar el botón
        self.driver.find_element(*self.card_code_input).send_keys(Keys.TAB)

        self.driver.find_element(*self.card_link_button).click()
#Pedir manta, pañuelos y 2 helados
    blanket_checkbox=(By.ID,'blanket')
    ice_cream_plus_button=(By.CLASS_NAME,'increment')
    ice_cream_counter=(By.CLASS_NAME,'counter')

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_checkbox).click()
    def request_ice_creams(self,quantity):
        for _ in range (quantity - 1): #Ya aparece con 1, sumamos desde 2
            self.driver.find_element(*self.ice_cream_plus_button).click()
#Mensaje para el conductor y ordenar taxi
    message_input=(By.ID,'comment')
    order_button = (By.ID,'order')

    def write_message_for_driver(self,message):
        self.driver.find_element(*self.message_input).send_keys(message)

    def order_taxi(self):
        self.driver.find_element(*self.order_button).click()



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        #Correccion
        # from selenium.webdriver.chrome.options import Options
        #
        # options = Options()
        # options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        # cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
    # Prueba para seleccionar Tarifa
    def test_select_tariff(self):
        self.driver.get(data.urban_routes_url)
        page= UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_tariff_comfort()
    #Prueba de ingreso de codigo y phone number
    def test_enter_phone_and_code(self):
        self.driver.get(data.urban_routes_url)
        page= UrbanRoutesPage(self.driver)
        # Primer paso configurar la ruta
        page.set_route(data.address_from, data.address_to)
        #Paso dos seleccionar la tarifa
        page.select_tariff_comfort()
        #Paso 3 ingresar el número y Codigo
        page.enter_phone_number(data.phone_number)
        code= retrieve_phone_code(self.driver)
        page.enter_phone_code(code)

    #Prueba de agregar tarjeta
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        page= UrbanRoutesPage(self.driver)
        page.set_route(data.address_from,data.address_to)
        page.select_tariff_comfort()
        page.enter_phone_number(data.phone_number)
        code= retrieve_phone_code(self.driver)
        page.enter_phone_code(code)
        #Paso de agregar tarjeta

        page.add_credit_card(data.card_number, data.card_code)
    #Prueba pedir manta, pañuelos y helados
    def test_extras_and_order(self):
        self.driver.get(data.urban_routes_url)
        page= UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_tariff_comfort()
        page.enter_phone_number(data.phone_number)
        code= retrieve_phone_code(self.driver)
        page.enter_phone_code(code)
        page.add_credit_card(data.card_number,data.card_code)

        #pedir La manta y pañuelos
        page.request_blanket_and_tissues()
        #pedir 2 helados
        page.request_ice_creams(2)
    #Prueba full order
    def test_full_order(self):
        self.driver.get(data.urban_routes_url)
        page=UrbanRoutesPage(self.driver)
        page.set_route(data.address_from,data.address_to)
        page.select_tariff_comfort()
        page.enter_phone_code(code)
        page.add_credit_card(data.card_number,data.card_code)
        page.request_ice_creams(2)

        #Mensaje para el conductor
        page.write_message_for_driver(data.message_for_driver)
        #Pedir taxi
        page.order_taxi()







    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
