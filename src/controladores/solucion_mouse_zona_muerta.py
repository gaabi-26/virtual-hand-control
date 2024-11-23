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

# Definir zona muerta central (en píxeles)
zona_muerta = 15  # Ajusta este valor para hacer la zona más grande o pequeña

def mover_mouse(x, y):
    # Solo mover si estamos fuera de la zona muerta
    if abs(x) > zona_muerta or abs(y) > zona_muerta:
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
            
            # Calcular desplazamiento desde el centro
            dx = x - int(ancho_cam/2)
            dy = y - int(alto_cam/2)
            
            # Mover mouse y dibujar puntos de referencia
            mover_mouse(dx, dy)
            
            # Dibujar punto verde (palma) y zona muerta
            cv2.circle(imagen, (x, y), 10, (0, 255, 0), cv2.FILLED)
            cv2.rectangle(imagen, 
                         (int(ancho_cam/2) - zona_muerta, int(alto_cam/2) - zona_muerta),
                         (int(ancho_cam/2) + zona_muerta, int(alto_cam/2) + zona_muerta),
                         (255, 0, 0), 2)

    cv2.imshow("Control del Mouse", imagen)
    
    if cv2.waitKey(1) & 0xFF == 27:  # Presiona ESC para salir
        break

camara.release()
cv2.destroyAllWindows()