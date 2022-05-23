from pageObjects.login_page import LoginPage
from pageObjects.home_page import HomePage
from pageObjects.workspace_page import WorkSpacePage
from utilities.BaseClass import BaseClass
from utilities.custom_logger import customLogger
from utilities import read_json as td


class TestInspire(BaseClass):
    board_name = td.testData("board_name", "test_data/trello_data.json")
    list_name = td.testData("list_name", "test_data/trello_data.json")
    card_name = td.testData("card_name", "test_data/trello_data.json")

    def test_inspire_website(self):
        log = customLogger()
        loginPage = LoginPage(self.driver, log)
        loginPage.trello_login()
        homePage = HomePage(self.driver, log)
        homePage.create_trello_board(self.board_name)
        workspacePage = WorkSpacePage(self.driver, log)
        workspacePage.create_lists(self.list_name[0])
        workspacePage.create_lists(self.list_name[1])
        workspacePage.create_lists(self.list_name[2])
        workspacePage.add_card()
        workspacePage.create_cards(self.card_name[0])
        workspacePage.create_cards(self.card_name[1])
        workspacePage.create_cards(self.card_name[2])
