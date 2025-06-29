from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(driver, locator, timeout=10):
    """Espera explícita genérica para que un elemento esté presente y visible."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )