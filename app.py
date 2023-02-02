
from flask import Flask, render_template
from drone_api import DroneController
from blynk_api import WinchController
import time
# from detect import ObjectDetection


app = Flask(__name__)


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

    # detect = ObjectDetection()
    party = True
    while party:
        if run_object_detection():
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

import cv2
import numpy as np

#ENV
# api key = NjEzZDA4MjI0YjIzYmM0NGJkNjU5ZDlhNzZkZDEzODk4MmYzNzE3OGFiZjc4OWZhMThhYzE5MjQ=
# vehicleId= r4EeYcnz
# token = 60ac081f527e8baab8ac3bae078d1922d34cfd2e



def run_object_detection():


    capture = cv2.VideoCapture(0)
    wh_target = 320
    confidence_threshold = 0.8
    nms_threshold = 0.3

    class_file = 'class.names'
    class_names = []

    with open(class_file, 'rt') as f:
        class_names = f.read().rstrip('\n').split('\n')

    # tiny weights (higher frame rate, lower accuracies)
    #model_config = 'yolov3-tiny.cfg'
    #model_weights = 'yolov3-tiny.weights'

    # using more trained weights (lower frame rate, higher accuracies)
    model_config = 'yolov3.cfg'
    model_weights = 'yolov3.weights'

    network = cv2.dnn.readNetFromDarknet(model_config, model_weights)

    # use CPU
    network.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    network.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # use GPU (CUDA)
    #network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    #network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def find_objects(outputs, img):
        hT, wT, cT = img.shape
        bounding_box = []
        class_ids = []
        confidence_values = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > confidence_threshold:
                    width, height = int(detection[2] * wT), int(detection[3] * hT)
                    x, y = int(detection[0] * wT - width / 2), int(detection[1] * hT - height / 2)
                    bounding_box.append([x, y, width, height])
                    class_ids.append(class_id)
                    confidence_values.append(float(confidence))
                    

        indices = cv2.dnn.NMSBoxes(bounding_box, confidence_values, confidence_threshold, nms_threshold)

        for i in indices:
        
            # okay so i think this part is where the text is outputted
            box = bounding_box[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x + w, y + h), (100, 100, 255), 2)
            cv2.putText(img, f'{class_names[class_ids[i]]} {int(confidence_values[i] * 100)}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)
            

        # print(len(indices)) 

        if len(indices) > 2:
            print('PARTY TIME')
            return True
            
        else:
            return False


            # if class_names[class_ids[i]] != 'person':
            #     print('move foward a little bit')
            # else:
            #     print('stopped')
        


    while True:
        success, img = capture.read() 

        blob = cv2.dnn.blobFromImage(img, 1 / 255, (wh_target, wh_target), [0, 0, 0], 1, crop=False)
        network.setInput(blob)

        layer_names = network.getLayerNames()
        output_names = [layer_names[i - 1] for i in network.getUnconnectedOutLayers()]

        outputs = network.forward(output_names)

        find_obj = find_objects(outputs, img)

        # cv2.imshow('Camera', img)
        cv2.waitKey(1)
        
        return find_obj

if __name__ == "__main__":
    app.run(debug=True)