import cv2
import numpy as np
import dlib
import os
import _pickle as cPickle


 
PREDICTOR_PATH = '../models/shape_predictor_68_face_landmarks.dat'
FACE_RECOGNITION_MODEL_PATH = '../models/dlib_face_recognition_resnet_model_v1.dat'

faceDetector = dlib.get_frontal_face_detector()
shapePredictor = dlib.shape_predictor(PREDICTOR_PATH)
faceRecognizer = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL_PATH)


faceDatasetFolder = '../data/faces'

subfolders = []
for x in os.listdir(faceDatasetFolder):       
  xpath = os.path.join(faceDatasetFolder, x)  
  if os.path.isdir(xpath):            
    subfolders.append(xpath)    
#print(subfolders)

nameLabelMap = {}
labels = []
imagePaths = []
for i, subfolder in enumerate(subfolders):    
  for x in os.listdir(subfolder):             
    xpath = os.path.join(subfolder, x)        
    if x.endswith('jpg'):                    
      imagePaths.append(xpath)               
      labels.append(i) 
      nameLabelMap[x] = subfolder


#nlm = nameLabelMap
#print(nlm)
#labs = labels
#print(labs)
#ips = imagePaths
#print(ips)



index = {}
i = 0
faceDescriptors = None
for imagePath in imagePaths:
  print("processing: {}".format(imagePath))
  
  img = cv2.imread(imagePath)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  
  faces = faceDetector(img, 1)

  
  for k, face in enumerate(faces):

    shape = shapePredictor(img, face)
  
    landmarks = [(p.x, p.y) for p in shape.parts()]

    faceDescriptor = faceRecognizer.compute_face_descriptor(img, shape)

    faceDescriptorList = [x for x in faceDescriptor]
    faceDescriptorNdarray = np.asarray(faceDescriptorList, dtype=np.float64)
    faceDescriptorNdarray = faceDescriptorNdarray[np.newaxis, :]

    
    if faceDescriptors is None:
      faceDescriptors = faceDescriptorNdarray
    else:
      faceDescriptors = np.concatenate((faceDescriptors, faceDescriptorNdarray), axis=0)

    index[i] = imagePath
    i += 1


np.save('descriptors.npy', faceDescriptors)
with open('index.pkl', 'wb') as f:
  cPickle.dump(index, f)
