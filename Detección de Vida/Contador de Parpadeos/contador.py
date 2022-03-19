import cv2
import mediapipe as mp
import numpy as np
import random

def drowing_output(frame, coordinates_left_eye, coordinates_right_eye, blink_counter):
    msj = ""
    aux_image= np.zeros(frame.shape, np.uint8)
    output = cv2.addWeighted(frame, 1, aux_image,0.7,1)
    if (blink_counter< parpadeos):
        cv2.putText(output, "Num. Parpadeos: ", (10,30), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),2)
        cv2.putText(output, "{}".format(blink_counter), (220, 35), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0), 3)
        cv2.putText(output, "Parpadear: " + "{}".format(parpadeos) + " Veces", (10, 300), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                    (0,255,0), 2)
    if(blink_counter>parpadeos):
        cv2.putText(output, "Parpadeos Excedidos", (10,50), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0,0,255),2)
    if(blink_counter==parpadeos):
        cv2.putText(output, "REAL", (10,50), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),2)
    return output

def eye_aspect_ratio(coordinates):
    d_A= np.linalg.norm(np.array(coordinates[1])-np.array(coordinates[5]))
    d_B= np.linalg.norm(np.array(coordinates[2])-np.array(coordinates[4]))
    d_C= np.linalg.norm(np.array(coordinates[0])-np.array(coordinates[3]))
    return (d_A +d_B)/(2*d_C)

cap = cv2.VideoCapture(0)
mp_face_mesh = mp.solutions.face_mesh
index_left_eye= [33,160,158,133,153,144]
index_right_eye= [362,385,387,263,373,380]
EAR_THRESH = 0.24
aux_counter=0
NUM_FRAMES = 3
blink_counter=0
parpadeos = random.randint(1, 5)

#parpadeos= 3
with mp_face_mesh.FaceMesh(
    static_image_mode= False,
    max_num_faces=1)as face_mesh:
    while True:
        ret, frame = cap.read()
        if ret ==False:
            break
        frame = cv2.flip(frame, 1)
        height,width, _ = frame.shape
        frame_rgb= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results= face_mesh.process(frame_rgb)
        coordinates_left_eye=[]
        coordinates_right_eye = []
        if results.multi_face_landmarks is not  None:
            for face_landmarks in results.multi_face_landmarks:
                for index in index_left_eye:
                    x= int(face_landmarks.landmark[index].x * width)
                    y= int(face_landmarks.landmark[index].y * height)
                    coordinates_left_eye.append([x,y])
                    cv2.circle(frame, (x, y), 2, (128, 0, 250), 1)
                for index in index_right_eye:
                    x= int(face_landmarks.landmark[index].x * width)
                    y= int(face_landmarks.landmark[index].y * height)
                    coordinates_right_eye.append([x, y])
                    cv2.circle(frame, (x,y),2,(128,0,250),1)
            ear_left_eye=eye_aspect_ratio(coordinates_left_eye)
            ear_righ_eye= eye_aspect_ratio(coordinates_right_eye)
            ear = (ear_righ_eye+ear_left_eye)/2
            #ojos cerrados
            if ear < EAR_THRESH:
                aux_counter +=1
            else:
                if aux_counter>=NUM_FRAMES:
                    aux_counter=0
                    blink_counter+=1
                    #print(blink_counter)
            frame= drowing_output(frame, coordinates_left_eye, coordinates_right_eye, blink_counter)
        cv2.imshow("Frame", frame)
        k= cv2.waitKey(1) & 0xFF
        if k==27:
            break
cap.release()
cv2.destroyAllWindows()
