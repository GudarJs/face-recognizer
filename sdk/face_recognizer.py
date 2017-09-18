# facerec.py
import cv2, os
import numpy as np
import base64
import cStringIO
from PIL import Image

fn_haar = 'sdk/classifiers/haarcascade_frontalface_default.xml'
fn_dir = 'sdk/face_data'

def read_images():
    # Create a list of images and a list of corresponding names
    (names, id) = ({}, 0)
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

            id += 1

    return names

def decode_image(base64_string):
    im_string = cStringIO.StringIO(base64.b64decode(base64_string.split(',')[1]))
    im = Image.open(im_string)
    npimg = np.asarray(im)
    return npimg

def recognize(model, names, frame):
    haar_cascade = cv2.CascadeClassifier(fn_haar)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    (im_width, im_height) = (112, 92)
    size = 2

    # Flip the image (optional)
    frame=cv2.flip(frame,1,0)

    # # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
    
    faces = haar_cascade.detectMultiScale(mini)
    for i in range(len(faces)):
        face_i = faces[i]
        (x, y, w, h) = [v * size for v in face_i]
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))
        
        # Try to recognize the face
        prediction = model.predict(face_resize)
        
        cara = '%s' % (names[prediction[0]])
        if(prediction[1]/10 < 500):
            return names[prediction[0]]
        else:
            return 'Desconocido'
