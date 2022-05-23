from pageObjects.base_page import BasePage
from locators.home_page_locators import HomePageLocators as home_locat


class HomePage(BasePage):

    def create_trello_board(self, board_name):
        assert self.elementClick(home_locat.create_button_locator)
        assert self.elementClick(home_locat.create_board_button_locator)
        assert self.sendKeys(home_locat.board_name_locator, board_name)
        assert self.elementClick(home_locat.final_create_button_locator)



