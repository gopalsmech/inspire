import os

import json


def testData(attribute, JsonfileName):
    testDataPath = os.path.abspath(JsonfileName)
    testDataJsonFile = readJson(testDataPath)
    return testDataJsonFile[attribute]


def readJson(jsonFilePath):
    with open(jsonFilePath) as f:
        jsonFile = json.load(f)

    return jsonFile
