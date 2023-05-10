# Prototipo de reconocimiento facial con detección de vida para el registro de asistencias en el laboratorio de software de CIS/C UNL.

![registrado](https://github.com/Computacion-UNL/FaceRecognition-LivenessDetection/assets/46323169/8a028adb-6e73-4091-82e7-c9a3b0f2fa32)

------------
## Tabla de Contenidos:
- [Autor](#autor)
- [Descripción y Contexto](#descripción-y-contexto)
- [Información adicional](#información-adicional)

## Autor:
El presente Trabajo de Titulación fue desarrollado por:
- Dayanna Magdalla Alvarado Castillo - dayanna.alvarado@unl.edu.ec

Con la dirección de:
- Ing. Oscar Miguel Cumbicus Pineda, Mg. Sc. - oscar.cumbicus@unl.edu.ec

## Descripción y Contexto:
El presente repositorio contiene el código del proyecto de Titulación denominado **"Prototipo de reconocimiento facial con detección de vida para el registro de asistencias en el laboratorio de software"** de la Carrera de Ingeniería en Sistemas/Computación de la Universidad Nacional de Loja.

El repositorio se compone de 3 directorios: 
1. **Detección de vida:**  
Esta carpeta contiene los modelos con los que se experimentó la detección de vida, se presenta el modelo desarrollado para el análisis de profundidad y el contador de parpadeos.  

    **Análisis de porfundidad**  
    
        - El método de análisis de profundidad es un modelo de detección de vida siguiendo un enfoque pasivo, en el cual no es necesario que el usuario interactuaé con el sistema.
        - Ejecutar el archivo profundidad.py, en el cual se almacena el código correspondiente.
        - Ejemplos de pruebas realizadas se presenta en el archivo TEST.md

   **Contador de parpadeos**  
   
        - El modelo contador de parpadeos pretende ser un modelo de detección de vida siguiendo un enfoque activo, en el cual el usuario deberá interactuar con el sistema. El modelo solicita al usuario un número de parpadeos cada vez aleatorio, el usuario deberá parpadear las veces correspondientes, si se cumplen, se considerará al usuario como individuo en tiempo real frente al punto de captura, si no se cumplen o se exceden se considerará como ataque de presentación.Todo esto dado que, mediante la presentación de una fotografía frente al punto de captura esta no efectuará la acción solicitada, y en caso de ser un video, este no responderá al número exacto solicitado ya que el número que se solicita es randómico.
        - Ejecutar el archivo contador.py, en el cual se almacena el código correspondiente. 
        - Ejemplos de pruebas realizadas se presenta en el archivo TEST.md
 
2. **Reconocimiento facial:** Esta carpeta contiene los modelos Eigen-Face, Fisher-Face, LBPH-Face y Face-recognition, con los que se experimentó el reconocimiento facial.

      **Modelos preentrenados Eigen-Face, Fisher-Face y LBPH-Face**

      * Los modelos preentrenados Eigen-Face, Fisher-Face y LBPH-Face son útiles para realizar reconocimiento facial, estos requieren _aprender_ las carácteristicas faciales de los usuarios del sistema, por tanto se requiere una base de datos con almenos 300 fotogramas por cada individuo.
      * El código respectivo para facilitar la captura de mencionados fotogramas está en el archivo **_captura.py_**, al ejecutar el archivo se abrirá la cámara del computador, el usuario deberá colocarse frente al punto de captura y realizar diversos gestos, estos fotogramas serán almacenados dentro del directorio **_Data/Nombre del Usuario/_**. Para que se pueda capturar los rostros se necesita un modelo de detección de rostro, para ello se utilza en modelo preentrenado haarcascade disponible en el archivo **_haarcascade_frontalface_default.xml_**. Un ejemplo de la creación de a BD se presenta a continuación.

      ![WhatsApp Image 2022-03-19 at 2 06 19 AM](https://user-images.githubusercontent.com/46323169/159111369-3bf2fd48-7ad1-4110-a807-8e03c228bd7f.jpeg)

      * Posteriormente se deberá entrenar cada uno de los modelos con la base de datos construida, para ello, se requiere ejecutar el archivo **_Entrenamiento.py_** disponible dentro de los directorios de cada modelo. Al concluir el entrenamiento automaticamente se creará un archivo **_.xml_** con el nombre del modelo que se esté entrenando. Este último archivo contiene la codificación facial de cada uno de los rostros de la base de datos.
      * Finalmente ejecutar el archivo **_reconocimiento.py_** disponible dentro del directorio de cada modelo de reconocimiento. Se abrirá la cámara del computador y se podrá realizar el reconocimiento facial.

    **Modelo preentrenado Face-Recognition.**
      * El modelo preentrenado Face-Recognition requiere tener una base de datos que contenga únicamente una fotografía de cada usuario.
      * Para crear la base de datos crear un directorio **_Data/faces/_** dentro de esta carperta incluir las fotografías identificadas según el nombre del isuario. Un ejemplo se presenta en la figura a continuación.
      
      ![WhatsApp Image 2022-03-19 at 1 58 45 AM](https://user-images.githubusercontent.com/46323169/159111125-13c98277-fbac-492c-a591-64080d67f89f.jpeg)
      

      * Este modelo ya incluye un detector facial, por tanto no es necesario ejecutar uno externo.
      * Para realizar el reconocimiento de rostros ejecutar el archivo **_reconocer.py_**.


4. **Asistencias:** Este directorio almacena el módulo web de registro de asistencias con reconocimiento facial y detección de vida, desarrollado en Odoo v13, se trata del prototipo final que contiene el modelo Face-Recognition y el modelo de análisis de profundidad.


## Información adicional: 
Para conocer más de Odoo ingrese a https://www.odoo.com/es_ES/  

Para acceder a la documentación de Desarrolladores de Odoo ingrese a https://www.odoo.com/documentation/13.0/

Para instruirse en el desarrollo en Framework Odoo ingrese a https://escuelafullstack.com/slides/curso-de-odoo-13-framework-backend-2
