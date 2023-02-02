from requests import get

# API for the winch - Joffen
class WinchController():
    def __init__(self, url="https://blynk.cloud/external/api", token="8t8bhyGlugCGMlQ--BfEUBgW31byK8ZT"):
        self.url = url
        self.token = token
    
    def lower_winch(self):
        get(self.url + "/update?token=" + self.token + "&dataStreamId=5&value=1")

    def stop_winch(self):
        get(self.url + "/update?token=" + self.token + "&dataStreamId=5&value=0")

    def raise_winch(self):
        get(self.url + "/update?token=" + self.token + "&dataStreamId=6&value=1")
       