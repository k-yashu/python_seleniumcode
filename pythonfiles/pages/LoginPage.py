from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_POPUP_CLOSE = (By.CSS_SELECTOR, 'button._2KpZ6l._2doB4z')
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input._2IX_2-._35mYY')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input._2IX_2-._3mctLh')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button._2KpZ6l._2HKlqd._3AWRsL')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'div._2M8cLY ._2YULOR')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def close_login_popup(self):
        try:
            close_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_POPUP_CLOSE))
            close_btn.click()
        except Exception:
            pass  # Popup may not always appear

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
