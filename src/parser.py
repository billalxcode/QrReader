import json

# Local lib
from src.util import convert2extensions

class Parser:
    def __init__(self):
        self.path = "data/settings.json"

    def openFile(self):
        files = open(self.path, mode="r")
        content =files.read()
        files.close()
        return content

    def parseExtensions(self):
        result = {}

        content = self.openFile()
        jsn = json.loads(content)

        try:
            extensions = jsn["data"]["extensions"]
            image = convert2extensions(extensions["image"])
            video = convert2extensions(extensions["video"])

            result["image"] = image
            result["video"] = video
            return result
        except KeyError:
            return result
    
    def parseCameraSettings(self):
        result = {}
        content = self.openFile()
        jsn = json.loads(content)
        try:
            data = jsn["data"]["camera"]
            if data["isUrl"]:
                if data["url"] == "":
                    result["src"] = data["devies"]
                else:
                    result["src"] = data["url"]
            else:
                result["src"] = data["devices"]
            return result
        except KeyError:
            return result