from selenium.webdriver.common.by import By


class LoginPageLocators:
    signin_button_locator = (By.XPATH, "//a[@href='/login']")
    username_field_locator = (By.ID, 'user')
    login_button_locator = (By.ID, 'login')
    password_field_locator = (By.ID, 'password')
    login_submit_button_locator = (By.ID, "login-submit")


