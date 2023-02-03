import requests
import json

class PartyController():
    def __init__(self):
      pass

    def get_party():
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
