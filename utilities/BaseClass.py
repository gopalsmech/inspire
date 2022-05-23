import json
import os

import pytest


@pytest.mark.usefixtures("setup_driver")
class BaseClass:

    def getJsonData(self, filename):
        jsonpath = os.getcwd() + "/testData/" + filename
        # Opening JSON file
        with open(jsonpath) as json_file:
            data = json.load(json_file)
            # Print the type of data variable
            print("Type:", type(data))
            return data