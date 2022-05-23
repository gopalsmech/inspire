from selenium.webdriver.common.by import By


class WorkSpacePageLocators:
    card_title_locator = (By.XPATH, "//textarea[contains(@placeholder,'Enter a title')]")
    add_card_btn_locator = (By.XPATH, "//input[@type='submit' and @value='Add card']")
    list_locator = (By.XPATH, "//input[contains(@placeholder,'Enter list title')]")
    add_list_locator = (By.XPATH, "//input[@type='submit' and @value='Add list']")
    add_card_link_locator = (By.XPATH, "//h2[text()='Not Started']/../../descendant::span[text()='Add a card']")
    existing_list_locator = (By.XPATH, "//textarea[text()='To Do']")
