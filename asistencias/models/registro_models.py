import glob , logging, os, cv2, face_recognition
from datetime import datetime
import numpy as np
from odoo import models, fields

name = "known"
_logger = logging.getLogger(__name__)
reconocer = 0

font = cv2.FONT_HERSHEY_DUPLEX
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv3D, MaxPooling3D

ROOT = os.path.dirname(__file__)

def livness():
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
    model.load_weights('C:/Program Files (x86)/Odoo 13.0/server/odoo/addons/asistencias/models/model.py')
    return model
    print("Loaded model from disk")

class AsistenciasRegistro(models.Model):
    c = ""
    nueva_materia= 1
    _name = 'asistencias.registro'
    id = fields.Integer(String="Id")
    fecha = fields.Datetime(string="Fecha", auto_now_add=True)
    estudiante_name = fields.Many2one('asistencias.estudiante', 'Usuario')
    nombre_estudiante = fields.Char('Nombres Y Apellidos')
    laboratorio_name = fields.Char('Laboratorio')
    usuario = fields.Char(string="Identificación")
    ciclo_estudiante = fields.Char('Ciclo')
    paralelo_estudiante = fields.Char('Paralelo')
    materia_estudiante = fields.Char('Materia')
    rol= fields.Char('Rol')
    horas_usadas =fields.Float(string="Horas Usadas")
    _rec_name = "id"

    def action_reconocer(self):
        faces_encodings = []
        registros = self.env['asistencias.registro'].search([])
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
            globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
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
        #video_capture = cv2.VideoCapture('rtsp://admin1:admin1@192.168.100.190:554/stream2')
        video_capture = cv2.VideoCapture(0)
        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if ret == False:
                print("Sin videoo")
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
                        # Livness detection
                        if len(input_vid) < 24:
                            liveimg = cv2.resize(frame, (100, 100))
                            liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
                            input_vid.append(liveimg)
                        else:
                            liveimg = cv2.resize(frame, (100, 100))
                            liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
                            input_vid.append(liveimg)
                            inp = np.array([input_vid[-24:]])
                            inp = inp / 255
                            inp = inp.reshape(1, 24, 100, 100, 1)
                            pred = livness().predict(inp)
                            input_vid = input_vid[-25:]
                            print(pred[0][0])
                            if pred[0][0] > .40:
                                a = "LIVE DETECTED"
                                print(a)
                                for registro in registros:
                                    if registro['usuario'] == nuevo:
                                        lapso =datetime.timestamp(datetime.now()) - datetime.timestamp(registro['fecha'])
                                        if lapso > 5:
                                            self.nueva_materia= 1
                                        else:
                                            self.nueva_materia= 0
                                if self.c != nuevo and self.nueva_materia==1:
                                    self.action_asigna(nuevo)
                            else:
                                a = "WAARRNING"
                                print(a)
                        # Fin de livness detection

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
                    cv2.putText(frame, "DESCONOCIDO", (400, 480), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 255), 2)
                else:
                    if a == "LIVE DETECTED":
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        # Input text label with a name below the face
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                        cv2.putText(frame, str(name.split(".")[0]), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                        cv2.putText(frame, "REGISTRADO", (460, 480), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                    else:
                        if a == "WAARRNING":
                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                            # Input text label with a name below the face
                            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                            cv2.putText(frame, str(name.split(".")[0]), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                            cv2.putText(frame, "FAKE FACE", (460, 480), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 255), 2)
                # Display the resulting image
            cv2.imshow('Iframe', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                for registro in registros:
                   if registro['nombre_estudiante'] == 0:
                      print("BORRANDO DATOS")
                      registro.unlink()
                break
        video_capture.release()
        cv2.destroyAllWindows()

    def action_asigna(self, nuevo):
        print("ASIGNADOOO")
        self.c = nuevo
        estudiantes = self.env['asistencias.estudiante'].search([])
        docentes = self.env['asistencias.docente'].search([])
        for estudiante in estudiantes:
            if estudiante['identificacion'] == nuevo:
                self.env['asistencias.registro'].create({
                    'nombre_estudiante': str(estudiante['nombres'])+" " +str(estudiante['apellidos']),
                    'usuario': nuevo,
                    'ciclo_estudiante': estudiante['ciclo'],
                    'rol': "Estudiante",
                    'paralelo_estudiante': estudiante['paralelo'],
                    'materia_estudiante': estudiante['materia_name'],
                    'fecha': datetime.strftime(fields.Datetime.context_timestamp(self, datetime.now()), "%Y-%m-%d %H:%M:%S"),
                    'laboratorio_name': "Laboratorio de Software"})
        for docente in docentes:
            if docente['identificacion'] == nuevo:
                self.env['asistencias.registro'].create({
                    'nombre_estudiante': docente['nombres'],
                    'usuario': nuevo,
                    'rol': "Docente",
                    'ciclo_estudiante': '- -',
                    'paralelo_estudiante': '- -',
                    'materia_estudiante': '- -',
                    'fecha': datetime.strftime(fields.Datetime.context_timestamp(self, datetime.now()), "%Y-%m-%d %H:%M:%S"),
                    'laboratorio_name': "Laboratorio de Software"})







