import cv2
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from keras.models import load_model
import keras as keras

def load_frames(participante):
    lista_frames,lista_yaw,lista_pitch,lista_roll=read_landmarks_frames(participante)

    lista_frames=min_max_scale_coordinates(lista_frames)

    # Crear un objeto StandardScaler
    scaler = StandardScaler()
    # Escalar los datos de yaw
    lista_yaw= scaler.fit_transform(np.array(lista_yaw).reshape(-1, 1))
    # Escalar los datos de pitch
    lista_pitch= scaler.fit_transform(np.array(lista_pitch).reshape(-1, 1))
    # Escalar los datos de roll
    lista_roll =scaler.fit_transform(np.array(lista_roll).reshape(-1, 1))

    # Combinar todos los datos en un solo objeto
    datos_participante = {
        "frames": lista_frames,
        "yaw": lista_yaw,
        "pitch": lista_pitch,
        "roll": lista_roll
    }

    return datos_participante


def read_landmarks_frames(participante):
    lista_frames = []  # Lista para almacenar todos los frames de un participante
    lista_yaw = []  # Lista para almacenar el yaw de cada frame
    lista_pitch = []  # Lista para almacenar el pitch de cada frame
    lista_roll = []  # Lista para almacenar el roll de cada frame
    participante = participante.strip('"')
    ruta_carpeta = os.path.join('', participante)
    archivos = os.listdir(ruta_carpeta)
    
    for archivo in archivos:
        if 'Landmarks' in archivo:
            ruta_subcarpeta = os.path.join(ruta_carpeta, archivo)
            break
    
    subcarpeta = os.listdir(ruta_subcarpeta)

    for archivo in subcarpeta:
        if archivo.endswith('.txt'):
            with open(os.path.join(ruta_subcarpeta, archivo), 'r') as archivotxt:
                lineas = archivotxt.readlines()
                # Obtener yaw, pitch y roll de la primera línea del archivo
                yaw, pitch, roll = map(float, lineas[0].strip().split())
                lista_yaw.append(yaw)
                lista_pitch.append(pitch)
                lista_roll.append(roll)
                coordenadas = lineas[2].strip().split()
                datos_frame = []  # Lista para almacenar las coordenadas de un frame
                for i in range(0, len(coordenadas), 2):
                    x = float(coordenadas[i])
                    y = float(coordenadas[i+1])
                    datos_frame.append((x, y))  # Almacena las coordenadas como tuplas (x, y)
                lista_frames.append(datos_frame)  # Agrega las coordenadas del frame a la lista
    return lista_frames, lista_yaw, lista_pitch, lista_roll


def min_max_scale_coordinates(data):
        scaled_data = []
        
        for sublist in data:
            # Separar las coordenadas x e y en listas separadas
            x_coords = [coord[0] for coord in sublist]
            y_coords = [coord[1] for coord in sublist]

            # Crear un MinMaxScaler para las coordenadas x
            scaler_x = MinMaxScaler()
            scaler_x.fit(np.array(x_coords).reshape(-1, 1))  # Ajustar el scaler a las coordenadas x
            x_scaled = scaler_x.transform(np.array(x_coords).reshape(-1, 1))  # Escalar las coordenadas x

            # Crear un MinMaxScaler para las coordenadas y
            scaler_y = MinMaxScaler()
            scaler_y.fit(np.array(y_coords).reshape(-1, 1))  # Ajustar el scaler a las coordenadas y
            y_scaled = scaler_y.transform(np.array(y_coords).reshape(-1, 1))  # Escalar las coordenadas y

            # Combinar las coordenadas x e y escaladas en pares nuevamente
            scaled_sublist = [(x_scaled[i][0], y_scaled[i][0]) for i in range(len(sublist))]
            scaled_data.append(scaled_sublist)

        return scaled_data

def formar_matriz_frames_landmarks(person1, person2):
        num_frames = len(person1)
        num_landmarks = len(person1[0])  # Suponiendo que todos los frames tienen la misma cantidad de landmarks
        matriz = np.zeros((num_frames, 2, num_landmarks, 2))  # Matriz inicializada con ceros
        
        for i in range(num_frames):
            for j in range(num_landmarks):
                matriz[i, 0, j] = person1[i][j]  # Puntos xy de la persona 1 en el frame i y landmark j
                matriz[i, 1, j] = person2[i][j]  # Puntos xy de la persona 2 en el frame i y landmark j

        return matriz





    
def detect_mimicry_with_shift(data_persona1, data_persona2,shift=50):
    ventana = 200  # Tamaño de la ventana para revisar el mimetismo
    resultados_mimetismo = []  # Lista para almacenar los resultados de mimetismo
    frames_p1=data_persona1["frames"]
    frames_p2=data_persona2["frames"]
    roll_p1=data_persona1["roll"]
    roll_p2=data_persona2["roll"]
    yaw_p1=data_persona1["yaw"]
    pitch_p1=data_persona1["pitch"]
    yaw_p2=data_persona2["yaw"]
    pitch_p2=data_persona2["pitch"]


    inicio = 0
    while inicio <= len(frames_p1) - ventana:
        fin = inicio + ventana
        if fin > len(frames_p1):
            break
        
        # Calcular el mimetismo dentro de la ventana de tiempo
        mimetismo = evaluar_mimetismo(frames_p1[inicio:fin], frames_p2[inicio:fin], yaw_p1[inicio:fin], yaw_p2[inicio:fin], pitch_p1[inicio:fin], pitch_p2[inicio:fin], roll_p1[inicio:fin], roll_p2[inicio:fin])
        
        if mimetismo:
            resultados_mimetismo.append([inicio, fin])
            # Avanzar el análisis 4 segundos (200 frames) si se detecta mimetismo
            inicio = fin + 200
        else:
            encontrado_mimetismo = False
            for desfase in range(1, 5):  # Rango de 1 a 4 segundos de desfase
                desfase_frames = desfase * 50  # Convertir segundos a frames
                ventana_inicio_persona2 = inicio + desfase_frames
                ventana_fin_persona2 = fin + desfase_frames

                if ventana_fin_persona2 <= len(frames_p2):
                    mimetismo = evaluar_mimetismo(frames_p1[inicio:fin], frames_p2[ventana_inicio_persona2:ventana_fin_persona2], yaw_p1[inicio:fin], yaw_p2[ventana_inicio_persona2:ventana_fin_persona2], pitch_p1[inicio:fin], pitch_p2[ventana_inicio_persona2:ventana_fin_persona2], roll_p1[inicio:fin], roll_p2[ventana_inicio_persona2:ventana_fin_persona2])
                    
                    if mimetismo:
                        resultados_mimetismo.append([inicio, fin])
                        encontrado_mimetismo = True
                        inicio = fin + 200  # Avanzar el análisis 4 segundos (200 frames) si se detecta mimetismo
                        break
            if not encontrado_mimetismo:
                inicio += shift                
        
    return resultados_mimetismo


def evaluar_mimetismo(frames_p1,frames_p2,yaw_p1,yaw_p2,pitch_p1,pitch_p2,roll_p1,roll_p2):
    
    modelo = load_model('models/antiguo_mejor_modelo_reentrenado_kfolds_070_089_079.keras')
    matriz_frames_landmarks = formar_matriz_frames_landmarks(frames_p1, frames_p2)
    num_frames, _, num_landmarks, _ = matriz_frames_landmarks.shape
    num_features = (num_landmarks * 4) + 6  # 2 personas * 2 coordenadas 
    matriz_flatten = np.zeros((num_frames, num_features))

    for i in range(num_frames):
        for j in range(num_landmarks):
            point1 = matriz_frames_landmarks[i, 0, j]
            point2 = matriz_frames_landmarks[i, 1, j]
            matriz_flatten[i, j * 4] = point1[0]  # x1
            matriz_flatten[i, j * 4 + 1] = point1[1]  # y1
            matriz_flatten[i, j * 4 + 2] = point2[0]  # x2
            matriz_flatten[i, j * 4 + 3] = point2[1]  # y2

        matriz_flatten[i, num_landmarks * 4] = yaw_p1[i]
        matriz_flatten[i, num_landmarks * 4 + 1] = yaw_p2[i]
        matriz_flatten[i, num_landmarks * 4 + 2] = roll_p1[i]
        matriz_flatten[i, num_landmarks * 4 + 3] = roll_p2[i]
        matriz_flatten[i, num_landmarks * 4 + 4] = pitch_p1[i]
        matriz_flatten[i, num_landmarks * 4 + 5] = pitch_p2[i]

    # Reshape para que coincida con la entrada esperada del modelo
    num_timesteps = 4  # Esto debe coincidir con la configuración del modelo
    n_length = num_frames // num_timesteps
    matriz_flatten_reshaped = matriz_flatten.reshape((1, num_timesteps, n_length, num_features))

    # Hacer la predicción
    prediccion = modelo.predict(matriz_flatten_reshaped)

    # Decidir si es mimetismo basado en la predicción (ajusta según tu caso)
    mimetismo = (prediccion > 0.5).astype(int)

    return np.any(mimetismo)
