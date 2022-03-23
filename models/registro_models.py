from odoo import models, fields, api
import face_recognition
import logging
import numpy as np
import os
import glob
import random
import cv2
import socket
from IPython.display import display, Javascript
from IPython.core.display import display, HTML
from base64 import b64decode
import js2py
import imutils
import http
import http.server
import socketserver
from time import sleep
import cv2
import threading
from datetime import datetime



name = "known"
_logger = logging.getLogger(__name__)
reconocer = 0

font = cv2.FONT_HERSHEY_DUPLEX
import keras
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv3D, MaxPooling3D
from keras import backend as K


class AsistenciasRegistro(models.Model):
    parpadeos = random.randint(1, 6)
    c = ""
    _name = 'asistencias.registro'
    id = fields.Integer(String="Id")
    fecha = fields.Datetime(
        string=u'Fecha y Hora',

        #default=lambda *a: datetime.now()
        #default=fields.datetime.now.strftime(DATETIME_FORMAT)
        )
    estudiante_name = fields.Many2one('asistencias.estudiante', 'Usuario')
    nombre_estudiante = fields.Char('Nombre del estudiante')
    apellido_estudiante = fields.Char('Apellido del estudiante')
    laboratorio_name = fields.Char('Laboratorio')
    usuario = fields.Char(string="Identificación del Estudiante")
    horas_usadas =fields.Float(string="Horas Usadas")
    _rec_name = "id"


    def action_reconocer(self):
        print(socket.gethostbyname(socket.gethostname()))
        faces_encodings = []
        print("RECONOCIENDOO--------------")
        faces_names = []
        a=""
        cur_direc = os.getcwd()
        path = os.path.join(cur_direc, 'odoo/addons/asistencias/images/')
        list_of_files = [f for f in glob.glob(path + '*.jpg')]
        number_files = len(list_of_files)
        names = list_of_files.copy()
        for i in range(number_files):
            globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
            globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[
                0]
            faces_encodings.append(globals()['image_encoding_{}'.format(i)])
            # Create array of known names
            names[i] = names[i].replace(cur_direc+  "\\odoo/addons/asistencias/images\\", "")
            faces_names.append(names[i])
        # Reconocimiento
        face_locations = []
        face_encodings = []
        face_names = []
        input_vid= []
        process_this_frame = True
        video_capture = cv2.VideoCapture(0)
        #video_capture= videos
        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if ret == False:
                break
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(faces_encodings, face_encoding)
                    name = "Unknown"
                    face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index] == True:
                        name = faces_names[best_match_index]
                        nuevo = name.split(".")
                        nuevo = nuevo[0]
                        if self.c != nuevo:
                          self.action_asigna(nuevo)
                    face_names.append(name)
            process_this_frame = not process_this_frame
            cont = 0
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                cont += 1
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                font = cv2.FONT_HERSHEY_DUPLEX
                if name == "Unknown":
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    # Input text label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    cv2.putText(frame, "NO REGISTRADO", (400, 480), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 255), 2)
                else :
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    # Input text label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, nuevo, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    cv2.putText(frame, "REGISTRADO", (400, 480), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                '''if a == "LIVE DETECTED":
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    # Input text label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, str(name.split(".")[0]), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    cv2.putText(frame, "REGISTRADO", (460, 480), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                if a == "WAARRNING":
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    # Input text label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, str(name.split(".")[0]), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    cv2.putText(frame, "FAKE FACE", (460, 480), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 255), 2)'''
                # Display the resulting image
            cv2.imshow('Iframe', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video_capture.release()
        cv2.destroyAllWindows()
    def captura(self):
        js1 = """
                import browserEnv from 'browser-env';
                browserEnv(['navigator']);
                console.log( "Hello World!" )
                const videos= document.getElementById("videoElement")
                                    navigator.mediaDevices.getUserMedia({video:true})
                                    .then(
                                        (stream)=>{
                                            videos.srcObject=stream;
                                            console.log("stream")

                                            return videos
                                            }
                                        )
                                    .catch((error)=>{
                                        console.log(error);}
                                    )
        """
        js2py.eval_js6(js1)
    def action_asigna(self, nuevo):
        print("ASIGNADOOO")
        #fech_=time.asctime(time.localtime()).strftime('%Y-%m-%dT%H:%M:%SZ')
        #fech_ = (lambda self: fields.datetime.now())
        self.c = nuevo
        # print("c de asiganr = "+ self.c)
        # self.write({'usuario': x})
        records = self.env['asistencias.estudiante'].search([])
        # print(records[1])
        for record in records:
            # print(record)
            if record['identificacion'] == nuevo:
                # self.write({ 'usuario': x,'nombre_estudiante': record['nombres'] ,'apellido_estudiante': record['apellidos']})
                self.env['asistencias.registro'].create({
                    'nombre_estudiante': record['nombres'],
                    'apellido_estudiante': record['apellidos'],
                    'usuario': nuevo,
                    'fecha': datetime.now(),
                    'laboratorio_name': "Laboratorio de Software"})
