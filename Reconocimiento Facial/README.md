### MODELOS PREENTRENADOS EIGEN-FACE, FISHER-FACE Y LBPH-FACE

* Los modelos preentrenados Eigen-Face, Fisher-Face y LBPH-Face son útiles para realizar reconocimiento facial, estos requieren _aprender_ las carácteristicas faciales de los usuarios del sistema, por tanto se requiere una base de datos con almenos 300 fotogramas por cada individuo.
* El código respectivo para facilitar la captura de mencionados fotogramas está en el archivo **_captura.py_**, al ejecutar el archivo se abrirá la cámara del computador, el usuario deberá colocarse frente al punto de captura y realizar diversos gestos, estos fotogramas serán almacenados dentro del directorio **_Data/Nombre del Usuario/_**. Para que se pueda capturar los rostros se necesita un modelo de detección de rostro, para ello se utilza en modelo preentrenado haarcascade disponible en el archivo **_haarcascade_frontalface_default.xml_**.
* Posteriormente se deberá entrenar cada uno de los modelos con la base de datos construida, para ello, se requiere ejecutar el archivo **_Entrenamiento.py_** disponible dentro de los directorios de cada modelo. Al concluir el entrenamiento automaticamente se creará un archivo **_.xml_** con el nombre del modelo que se esté entrenando. Este último archivo contiene la codificación facial de cada uno de los rostros de la base de datos.
* Finalmente ejecutar el archivo **_reconocimiento.py_** disponible dentro del directorio de cada modelo de reconocimiento. Se abrirá la cámara del computador y se podrá realizar el reconocimiento facial.

### MODELO PREENTRENADO FACE-RECOGNITION.
* El modelo preentrenado Face-Recognition requiere tener una base de datos que contenga únicamente una fotografía de cada usuario.
* Este modelo ya incluye un detector facial, por tanto no es necesario ejecutar uno externo.
* Para realizar el reconocimiento de rostros ejecutar el archivo **_reconocer.py_**.
