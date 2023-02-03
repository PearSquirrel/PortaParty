from flask import Flask, render_template
from drone_api import DroneController
from blynk_api import WinchController
import time
from detect import ObjectDetection
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST']) 
def home():
    return render_template("index.html")

@app.route('/party', methods=['GET', 'POST']) 
def party():
    print("clicked party")

    #### FlytBase Cloud API ####
    token = '60ac081f527e8baab8ac3bae078d1922d34cfd2e' # personal access token
    droneHandle = DroneController(Token=token, VehicleId='r4EeYcnz',
                              fb_server_url='https://dev.flytbase.com/rest/ros/flytos')

    detect = ObjectDetection()

    party = True
    while party:
        if detect.run_object_detection():
            # if detect.run_object_detection():
            print("more than two people in the frame")
            # time.sleep(20)

            # detect.run_object_detection()
                #### Blynk API ####
            winch = WinchController()
            winch.lower_winch()
            print("Lowering winch...")
            time.sleep(2)
            winch.stop_winch()
            time.sleep(1)
            print("Stopped winch")
            winch.raise_winch()
            print("Raising winch...")
            party = False
        else:
            print("Not enough people")
    
        # print("less than three people in the frame")
    
    return render_template("party.html")


if __name__ == "__main__":
    app.run(debug=True)