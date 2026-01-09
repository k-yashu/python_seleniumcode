import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.flipkart_pages import LoginPage, HomePage, ProductPage, CartPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_valid_credentials(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login_with_password('valid_user', 'valid_password')
    home_page = HomePage(driver)
    assert home_page.is_user_logged_in(), 'User should be logged in with valid credentials.'

def test_login_invalid_credentials(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login_with_password('invalid_user', 'invalid_password')
    error_msg = login_page.get_error_message()
    assert error_msg is not None and 'Invalid' in error_msg, 'Error message should be displayed for invalid credentials.'

def test_login_empty_fields(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login_with_password('', '')
    error_msg = login_page.get_error_message()
    assert error_msg is not None and 'Please enter' in error_msg, 'Error message should be displayed for empty fields.'

def test_login_with_otp(driver):
    def fake_otp_callback():
        return '123456'  # Simulate OTP

    login_page = LoginPage(driver)
    login_page.open()
    login_page.login_with_otp('valid_mobile_number', fake_otp_callback)
    home_page = HomePage(driver)
    assert home_page.is_user_logged_in(), 'User should be logged in with OTP.'

def test_add_product_to_cart(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login_with_password('valid_user', 'valid_password')
    home_page = HomePage(driver)
    home_page.search_product('Laptop')
    product_page = ProductPage(driver)
    product_page.select_first_product()
    product_page.add_to_cart()
    product_page.go_to_cart()
    cart_page = CartPage(driver)
    items = cart_page.get_cart_items()
    assert any('Laptop' in item for item in items), 'Product should be in cart after adding.'

def test_add_product_to_cart_without_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.close_login_popup()
    home_page = HomePage(driver)
    home_page.search_product('Laptop')
    product_page = ProductPage(driver)
    product_page.select_first_product()
    product_page.add_to_cart()
    # After clicking add to cart, Flipkart should prompt login
    login_popup_present = False
    try:
        driver.find_element(*LoginPage.LOGIN_POPUP)
        login_popup_present = True
    except:
        pass
    assert login_popup_present, 'Login prompt should be displayed when adding to cart without login.'
