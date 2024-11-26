import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import win32api
import win32con
import math
import time
from pynput.keyboard import Controller, Key

# Inicializar el controlador del teclado
keyboard = Controller()

# Inicializar MediaPipe para el reconocimiento de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  # Detecta hasta dos manos
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Configurar la cámara y obtener dimensiones de la pantalla
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

# Obtener dimensiones de la cámara
cam_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Definir zona muerta en píxeles (área donde el mouse no se mueve)
dead_zone = 15

# Variables para el estado de los dedos
pulgar = True
indice = True
medio = True
anular = True
meñique = True

# Variables para el estado de las teclas
tecla_space_presionada = False
tecla_r_presionada = False
tecla_e_presionada = False
tecla_w_presionada = False
tecla_a_presionada = False

# Variables para el estado de los clicks
click_presionado = False
click_derecho_presionado = False

def calcular_distancia(punto1, punto2):
    """Calcular distancia euclidiana entre dos puntos"""
    return math.sqrt((punto1['x'] - punto2['x'])**2 + (punto1['y'] - punto2['y'])**2)

def move_mouse(x, y):
    # Mover el mouse solo si está fuera de la zona muerta
    if abs(x) > dead_zone or abs(y) > dead_zone:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)

def click_izquierdo(presionar):
    # Función para presionar o soltar el click izquierdo
    if presionar:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def click_derecho(presionar):
    # Función para presionar o soltar el click derecho
    if presionar:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

while True:
    success, img = cap.read()
    if not success:
        continue
        
    # Voltear la imagen horizontalmente para efecto espejo
    img = cv2.flip(img, 1)
    
    # Convertir a RGB para MediaPipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        # Determinar cuál mano es la izquierda y cuál la derecha
        mano_izquierda = None
        mano_derecha = None
        
        for idx, hand in enumerate(results.multi_handedness):
            if hand.classification[0].label == "Left":
                mano_izquierda = results.multi_hand_landmarks[idx]
            else:
                mano_derecha = results.multi_hand_landmarks[idx]

        # Procesar la mano del mouse (palma de la mano izquierda)
        if mano_izquierda:
            # Obtener posición de la palma (punto de referencia 0)
            palm = mano_izquierda.landmark[0]
            x = int(palm.x * cam_width)
            y = int(palm.y * cam_height)
            
            # Calcular desplazamiento desde el centro
            dx = x - int(cam_width/2)
            dy = y - int(cam_height/2)
            
            # Mover el mouse y dibujar puntos de referencia
            move_mouse(dx, dy)
            
            # Dibujar punto verde (palma) y zona muerta
            cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, 
                         (int(cam_width/2) - dead_zone, int(cam_height/2) - dead_zone),
                         (int(cam_width/2) + dead_zone, int(cam_height/2) + dead_zone),
                         (255, 0, 0), 2)

            # Dibujar landmarks (como estaba originalmente en la mano izquierda)
            mp_draw.draw_landmarks(img, mano_izquierda, mp_hands.HAND_CONNECTIONS)
            
            # Obtener coordenadas de los puntos de la mano
            coordenadas = {}
            for id, punto in enumerate(mano_izquierda.landmark):
                alto, ancho, _ = img.shape
                cord_x, cord_y = int(punto.x * ancho), int(punto.y * alto)
                coordenadas[id] = {"x": cord_x, "y": cord_y}
            
            # Control de teclas según la posición de los dedos
            # Pulgar - Tecla Espacio
            if coordenadas[4]["x"] < coordenadas[2]["x"] and pulgar:
                pulgar = False
                keyboard.press(Key.space)
                tecla_space_presionada = True 
            elif coordenadas[4]["x"] > coordenadas[2]["x"] and not pulgar:
                pulgar = True
                if tecla_space_presionada:
                    keyboard.release(Key.space)
                    tecla_space_presionada = False

            # Índice - Tecla R
            if coordenadas[8]["y"] > coordenadas[5]["y"] and indice:
                indice = False
                keyboard.press('r')
                tecla_r_presionada = True
            elif coordenadas[8]["y"] < coordenadas[5]["y"] and not indice:
                indice = True
                if tecla_r_presionada:
                    keyboard.release('r')
                    tecla_r_presionada = False

            # Medio - Tecla E
            if coordenadas[12]["y"] > coordenadas[9]["y"] and medio:
                medio = False
                keyboard.press('e')
                tecla_e_presionada = True
            elif coordenadas[12]["y"] < coordenadas[9]["y"] and not medio:
                medio = True
                if tecla_e_presionada:
                    keyboard.release('e')
                    tecla_e_presionada = False

            # Anular - Tecla W
            if coordenadas[16]["y"] > coordenadas[13]["y"] and anular:
                anular = False
                keyboard.press('w')
                tecla_w_presionada = True
            elif coordenadas[16]["y"] < coordenadas[13]["y"] and not anular:
                anular = True
                if tecla_w_presionada:
                    keyboard.release('w')
                    tecla_w_presionada = False

            # Meñique - Tecla A
            if coordenadas[20]["y"] > coordenadas[17]["y"] and meñique:
                meñique = False
                keyboard.press('a')
                tecla_a_presionada = True
            elif coordenadas[20]["y"] < coordenadas[17]["y"] and not meñique:
                meñique = True
                if tecla_a_presionada:
                    keyboard.release('a')
                    tecla_a_presionada = False

        # Procesar la mano de clicks (mano derecha)
        if mano_derecha:
            # Obtener coordenadas de los puntos de la mano
            coordenadas = {}
            for id, punto in enumerate(mano_derecha.landmark):
                alto, ancho, _ = img.shape
                cord_x, cord_y = int(punto.x * ancho), int(punto.y * alto)
                coordenadas[id] = {"x": cord_x, "y": cord_y}
            
            # Calcular distancias para clicks
            distancia_click_izq = calcular_distancia(coordenadas[4], coordenadas[8])
            distancia_click_der = calcular_distancia(coordenadas[4], coordenadas[20])
            
            # Dibujar líneas de distancia como en el código original
            cv2.line(img, 
                     (coordenadas[4]['x'], coordenadas[4]['y']), 
                     (coordenadas[8]['x'], coordenadas[8]['y']), 
                     (0, 255, 0), 2)  # Línea verde para pulgar-índice
            
            cv2.line(img, 
                     (coordenadas[4]['x'], coordenadas[4]['y']), 
                     (coordenadas[20]['x'], coordenadas[20]['y']), 
                     (0, 0, 255), 2)  # Línea roja para pulgar-meñique
            
            # Dibujar landmarks específicos
            cv2.circle(img, (coordenadas[4]['x'], coordenadas[4]['y']), 5, (255, 0, 0), cv2.FILLED)  # Pulgar
            cv2.circle(img, (coordenadas[8]['x'], coordenadas[8]['y']), 5, (255, 0, 0), cv2.FILLED)  # Índice
            cv2.circle(img, (coordenadas[20]['x'], coordenadas[20]['y']), 5, (255, 0, 0), cv2.FILLED)  # Meñique

            # Click izquierdo - cuando la distancia entre pulgar e índice es menor a 40
            if distancia_click_izq < 40 and not click_presionado:
                click_izquierdo(True)
                click_presionado = True
            elif distancia_click_izq >= 40 and click_presionado:
                click_izquierdo(False)
                click_presionado = False

            # Click derecho - cuando la distancia entre pulgar y meñique es menor a 30
            if distancia_click_der < 30 and not click_derecho_presionado:
                click_derecho(True)
                click_derecho_presionado = True
            elif distancia_click_der >= 30 and click_derecho_presionado:
                click_derecho(False)
                click_derecho_presionado = False
    else:
        # Liberar todas las teclas y clicks si no se detectan manos
        if tecla_space_presionada:
            keyboard.release(Key.space)
            tecla_space_presionada = False
        if tecla_r_presionada:
            keyboard.release('r')
            tecla_r_presionada = False
        if tecla_e_presionada:
            keyboard.release('e')
            tecla_e_presionada = False
        if tecla_w_presionada:
            keyboard.release('w')
            tecla_w_presionada = False
        if tecla_a_presionada:
            keyboard.release('a')
            tecla_a_presionada = False
        if click_presionado:
            click_izquierdo(False)
            click_presionado = False
        if click_derecho_presionado:
            click_derecho(False)
            click_derecho_presionado = False
    
    # Mostrar imagen
    cv2.imshow("Hand Tracking", img)
    
    # Salir con la tecla 'ESC'
    if cv2.waitKey(1) & 0xFF == 27:
        # Liberar todas las teclas y clicks antes de salir
        keyboard.release(Key.space)
        keyboard.release('r')
        keyboard.release('e')
        keyboard.release('w')
        keyboard.release('a')
        if click_presionado:
            click_izquierdo(False)
        if click_derecho_presionado:
            click_derecho(False)
        break

cap.release()
cv2.destroyAllWindows()