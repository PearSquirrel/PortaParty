import requests
import json

class PartyController():
    def __init__(self):
      pass

    def get_party(self):
      url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/portaparty"

      payload = json.dumps({
        "action": "getparty"
      })
      headers = {
        'Content-Type': 'application/json'
      }

      response = requests.request("POST", url, headers=headers, data=payload)

      print(response.text)

      js = response.json()

      if js['status'] == "0" :
          print("party is off")

      if js['status'] == "1" :
          print("party is on")

    def start_party(self):
      url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/portaparty"

      payload = json.dumps({
        "action": "startparty"
      })
      headers = {
        'Content-Type': 'application/json'
      }

      response = requests.request("POST", url, headers=headers, data=payload)

      print(response.text)

    def stop_party(self):
      url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/portaparty"

      payload = json.dumps({
        "action": "stopparty"
      })
      headers = {
        'Content-Type': 'application/json'
      }

      response = requests.request("POST", url, headers=headers, data=payload)

      print(response.text)
