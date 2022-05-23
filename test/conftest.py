import os.path
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from utilities import read_json as td


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", default="chrome"
    )


@pytest.fixture(scope="session")
def setup_driver(request):
    RUN_FROM = td.testData("run_from", "config/properties.json")
    inspire_url = td.testData("environment", "config/properties.json")
    browser_name = td.testData("browser", "config/properties.json")

    global driver
    if RUN_FROM == 'Remote':
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs",
                                               {"profile.default_content_setting_values.notifications": 1})
        desired_cap = chrome_options.to_capabilities()
        desired_cap.update({
            "browserName": "chrome",
            "version": "99.0",
            "enableVNC": True,
            "enableVideo": True
        })

        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            desired_capabilities=desired_cap)

    elif RUN_FROM == 'Local':
        if browser_name == "chrome":
            driver = webdriver.Chrome(ChromeDriverManager().install())

        elif browser_name == "firefox":
            driver = webdriver.Firefox()

    driver.get(inspire_url)
    driver.implicitly_wait(20)
    driver.maximize_window()
    node = request.node

    for item in node.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", driver)
    yield

    # driver.quit()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup_driver":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            report_directory = os.path.dirname("reports")
            file_name = report.nodeid.replace("::", "_") + ".png"
            destinationFile = os.path.join(report_directory, file_name)
            _capture_screenshot(destinationFile)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)
