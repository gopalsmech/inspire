1) This Selenium Automation framework is developed using PyTest with Page Object Model

2) The main components of this framework are 
   a) Locators - Where all web-element locator for the respective pages are stored
   b) PageObjects - The functionalities for each page are covered here
   c) Test - Where all the test case flows are manipulated using different page functions
   d) Conftest - The driver initiation and tear down actions are carried out here. Also 
      it has the feasibility to run the code in local or in Cloud environment
   e) Test_Data - In this framework we can provide our input (test data) in JSON or EXCEL
   f) Utilities - It has the common function in which driver instance is not necessary
   g) Requirements - This contains of required library to support for this automation framework

3) Using this framework the test cases can be run in Local machine or in Cloud environment by using
   Selenoid in GCP.

4) This PyTest framework also supports Parallel run and rerunning of failed test cases

5) Also, HTML report is implemented where we can see the fine report with screenshots(Allure report also possible)

# **Why this Framework:**

1) This framework is much reusable, where we can utilise this framework for different web applications
2) The Duplication effort is absolutely avoided as we are using POM
3) As per current automation trends the PyTest framework supports for different application integration(Ex- TestRail)
4) It supports for Cloud run and CI-CD pipeline
5) It is easy to modify for new enhancement.
