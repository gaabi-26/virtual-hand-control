import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import win32api
import win32con
import math
import time
from pynput.keyboard import Controller, Key

# Inicializar el controlador de teclado
keyboard = Controller()

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  # Detectamos dos manos
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Configurar la cámara
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

# Obtener dimensiones de la cámara
cam_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Variables para suavizado del movimiento
smoothening = 7
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

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

def move_mouse(x, y):
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
        
    # Voltear la imagen horizontalmente para efecto espejo
    img = cv2.flip(img, 1)
    
    # Convertir a RGB para MediaPipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        # Determinar qué mano es izquierda y cuál es derecha
        mano_izquierda = None
        mano_derecha = None
        
        for idx, hand in enumerate(results.multi_handedness):
            if hand.classification[0].label == "Left":
                mano_izquierda = results.multi_hand_landmarks[idx]
            else:
                mano_derecha = results.multi_hand_landmarks[idx]

        # Procesar mano del mouse (derecha)
        if mano_derecha:
            mp_draw.draw_landmarks(img, mano_derecha, mp_hands.HAND_CONNECTIONS)
            
            # Control del mouse con el dedo índice
            index_finger = mano_derecha.landmark[8]
            
            x = int(index_finger.x * cam_width)
            y = int(index_finger.y * cam_height)
            
            screen_x = np.interp(x, (0, cam_width), (0, screen_width))
            screen_y = np.interp(y, (0, cam_height), (0, screen_height))
            
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening
            
            move_mouse(curr_x - prev_x, curr_y - prev_y)
            
            prev_x, prev_y = curr_x, curr_y

            # Detectar gestos para clicks
            meñique_y = mano_derecha.landmark[20].y
            anular_y = mano_derecha.landmark[16].y
            
            meñique_arriba = meñique_y < mano_derecha.landmark[19].y
            anular_arriba = anular_y < mano_derecha.landmark[15].y

            # Click derecho - cuando el índice está abajo
            if not meñique_arriba and not click_derecho_presionado:
                click_derecho(True)
                click_derecho_presionado = True
            elif meñique_arriba and click_derecho_presionado:
                click_derecho(False)
                click_derecho_presionado = False

            # Click izquierdo - cuando el anular está abajo
            if not anular_arriba and not click_presionado:
                click_izquierdo(True)
                click_presionado = True
            elif anular_arriba and click_presionado:
                click_izquierdo(False)
                click_presionado = False

            cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)

        # Procesar mano de teclas (izquierda)
        if mano_izquierda:
            mp_draw.draw_landmarks(img, mano_izquierda, mp_hands.HAND_CONNECTIONS)
            
            coordenadas = {}
            for id, punto in enumerate(mano_izquierda.landmark):
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

            # Control de teclas
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

            # Medio - E
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
    
    # Mostrar imagen
    cv2.imshow("Hand Tracking", img)
    
    # Salir con la tecla 'q'
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