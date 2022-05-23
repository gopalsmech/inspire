from selenium.webdriver.common.by import By


class HomePageLocators:
    create_button_locator = (By.XPATH, "//button/p[text()='Create']")
    create_board_button_locator = (By.XPATH, "//button/descendant::span[text()='Create board']")
    board_name_locator = (By.XPATH, "//div[text()='Board title']/../descendant::input")
    final_create_button_locator = (By.XPATH, "//button[text()='Create']")


