import cv2, os
import numpy as np

size = 4
(im_width, im_height) = (112, 92)
fn_haar = 'sdk/classifiers/haarcascade_frontalface_default.xml'
eyes_har = 'sdk/classifiers/haarcascade_eye.xml'
fn_dir = 'sdk/face_data'

def read_images():
    print('Training...')

    # Create a list of images and a list of corresponding names
    (images, lables, names, id) = ([], [], {}, 0)
    # Get the folders containing the training data
    for (subdirs, dirs, files) in os.walk(fn_dir):
        # Loop through each folder named after the subject in the photos
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(fn_dir, subdir)

            # Loop through each photo in the folder
            for filename in os.listdir(subjectpath):

                # Skip non-image formates
                f_name, f_extension = os.path.splitext(filename)
                if(f_extension.lower() not in
                        ['.png','.jpg','.jpeg','.gif','.pgm']):
                    print( "Skipping " + filename + ", wrong file type" )
                    continue
                path = subjectpath + '/' + filename
                lable = id

                # Add to training data
                images.append(cv2.imread(path, 0))
                lables.append(int(lable))
            id += 1

    # Create a Numpy array from the two lists above
    (images, lables) = [np.array(lis) for lis in [images, lables]]

    return (images, lables)

name = raw_input('Please enter a name: ')
path = 'sdk/face_data/' + name

if not os.path.isdir(path):
      os.mkdir(path)
      
haar_cascade = cv2.CascadeClassifier(fn_haar)
eye_cascade = cv2.CascadeClassifier(eyes_har)

webcam = cv2.VideoCapture(0) #'0' is use for my webcam, if you've any other
#camera attached use '1' like this
pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path)
if n[0]!='.' ]+[0])[-1] + 1

# The program loops until it has 50 images of the face.
count = pin
samples = 0 
while samples < 50:
    (rval, im) = webcam.read()

    im = cv2.flip(im, 1, 0)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    mini = cv2.resize(gray, (gray.shape[1] / size, gray.shape[0] / size))

    faces = haar_cascade.detectMultiScale(mini)
    faces = sorted(faces, key=lambda x: x[3])
    
    if faces:
        face_i = faces[0]
        (x, y, w, h) = [v * size for v in face_i]

        face = gray[y:y + h, x:x + w]
        face_color = im[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))

        eyes = eye_cascade.detectMultiScale(face)

        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
            if ey < h / 2:
                cv2.rectangle(face_color,(ex,ey),(ex+ew,ey+eh),(140,255,0),2)
            cv2.putText(im, name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0)) 

            if len(eyes) > 2 :
 				cv2.imwrite('%s/%s.pgm' % (path, count), face_resize)
				count += 1
				samples += 1
       
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(100)
    if key == 27:
      break

cv2.destroyAllWindows()
model = cv2.face.createLBPHFaceRecognizer()
(images, labels) = read_images()
model.train(images, labels)
model.save('sdk/training/face_training.yml')
