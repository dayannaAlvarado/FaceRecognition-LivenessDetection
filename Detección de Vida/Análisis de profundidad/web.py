
import face_recognition
import cv2
import numpy as np
import os
import glob

font = cv2.FONT_HERSHEY_DUPLEX
import keras
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv3D, MaxPooling3D
from keras import backend as K

model = Sequential()
model.add(Conv3D(32, kernel_size=(3, 3, 3), activation='relu',input_shape=(24,100,100,1)))
model.add(Conv3D(64, (3, 3, 3), activation='relu'))
model.add(MaxPooling3D(pool_size=(2, 2, 2)))
model.add(Conv3D(64, (3, 3, 3), activation='relu'))
model.add(MaxPooling3D(pool_size=(2, 2, 2)))
model.add(Conv3D(64, (3, 3, 3), activation='relu'))
model.add(MaxPooling3D(pool_size=(2, 2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))    
#model = get_liveness_model()
model.load_weights('model/model.py')
print("Loaded model from disk")


faces_encodings = []
faces_names = []
cur_direc = os.getcwd()
path = os.path.join(cur_direc, 'Data/faces/')
list_of_files = [f for f in glob.glob(path+'*.jpg')]
number_files = len(list_of_files)
names = list_of_files.copy()

for i in range(number_files):
    globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
    globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
    faces_encodings.append(globals()['image_encoding_{}'.format(i)])
# Create array of known names
    names[i] = names[i].replace(cur_direc+"\Data/faces", "")
    faces_names.append(names[i])
    #print(faces_names)

#Reconocimiento
face_locations = []
face_encodings = []
face_names = []
a=""
process_this_frame = True
input_vid = []
video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
            face_locations = face_recognition.face_locations( rgb_small_frame)
            face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces (faces_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance( faces_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                #print(best_match_index)
                if matches[best_match_index] == True:
                    name = faces_names[best_match_index]
                    name = name.split(".")
                    name = name[0]
                    #Livness detection
                    if len(input_vid) < 24:
                        liveimg = cv2.resize(frame, (100,100))
                        liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
                        #liveimg= rgb_small_frame
                        input_vid.append(liveimg)
                    else:
                        liveimg = cv2.resize(frame, (100,100))
                        liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
                        #liveimg= rgb_small_frame
                        input_vid.append(liveimg)
                        inp = np.array([input_vid[-24:]])
                        inp = inp/255
                        inp = inp.reshape(1,24,100,100,1)
                        pred = model.predict(inp)
                        input_vid = input_vid[-25:]
                        print(pred[0][0])
                        if pred[0][0]> .85:

                            a="LIVE"
                            print (a)
                        else:     
                            a="FAKE" 
                            print (a)
                    #Fin de livness detection
                    
                face_names.append(name)
    process_this_frame = not process_this_frame
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    # Display the resulting image
            if a == "LIVE":
                cv2.putText(frame, a, (460, 480), cv2.FONT_HERSHEY_COMPLEX, 0.9,(0, 255, 0), 3)
            else:
                cv2.putText(frame, a, (460, 480), cv2.FONT_HERSHEY_COMPLEX, 0.9,(0, 0, 255), 3)
    
    cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
