import cv2
import os
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
from matplotlib.patches import Rectangle
from numpy import asarray
from PIL import Image
from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
from scipy.spatial.distance import cosine

video=cv2.VideoCapture(0)

facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

count=0

def extract_face_from_image(image_path, required_size=(224, 224)):
    # load image and detect faces
    image = plt.imread(image_path)

    detector = MTCNN()
    faces = detector.detect_faces(image)

    # extract the bounding box from the requested face
    x1, y1, width, height = faces[0]['box']
    x2, y2 = x1 + width, y1 + height

    # extract the face
    face_boundary = image[y1:y2, x1:x2]

    image = cv2.resize(face_boundary, required_size)
    print(image)
    return image

def get_model_scores(faces):
  samples = asarray(faces, 'float32')

  # prepare the data for the model
  samples = preprocess_input(samples, version=2)

  # create a vggface model object
  model = VGGFace(model='resnet50',
      include_top=False,
      input_shape=(224, 224, 3),
      pooling='avg')

  # perform prediction
  return model.predict(samples)

def capture(count):
	while True:
		ret,frame=video.read()
        #scale factor = 1.3 neighbours = 5-
		faces=facedetect.detectMultiScale(frame,1.3, 5)
		for x,y,w,h in faces:
			count=count+1
			name="./images1/"+str(count) + '.jpg'
			print("Creating Images........." +name)
			cv2.imwrite(name, frame[y:y+h,x:x+w])
			cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
		cv2.imshow("WindowFrame", frame)
		cv2.waitKey(1)
		if count>1:
			break
	video.release()
	cv2.destroyAllWindows()


def compare(path1 ,path2): 
    faces = [extract_face_from_image(image_path)for image_path in [path1, path2]]
    model_scores = get_model_scores(faces)

    if cosine(model_scores[0], model_scores[1]) <= 0.5:
        print("Faces Matched")
        return 1
    else:
        print("Not matched")
        return 0
	

def face_check():
    capture(0)
    directory1 = 'images1/'
    directory2 = 'images/'
    for filename1 in os.listdir(directory1):
        i = os.path.join(directory1, filename1)
        if 1:
            print(i)
            for filename2 in os.listdir(directory2):
                j = os.path.join(directory2, filename2)
                if os.path.isfile(j) and filename2.endswith('.jpg'):
                    print(j)
                    result = compare(i, j)
                    if result == 1:
                        print(i, j)
                        j = j.split("images/",1)[1]
                        j = j.split(".")[0]
                        return str(j)
    return 0