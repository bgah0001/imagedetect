import cv2
import numpy as np

class ObjectDetector:
    def __init__(self):
        self.classes = self.loadClasses()
        self.output_layers = self.loadYolo()

    def loadYolo(self):
        self.yolo = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
        
        layer_names = self.yolo.getLayerNames()

        return [layer_names[i - 1] for i in self.yolo.getUnconnectedOutLayers()]
        
      
    def loadClasses(self):
        with open("coco.names", "r") as f:
            return [line.strip() for line in f.readlines()]
        
    def loadImage(self, img):
        return cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
       
    
    def detectImage(self, img):
        blob = self.loadImage(img)
        #Detecting objects
        self.yolo.setInput(blob)
        outs = self.yolo.forward(self.output_layers)
        objects = []
        height, width, channels = img.shape
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    object = {
                        "label":self.classes[class_id],
                        "accuracy":float(confidence),
                        "rectangle":[x, y, w, h]
                    }
                    objects.append(object)
        return objects           