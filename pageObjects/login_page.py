from pageObjects.base_page import BasePage
from utilities import read_json as td
from locators.login_page_locators import LoginPageLocators as login_local


class LoginPage(BasePage):

    def trello_login(self):
        user_name = td.testData("emailGmail", "config/properties.json")
        password = td.testData("password", "config/properties.json")
        assert self.elementClick(login_local.signin_button_locator)
        assert self.sendKeys(login_local.username_field_locator, user_name)
        assert self.elementClick(login_local.login_button_locator)
        assert self.sendKeys(login_local.password_field_locator, password)
        assert self.elementClick(login_local.login_submit_button_locator)
