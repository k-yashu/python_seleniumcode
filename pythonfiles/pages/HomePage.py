from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    SEARCH_BOX = (By.NAME, 'q')
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'button.L0Z3Pu')
    USER_PROFILE_ICON = (By.CSS_SELECTOR, 'div._28p97w')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def search_product(self, product_name):
        search_box = self.wait.until(EC.visibility_of_element_located(self.SEARCH_BOX))
        search_box.clear()
        search_box.send_keys(product_name)
        self.driver.find_element(*self.SEARCH_BUTTON).click()

    def is_logged_in(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except Exception:
            return False
