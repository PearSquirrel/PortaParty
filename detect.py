
import cv2
import numpy as np

#ENV
# api key = NjEzZDA4MjI0YjIzYmM0NGJkNjU5ZDlhNzZkZDEzODk4MmYzNzE3OGFiZjc4OWZhMThhYzE5MjQ=
# vehicleId= r4EeYcnz
# token = 60ac081f527e8baab8ac3bae078d1922d34cfd2e

class ObjectDetection():
    def __init__(self):
        self.wh_target = 320
        self.confidence_threshold = 0.8
        self.nms_threshold = 0.3

        class_file = 'class.names'
        self.class_names = []

        with open(class_file, 'rt') as f:
            self.class_names = f.read().rstrip('\n').split('\n')

        # tiny weights (higher frame rate, lower accuracies)
        #model_config = 'yolov3-tiny.cfg'
        #model_weights = 'yolov3-tiny.weights'

        # using more trained weights (lower frame rate, higher accuracies)
        model_config = 'yolov3.cfg'
        model_weights = 'yolov3.weights'

        self.network = cv2.dnn.readNetFromDarknet(model_config, model_weights)

        # use CPU
        self.network.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.network.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # use GPU (CUDA)
        #self.network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        #self.network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def _find_objects(self, outputs, img):
        hT, wT, cT = img.shape
        bounding_box = []
        class_ids = []
        confidence_values = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.confidence_threshold:
                    width, height = int(detection[2] * wT), int(detection[3] * hT)
                    x, y = int(detection[0] * wT - width / 2), int(detection[1] * hT - height / 2)
                    bounding_box.append([x, y, width, height])
                    class_ids.append(class_id)
                    confidence_values.append(float(confidence))
                    

        indices = cv2.dnn.NMSBoxes(bounding_box, confidence_values, self.confidence_threshold, self.nms_threshold)
        
        # Only look for people
        indices = [i for i in indices if self.class_names[class_ids[i]] == 'person']
        
        objects = []
        for i in indices:
            # okay so i think this part is where the text is outputted
            box = bounding_box[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x + w, y + h), (100, 100, 255), 2)
            cv2.putText(img, f'{self.class_names[class_ids[i]]} {int(confidence_values[i] * 100)}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)
        
            objects.append({
                'name': self.class_names[class_ids[i]],
                'confidence': confidence_values[i],
                'x': x,
                'y': y,
                'width': w,
                'height': y,
            })

        return objects


    def get_detected_objects(self, image):
        image = np.array(image.convert('RGB')) 
        blob = cv2.dnn.blobFromImage(image, 1 / 255, (self.wh_target, self.wh_target), [0, 0, 0], 1, crop=False)
        self.network.setInput(blob)

        layer_names = self.network.getLayerNames()
        output_names = [layer_names[i - 1] for i in self.network.getUnconnectedOutLayers()]

        outputs = self.network.forward(output_names)

        detected_objects = self._find_objects(outputs, image)

        # cv2.imshow('Camera', img)
        # cv2.waitKey(10)
        # cv2.destroyAllWindows()
        
        return detected_objects

# ObjectDetection().run_object_detection()




# capture = cv2.imread(image, flags=cv2.IMREAD_COLOR)
        # img_array = np.asarray(bytearray(image), dtype=np.uint8)
        # capture = cv2.imdecode(img_array, 0)
        # nparr = np.fromstring(image, np.uint8)
        # capture = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        jpg_as_np = np.asarray(bytearray())
        capture = cv2.imdecode(jpg_as_np, flags=1)
        # capture = cv2.imread(capture)

        # print(capture)