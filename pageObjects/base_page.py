import random
import string
import time
from datetime import datetime, date, timedelta


from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, log):
        self.driver = driver
        self.log = log

    def visit(self, url):
        self.driver.get(url)

    def find_element(self, *locators):
        return self.driver.find_element(*locators)

    def sendkeys_enter(self, locator, text):
        self.isElementPresent(locator)
        self.driver.find_element(*locator).send_keys(text + Keys.RETURN)

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type" + locatorType + "not correct/supported")
        return False

    def dropdownSelectElement(self, locator, selector="", selectorType="text"):
        try:
            element = self.getElement(locator)
            sel = Select(element)
            if selectorType == "value":
                sel.select_by_value(selector)
                time.sleep(1)
            elif selectorType == "index":
                sel.select_by_index(selector)
                time.sleep(1)
            elif selectorType == "text":
                sel.select_by_visible_text(selector)
                time.sleep(1)
            # self.log.info("Element selected with selector: " + str(selector) +
            #               " and selectorType: " + selectorType)

        except:
            self.log.error("Element not selected with selector: " + str(selector) +
                           " and selectorType: " + selectorType)
            # print_stack()
            return False
        return True

    def getDropdownOptionsCount(self, locator, locatorType="id"):
        '''
        get the number of options of drop down list
        :return: number of Options of drop down list
        '''
        options = None
        try:
            element = self.getElement(locator, locatorType)
            sel = Select(element)
            options = sel.options
            self.log.info("Element found with locator: " + locator +
                          " and locatorType: " + locatorType)
        except:
            self.log.error("Element not found with locator: " + locator +
                           " and locatorType: " + locatorType)

        return options

    def getDropdownSelectedOptionText(self, locator, locatorType="id"):
        '''
        get the text of selected option in drop down list
        :return: the text of selected option in drop down list
        '''
        selectedOption_text = None
        try:
            element = self.getElement(locator, locatorType)
            sel = Select(element)
            selectedOption_text = sel.first_selected_option.text
            self.log.info("Return the selected option of drop down list with locator: " + locator +
                          " and locatorType: " + locatorType)
        except:
            self.log.error("Can not return the selected option of drop down list with locator: " + locator +
                           " and locatorType: " + locatorType)

        return selectedOption_text

    def getDropdownSelectedOptionValue(self, locator, locatorType="id"):
        '''
        get the value of selected option in drop down list
        :return: the value of selected option in drop down list
        '''
        selectedOption_value = None
        try:
            element = self.getElement(locator, locatorType)
            sel = Select(element)
            selectedOption_value = sel.first_selected_option.get_attribute("value")
            self.log.info("Return the selected option of drop down list with locator: " + locator +
                          " and locatorType: " + locatorType)
        except:
            self.log.error("Can not return the selected option of drop down list with locator: " + locator +
                           " and locatorType: " + locatorType)

        return selectedOption_value

    def getElement(self, locator):
        element = None
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
            )
            element = self.driver.find_element(*locator)

        except:
            self.log.error("Element not found with locator: " + locator[1] +
                           " and locatorType: " + locator[0])
            return None
        return element

    def isElementSelected(self, locator):
        isSelected = None
        try:
            element = self.getElement(locator)
            isSelected = element.is_selected()

        except:
            self.log.error("Element not found with locator: " + locator[1] +
                           " and locatorType: " + locator[0])
            return False

        return isSelected

    def getElementList(self, locator):
        """
        Get list of elements
        """
        element = None
        assert self.waitForElementDisplay(locator)
        try:
            element = self.driver.find_elements(*locator)

        except:
            self.log.error("Element list not found with locator: " + locator[1] +
                           " and locatorType: " + locator[0])

        return element

    def elementClick(self, locator, element=None):
        """
        Either provide element or a combination of locator and locatorType
        """

        try:
            if locator:
                element = self.waitForElementClick(locator)
            element.click()

        except:
            self.log.error("cannot click on the element with locator: " + locator[1] +
                           " locatorType: " + locator[0])
            return False
        return True

    def elementActionClick(self, locator, element=None):
        """
        Either provide element or a combination of locator and locatorType
        """

        try:
            if locator:
                element = self.waitForElementClick(locator)

            actions = ActionChains(self.driver)
            actions.click(element).perform()

        except:
            self.log.error("cannot click on the element with locator: " + locator[1] +
                           " locatorType: " + locator[0])
            return False
        return True

    def elementHover(self, locator, element=None):
        """
        Either provide element or a combination of locator and locatorType
        """

        try:
            if locator:
                element = self.getElement(locator)
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            time.sleep(2)

        except:
            self.log.error("cannot hover to the element with locator: " + locator[1] +
                           " locatorType: " + locator[0])

    def sendKeys(self, locator, data, element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        time.sleep(1)
        try:
            if locator:
                element = self.waitForElementClick(locator)
            self.clearKeys(locator)
            element.send_keys(data)
        except Exception as e:
            self.log.error(e)
            return False
        return True

    def clear_and_sendKeys(self, locator, data, element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.waitForElementClick(locator)
                ActionChains(self.driver).double_click(element).click(element).double_click(element).click(element).send_keys(Keys.BACKSPACE).send_keys(data).perform()
        except Exception as e:
            self.log.error(e)
            return False
        return True

    def drag_and_drop(self, source, target):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if source:
                source1 = self.waitForElementClick(source)
                target1 = self.waitForElementClick(target)
                action = ActionChains(self.driver)
                action.drag_and_drop(source1, target1).perform()
        except Exception as e:
            self.log.error(e)
            return False
        return True

    def sendKeys_backspace(self, locator, element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.waitForElementClick(locator)
                ActionChains(self.driver).click(element).send_keys(Keys.BACKSPACE).perform()
        except Exception as e:
            self.log.error(e)
            return False
        return True

    def clearKeys(self, locator, element=None):
        """
        Clear keys of an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator)
            element.clear()

        except:
            self.log.error("cannot clear data of the element with locator: " + locator[1] +
                           " locatorType: " + locator[0])

    def getText(self, locator, element=None, info=""):
        """
        Get 'Text' on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator)
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:

                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            text = None
        return text

    def isElementPresent(self, locator):
        """
        Check if element is present
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator)
            if element is not None:
                self.log.info("Element found with locator: " + locator[1] +
                              " and locatorType: " + locator[0])
                return True
            else:
                self.log.error("Element not found with locator: " + locator[1] +
                               " and locatorType: ")
                return False
        except:
            self.log.error("Element not found with locator: " + locator[1] +
                           " and locatorType: ")
            return False

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        """
        Check if element is displayed
        Either provide element or a combination of locator and locatorType
        """
        isDisplayed = False
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator: " + locator +
                              " and locatorType: " + locatorType)
            else:
                self.log.error("Element is not displayed with locator: " + locator +
                               " and locatorType: " + locatorType)
            return isDisplayed
        except:
            self.log.error("Element is not displayed with locator: " + locator +
                           " and locatorType: " + locatorType)
            return False

    def elementPresenceCheck(self, locator="", locatorType="id"):
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False

    def waitForElementClick(self, locator, timeout=20, pollFrequency=0.5):
        element = None
        try:

            wait = WebDriverWait(self.driver, timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable(locator))


        except:
            self.log.error("Element not appeared on the web page")

        return element

    def webScroll(self, direction="up"):
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -500);")
        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 500);")

    def getURL(self):
        '''
        Get the current URL
        :return: current URL
        '''
        currentURL = self.driver.current_url

        return currentURL

    def pageBack(self):
        '''
        page back the browser
        '''
        self.driver.execute_script("window.history.go(-1)")

    def getAttributeValue(self, locator, element=None, attribute=''):
        '''
        get attribute value
        '''
        try:
            if locator:
                element = self.getElement(locator)
            attribute_value = element.get_attribute('value')
        except:
            self.log.error("Failed to get " + attribute + " in element with locator: " +
                           locator[1] + " and locatorType: " + locator[0])
            attribute_value = None
        return attribute_value

    def refresh(self):
        self.driver.get(self.driver.current_url)

    def waitForPresenceOfElement(self, locator, timeout=10, pollFrequency=0.5):
        element = None
        try:

            wait = WebDriverWait(self.driver, timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.presence_of_element_located(locator))


        except:
            self.log.error("Element not appeared on the web page")

        return element

    def waitForElementDisplay(self, locator, timeout=20, pollFrequency=0.5):
        element = None
        try:

            wait = WebDriverWait(self.driver, timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.presence_of_element_located(locator))


        except:

            return False

        return True

    def javascriptClick(self, locator, element=None):
        """
        Either provide element or a combination of locator and locatorType
        """

        try:
            if locator:
                element = self.getElement(locator)
            self.waitForElementDisplay(element)
            self.driver.execute_script("arguments[0].click();", element)
        except:
            self.log.error("cannot click on the element with locator: " + locator[1] +
                           " locatorType: " + locator[0])
            return False
        return True

    def sendKeysdownEnter(self, locator, data, element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.waitForElementClick(locator)
            element.send_keys(data)
            time.sleep(1)
            dyanamicdropdown = (By.XPATH, "(//input[@aria-expanded='true'])[last()]")
            assert self.waitForElementDisplay(dyanamicdropdown)
            dyanamicdropdown_options = (
                By.XPATH, "(//input[@aria-expanded='true']/../..//ul/li//lightning-base-combobox-item)[1]")
            assert self.waitForElementDisplay(dyanamicdropdown_options)
            assert self.javascriptClick(dyanamicdropdown_options)
        except:
            self.log.error("cannot send data on the element with locator: " + locator[1] +
                           " locatorType: " + locator[0])
            return False
        return True

    def listtypedropdown(self, dropdownlocator, option, element=None):
        try:
            element = self.getElement(dropdownlocator)
            element.click()
            time.sleep(0.5)
            dyanamicdropdown = (By.XPATH, "(//ul/li/a[text()='" + option + "'])[last()]")
            self.javascriptClick(dyanamicdropdown)

        except:
            self.log.error("Error occured during dropdown selection")
            return False
        return True

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def get_random_number(self, length):
        number = []
        number.append(random.randint(6, 9))
        for i in range(1, length):
            number.append(random.randint(0, 9))
        s = [str(i) for i in number]
        result = "".join(s)
        return result

    def isElementClickable(self, locator, element=None):
        """
        Check if element is present
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.waitForElementClick(locator)
            if element is not None:
                return True
            else:
                self.log.error("Element not found with locator: " + locator[1] +
                               " and locatorType: ")
                return False
        except:
            self.log.error("Element not found with locator: " + locator[1] +
                           " and locatorType: ")
            return False

    def waitForElementInvisible(self, locator, timeout=10, pollFrequency=0.5):
        element = None
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.invisibility_of_element_located(locator))

        except:
            self.log.error("Element not appeared on the web page")
            return False

        return True

    def spantypedropdown(self, dropdownlocator, option, element=None):
        try:
            element = self.getElement(dropdownlocator)
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(0.8)
            dyanamicdropdown = (By.XPATH, "(//span[@title='" + option + "'])[last()]")
            assert self.javascriptClick(dyanamicdropdown)

        except:
            self.log.error("Error occured during dropdown selection")
            return False
        return True

    def multiselectmove(self, option, listvalues):
        for i in listvalues:
            dyanamiclocator = (By.XPATH, "//div[text()='" + option + "']/..//ul/li//span[@title='" + i + "']")
            self.javascriptClick(dyanamiclocator)
            time.sleep(0.5)
            moveoption = (By.XPATH, "(//div[text()='" + option + "']/..//button[@title='Move selection to Chosen'])")
            assert self.javascriptClick(moveoption)
        return True

    def sendKeysdownEnterList(self, locator, data, element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.waitForElementClick(locator)
            element.send_keys(data)
            time.sleep(1)
            dyanamicdropdown = (By.XPATH, "(//input[@aria-expanded='true'])[last()]")
            self.waitForElementDisplay(dyanamicdropdown)
            dyanamicdropdown_options = (
                By.XPATH, "(//ul[contains(@class,'visible')]/li[not(contains(@class,'invisible'))])[1]")
            self.waitForElementDisplay(dyanamicdropdown_options)
            self.javascriptClick(dyanamicdropdown_options)
        except:
            self.log.error("cannot send data on the element with locator: " + locator[1] +
                           " locatorType: " + locator[0])
            return False
        return True

    def multiselectdropdown(self, type, options):
        try:
            dyanamiclocator = (By.XPATH, "//div[contains(text(),'" + type + "')]/..//span[text()='" + options[0] + "']")
            self.javascriptClick(dyanamiclocator)
            if len(options) > 1:
                for i in range(1, len(options)):
                    dyanamiclocator1 = (By.XPATH, "//div[text()='" + type + "']/..//span[text()='" + options[i] + "']")
                    element1 = self.getElement(dyanamiclocator1)
                    print(element1)
                    time.sleep(2)
                    actions = ActionChains(self.driver)
                    actions.key_down(Keys.CONTROL).click(on_element=element1).key_up(Keys.CONTROL).perform()
            time.sleep(2)
            moveoption = (By.XPATH, "(//div[text()='" + type + "']/..//button[@title='Move selection to Chosen'])")
            assert self.javascriptClick(moveoption)
            for j in options:
                chosen_verify = (By.XPATH, "//span[text()='Chosen']/..//span/span[text()='" + j + "']")
                self.waitForElementDisplay(chosen_verify)
        except:
            self.log.error("cannot select options from multiselect dropdown")
            return False
        return True

    def asset_values(self, data):
        time.sleep(1)
        assets_locator = (By.XPATH, "(//span[text()='Assets']/../../../..//span[text()='" + data + "'])[last()]")
        assert self.waitForElementDisplay(assets_locator)

    def flow_values(self, data):
        flow_locator = (By.XPATH, "(//span[text()='Flows']/../../../..//span[text()=" + '"' + data + '"' + "])[last()]")
        assert self.waitForElementDisplay(flow_locator)

    def sendKeysdownEnterPress(self, locator, data, element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.waitForElementClick(locator)
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(0.6)
            element.send_keys(data)
            dyanamiclocator = (
                By.XPATH, "(//div[@aria-expanded='true' and contains(@class,'slds-is-open')]//strong)[1]")
            self.waitForElementDisplay(dyanamiclocator)
            self.elementClick(dyanamiclocator)
        except:
            self.log.error("cannot send data on the element with locator: " + locator[1] +
                           " locatorType: " + locator[0])
            return False
        return True

    def getTodayDate(self):
        return str('{dt.month}/{dt.day}/{dt.year}'.format(dt=datetime.now()))

    def getTomorrowDate(self):
        EndDate = date.today() + timedelta(days=1)
        return EndDate.strftime('%m/%d/%Y')

    def getYesterdayDate(self):
        EndDate = date.today() - timedelta(days=1)
        return EndDate.strftime('%m/%d/%Y')

    def check_mandatory_field(self, locator):
        (byvalue, locatorvalue) = locator
        newlocator = locatorvalue + "/../../../../../../../..//abbr[text()='*']"
        assert self.waitForElementDisplay((byvalue, newlocator), timeout=7)

    def check_mandatory_field_activity_notes(self, locator):
        (byvalue, locatorvalue) = locator
        newlocator = locatorvalue + "/../../../../..//abbr[text()='*']"
        assert self.waitForElementDisplay((byvalue, newlocator), timeout=7)

    def get_spandropdown_values(self, locator):
        assert self.javascriptClick(locator)
        dropdownelement = self.driver.find_elements(By.XPATH, "//input[@aria-expanded='true']/../..//div//span[2]/span")
        values = set()
        for i in dropdownelement:
            values.add(i.text)
        return values

    def get_buttondropdown_values(self, locator):
        assert self.javascriptClick(locator)
        time.sleep(0.5)
        dropdownelement = self.driver.find_elements(By.XPATH, "//*[@aria-selected='true']/..//span/../span[2]")
        list_value = []
        for i in dropdownelement:
            list_value.append(i.text)
        return list_value

    def get_listdropdown_values(self, locator):
        assert self.javascriptClick(locator)
        time.sleep(1)
        dropdownelement = self.driver.find_elements(By.XPATH, "//*[contains(@class,'visible positioned')]//li/a")
        list_value = []
        for i in dropdownelement:
            list_value.append(i.text)
        assert self.javascriptClick(locator)
        return list_value

    def json_list_filter(self, listvalue):
        return [x for x in listvalue if "Edit" not in x]

    def sendKeysdownEnterActivity(self, locator, data, element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:
                element = self.waitForElementClick(locator)
            self.javascriptClick(locator)
            element.send_keys(data)
            dropdownoption = (By.XPATH, "(//strong)[1]")
            assert self.waitForElementDisplay(dropdownoption)
            time.sleep(1)
            assert self.javascriptClick(dropdownoption)
        except:
            self.log.error("cannot send data on the element with locator: " + locator[1] +
                           " locatorType: " + locator[0])
            return False
        return True

    def switchtoChildWindow(self):
        child_window = self.driver.window_handles[1]
        self.driver.switch_to_window(child_window)

    def getListText(self, locator):
        list_value = []
        elementlist = self.getElementList(locator)
        if len(elementlist) == 0:
            self.log.error("Element list is empty")
            return False
        else:
            for i in elementlist:
                list_value.append(i.text)
            return list_value

    def switchtoiframe(self):
        self.driver.switch_to.frame("iframe")

    def switchtoparentwindow(self):
        self.driver.switch_to.default_content()

