from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    LOGIN_POPUP = (By.CSS_SELECTOR, 'div._2QfC02')
    CLOSE_POPUP_BTN = (By.CSS_SELECTOR, 'button._2KpZ6l._2doB4z')
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input._2IX_2-._35mYYy')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input._2IX_2-._3mctLh')
    LOGIN_BTN = (By.CSS_SELECTOR, 'button._2KpZ6l._2HKlqd._3AWRsL')
    OTP_BTN = (By.XPATH, '//button[contains(text(), "Request OTP")]')
    OTP_INPUT = (By.CSS_SELECTOR, 'input._2IX_2-._3mctLh')
    SUBMIT_OTP_BTN = (By.XPATH, '//button[contains(text(), "Verify")]')
    ERROR_MSG = (By.CSS_SELECTOR, 'span._2YULOR')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get('https://www.flipkart.com')
        self.close_login_popup()

    def close_login_popup(self):
        try:
            close_btn = self.wait.until(EC.element_to_be_clickable(self.CLOSE_POPUP_BTN))
            close_btn.click()
        except TimeoutException:
            pass  # Popup not present

    def login_with_password(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()

    def login_with_otp(self, username, otp_callback):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(username)
        self.driver.find_element(*self.OTP_BTN).click()
        otp = otp_callback()
        self.wait.until(EC.visibility_of_element_located(self.OTP_INPUT)).send_keys(otp)
        self.driver.find_element(*self.SUBMIT_OTP_BTN).click()

    def get_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MSG)).text
        except TimeoutException:
            return None

class HomePage:
    SEARCH_BOX = (By.NAME, 'q')
    SEARCH_BTN = (By.CSS_SELECTOR, 'button.L0Z3Pu')
    USER_ICON = (By.CSS_SELECTOR, 'div._28p97w')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def search_product(self, product_name):
        search_box = self.wait.until(EC.visibility_of_element_located(self.SEARCH_BOX))
        search_box.clear()
        search_box.send_keys(product_name)
        self.driver.find_element(*self.SEARCH_BTN).click()

    def is_user_logged_in(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_ICON))
            return True
        except TimeoutException:
            return False

class ProductPage:
    PRODUCT_TITLES = (By.CSS_SELECTOR, 'div._4rR01T, a.IRpwTa')
    ADD_TO_CART_BTN = (By.XPATH, '//button[contains(text(), "Add to cart")]')
    GO_TO_CART_BTN = (By.XPATH, '//button[contains(text(), "GO TO CART")]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def select_first_product(self):
        products = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_TITLES))
        if products:
            products[0].click()
            self.driver.switch_to.window(self.driver.window_handles[-1])
        else:
            raise Exception('No products found')

    def add_to_cart(self):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN))
        add_btn.click()

    def go_to_cart(self):
        go_cart_btn = self.wait.until(EC.element_to_be_clickable(self.GO_TO_CART_BTN))
        go_cart_btn.click()

class CartPage:
    CART_ITEMS = (By.CSS_SELECTOR, 'div._1AtVbE')
    REMOVE_BTN = (By.XPATH, '//div[contains(text(), "Remove")]')
    CONFIRM_REMOVE_BTN = (By.XPATH, '//div[contains(text(), "Remove Item")]')
    EMPTY_CART_MSG = (By.CSS_SELECTOR, 'div._1LCJ1U')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_cart_items(self):
        items = self.driver.find_elements(*self.CART_ITEMS)
        return [item.text for item in items if item.text.strip()]

    def remove_first_product(self):
        remove_btns = self.driver.find_elements(*self.REMOVE_BTN)
        if remove_btns:
            remove_btns[0].click()
            confirm_btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_REMOVE_BTN))
            confirm_btn.click()
        else:
            raise Exception('No remove button found')

    def is_cart_empty(self):
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.EMPTY_CART_MSG))
            return 'empty' in msg.text.lower()
        except TimeoutException:
            return False
