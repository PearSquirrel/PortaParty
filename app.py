from flask import Flask, render_template, request, jsonify
from drone_api import DroneController
from blynk_api import WinchController
import time
from detect import ObjectDetection
from flask_cors import CORS
from get_party import PartyController
import json
import base64
from PIL import Image
import io
import atexit
import subprocess
import json, os, signal




app = Flask(__name__)
CORS(app)
party = False

@app.route('/', methods=['GET', 'POST']) 
def home():
    return render_template("index.html")

@app.route('/party', methods=['GET', 'POST']) 
def party():
    if not party:
        return json.dumps({'objects': []})
    
    print("clicked party")
    image_string = json.loads(request.data)['image_string']
    image_data = base64.b64decode(image_string)
    image = Image.open(io.BytesIO(image_data))
    # print(type(image))
    # image.show()

    #### FlytBase Cloud API ####
    token = '60ac081f527e8baab8ac3bae078d1922d34cfd2e' # personal access token
    droneHandle = DroneController(Token=token, VehicleId='r4EeYcnz',
                              fb_server_url='https://dev.flytbase.com/rest/ros/flytos')

    detect = ObjectDetection()
    PartyController().get_party()
    # time.sleep(1)
    PartyController().start_party()
    # PartyController().stop_party()
    
    detected_objects = detect.get_detected_objects(image)
    print("Found " + str(len(detected_objects)) + " people")

    if len(detected_objects) >= 1:

        #### Blynk API ####
        winch = WinchController()
        winch.lower_winch()
        print("Lowering winch...")
        time.sleep(10)
        winch.stop_winch()
        # time.sleep(1)
        print("Stopped winch")
        # winch.raise_winch()
        print("Raising winch...")
        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({ "success": True, "message": "Server is shutting down..." })        
    return json.dumps({'status': 'success', 'objects': detected_objects})


if __name__ == "__main__":
    app.run(debug=True)