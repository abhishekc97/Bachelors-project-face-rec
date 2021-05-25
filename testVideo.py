import os
import dlib
import cv2
import numpy as np


PREDICTOR_PATH = '../models/shape_predictor_68_face_landmarks.dat'
FACE_RECOGNITION_MODEL_PATH = '../models/dlib_face_recognition_resnet_model_v1.dat'
SKIP_FRAMES = 10
THRESHOLD = 0.5

faceDetector = dlib.get_frontal_face_detector()
shapePredictor = dlib.shape_predictor(PREDICTOR_PATH)
faceRecognizer = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL_PATH)

index = np.load('index.pkl')
faceDescriptorsEnrolled = np.load('descriptors.npy')

cam = cv2.VideoCapture(0)
count = 0
while True:
  
  success, im = cam.read()

  if not success:
    print ('cannot capture input from camera')
    break


  if (count % SKIP_FRAMES) == 0:

   
    img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    faces = faceDetector(img, 1)

    for face in faces:

      shape = shapePredictor(img, face)

      
      x1 = face.left()
      y1 = face.top()
      x2 = face.right()
      y2 = face.bottom()

      faceDescriptor = faceRecognizer.compute_face_descriptor(img, shape)

      faceDescriptorList = [m for m in faceDescriptor]
      faceDescriptorNdarray = np.asarray(faceDescriptorList, dtype=np.float64)
      faceDescriptorNdarray = faceDescriptorNdarray[np.newaxis, :]

      distances = np.linalg.norm(faceDescriptorsEnrolled - faceDescriptorNdarray, axis=1)

      argmin = np.argmin(distances)  
      minDistance = distances[argmin]  

      
      if minDistance <= THRESHOLD:
        label = os.path.splitext(os.path.basename(index[argmin].split('_')[0]))[0]
        #label = os.path.split("/")[-2]
      else:
        label = 'unknown'

     
      cv2.rectangle(im, (x1, y1), (x2, y2), (0, 0, 255))

      
      center = (int((x1 + x2)/2.0), int((y1 + y2)/2.0))
      radius = int((y2-y1)/2.0)
      color = (0, 255, 0)
      cv2.circle(im, center, radius, color, thickness=1, lineType=8, shift=0)

      
      org = (int(x1), int(y1))  
      font_face = cv2.FONT_HERSHEY_SIMPLEX
      font_scale = 0.8
      text_color = (255, 0, 0)
      printLabel = '{} {:0.4f}'.format(label, minDistance)
      cv2.putText(im, printLabel, org, font_face, font_scale, text_color, thickness=2)

    
    cv2.imshow('webcam', im)
  
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break  

  
  count += 1
cam.release()
cv2.destroyAllWindows()
