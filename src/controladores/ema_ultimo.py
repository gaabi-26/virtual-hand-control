import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import win32api
import win32con
import math
import time
from pynput.keyboard import Controller, Key

# Inicializamos el controlador de teclado
keyboard = Controller()

# Inicializamos MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # Para detectar solo una mano
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Configuramos la cámara
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

# Obtenemos dimensiones de la cámara
cam_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

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

# Centro
center_point = 20

def move_mouse(x, y):
    if abs(x) > center_point or abs(y) > center_point:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)

def click_izquierdo(presionar):
    if presionar:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def click_derecho(presionar):
    if presionar:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


while True:
    success, img = cap.read()
    if not success:
        continue
    
    # Convertimos a RGB para que trabaje con MediaPipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        # Procesamos la mano detectada
        mano = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, mano, mp_hands.HAND_CONNECTIONS)


        # --------------- Control del mouse con la palma de la mano ---------------

        # Obtenemos posición de la palma (punto de referencia 0)
        palm = mano.landmark[0]
        x = int(palm.x * cam_width)
        y = int(palm.y * cam_height)
            
        # Calculamos desplazamiento desde el centro
        dx = x - int(cam_width/2)
        dy = y - int(cam_height/2)
            
        # Movemos el mouse y dibujamos puntos de referencia
        move_mouse(dx, dy)
            
        # Dibujar punto verde (palma) y zona muerta
        cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (int(cam_width/2) - center_point, int(cam_height/2) - center_point),
                    (int(cam_width/2) + center_point, int(cam_height/2) + center_point), (255, 255, 0), 2)


        # --------------- Detectamos gestos para clicks ---------------
        distancia_camara = mano.landmark[8].z
        
        # Click derecho - cuando la mano se aleja a la cámara
        # Usamos la distancia del indice a la cámara como referencia       
        if distancia_camara > -0.06 and not click_derecho_presionado:   # El valor de 0.05 se ajusta a preferencia de distancia
            click_derecho(True)
            click_derecho_presionado = True
        elif distancia_camara <= -0.06 and click_derecho_presionado:
            click_derecho(False)
            click_derecho_presionado = False

        # Click izquierdo - cuando la mano se acerca a la cámara
        # Usamos la distancia del indice a la cámara como referencia
        if distancia_camara < -0.1 and not click_presionado:
            click_izquierdo(True)
            click_presionado = True
        elif distancia_camara >= -0.1 and click_presionado:
            click_izquierdo(False)
            click_presionado = False


        # Control de teclas
        coordenadas = {}
        for id, punto in enumerate(mano.landmark):
            alto, ancho, _ = img.shape
            cord_x, cord_y = int(punto.x * ancho), int(punto.y * alto)
            coordenadas[id] = {"x": cord_x, "y": cord_y}

        # Calcular distancias
        distance_lm4_lm17 = math.hypot(
            coordenadas[17]["x"] - coordenadas[4]["x"],
            coordenadas[17]["y"] - coordenadas[4]["y"]
        )
        distance_lm5_lm8 = math.hypot(
            coordenadas[8]["x"] - coordenadas[5]["x"],
            coordenadas[8]["y"] - coordenadas[5]["y"]
        )
        distance_lm9_lm12 = math.hypot(
            coordenadas[12]["x"] - coordenadas[9]["x"],
            coordenadas[12]["y"] - coordenadas[9]["y"]
        )
        distance_lm13_lm16 = math.hypot(
            coordenadas[16]["x"] - coordenadas[13]["x"],
            coordenadas[16]["y"] - coordenadas[13]["y"]
        )
        distance_lm17_lm20 = math.hypot(
            coordenadas[20]["x"] - coordenadas[17]["x"],
            coordenadas[20]["y"] - coordenadas[17]["y"]
        )


        # --------------- Control de teclas ---------------
        # Pulgar - Espacio
        if distance_lm4_lm17 < 80 and pulgar:
            pulgar = False
            keyboard.press(Key.space)
            tecla_space_presionada = True
        elif distance_lm4_lm17 > 90 and not pulgar:
            pulgar = True
            if tecla_space_presionada:
                keyboard.release(Key.space)
                tecla_space_presionada = False

        # Índice - R
        if distance_lm5_lm8 < 30 and indice:
            indice = False
            keyboard.press('r')
            tecla_r_presionada = True
        elif distance_lm5_lm8 > 50 and not indice:
            indice = True
            if tecla_r_presionada:
                keyboard.release('r')
                tecla_r_presionada = False

        # Mayor - E
        if distance_lm9_lm12 < 30 and medio:
            medio = False
            keyboard.press('e')
            tecla_e_presionada = True
        elif distance_lm9_lm12 > 50 and not medio:
            medio = True
            if tecla_e_presionada:
                keyboard.release('e')
                tecla_e_presionada = False

        # Anular - W
        if distance_lm13_lm16 < 30 and anular:
            anular = False
            keyboard.press('w')
            tecla_w_presionada = True
        elif distance_lm13_lm16 > 50 and not anular:
            anular = True
            if tecla_w_presionada:
                keyboard.release('w')
                tecla_w_presionada = False

        # Meñique - A
        if distance_lm17_lm20 < 30 and meñique:
            meñique = False
            keyboard.press('a')
            tecla_a_presionada = True
        elif distance_lm17_lm20 > 50 and not meñique:
            meñique = True
            if tecla_a_presionada:
                keyboard.release('a')
                tecla_a_presionada = False
    else:
        # Si no se detectan manos, liberar todas las teclas y clicks
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

# Mostramos imagen
    cv2.imshow("Hand Tracking", img)

# Salir si se presiona la tecla ESC
    if cv2.waitKey(1) & 0xFF == 27:
        #liberamos las teclas
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