import cv2
import mediapipe as mp
import win32api
import win32con

# Configuración para detectar manos
detector_manos = mp.solutions.hands
manos = detector_manos.Hands(
    static_image_mode=False,
    max_num_hands=1
)
dibujante = mp.solutions.drawing_utils

# Iniciar cámara
camara = cv2.VideoCapture(0)
ancho_cam = camara.get(cv2.CAP_PROP_FRAME_WIDTH)
alto_cam = camara.get(cv2.CAP_PROP_FRAME_HEIGHT)

def mover_mouse(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)

while True:
    # Capturar imagen
    _, imagen = camara.read()
    imagen = cv2.flip(imagen, 1)
    
    # Detectar manos
    resultados = manos.process(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
    
    if resultados.multi_hand_landmarks:
        for mano in resultados.multi_hand_landmarks:
            dibujante.draw_landmarks(imagen, mano, detector_manos.HAND_CONNECTIONS)
            
            # Obtener posición de la palma
            palma = mano.landmark[0]
            x = int(palma.x * ancho_cam)
            y = int(palma.y * alto_cam)
            
            # Mover mouse y dibujar punto verde
            mover_mouse(x - int(ancho_cam/2), y - int(alto_cam/2))
            cv2.circle(imagen, (x, y), 10, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Control del Mouse", imagen)
    
    if cv2.waitKey(1) & 0xFF == 27:  # Presiona ESC para salir
        break

camara.release()
cv2.destroyAllWindows()