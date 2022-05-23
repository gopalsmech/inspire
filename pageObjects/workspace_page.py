from selenium.common.exceptions import NoSuchElementException

from pageObjects.base_page import BasePage
from locators.workspace_page_locators import WorkSpacePageLocators as workspace_locat


class WorkSpacePage(BasePage):

    def create_lists(self, list_name):
        assert self.sendKeys(workspace_locat.list_locator, list_name)
        assert self.elementClick(workspace_locat.add_list_locator)

    def add_card(self):
        assert self.elementClick(workspace_locat.add_card_link_locator)

    def create_cards(self, card_name):
        assert self.sendKeys(workspace_locat.card_title_locator, card_name)
        assert self.elementClick(workspace_locat.add_card_btn_locator)

