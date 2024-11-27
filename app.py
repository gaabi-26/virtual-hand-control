# -*- coding: utf-8 -*-

import streamlit as st
import os 
import subprocess
import requests
from PIL import Image

# Título de la página, con descripcion breve
st.markdown(
    """
    <h1 style="text-align: center; color: White;">"Bienvenidos a nuestro proyecto sobre el Control de Juego con Gestos de Manos🙋‍♂️"</h1>
    <div style="text-align: center; font-size: 20px; line-height: 1.6; font-family: Calibri, sans-serif;">
        Este proyecto permite gracias a la inteligencia artificial el poder controlar videojuegos mediante gestos con las manos, 
        utilizando visión computacional que detecta y procesa el movimiento de la mano para acciones especificas como el mover un cursor, interactuar con una interfaz o ejecutar comandos en un videojuego, como el que nosotros nos basamos llamado " Surgeon Simulator" en una página web interactiva creada con 
        <strong>Streamlit</strong>. Dicho proyecto combina inteligencia artificial, procesamiento de imágenes 
        y una interfaz intuitiva para brindar una experiencia innovadora.
    </div>
    """,
    unsafe_allow_html=True
)
# Adelanto
st.write("")
st.write("")
   
### Adelanto de nuestro proyecto📷
st.image("https://github.com/gaabi-26/virtual-hand-control/blob/main/img/ejemplo_mano_juego.jpg?raw=true", caption="Esta es una imagen de como funciona el detector de manos", use_container_width=True)

st.image("https://github.com/gaabi-26/virtual-hand-control/blob/main/img/landmarks.png?raw=true", caption="Esta es una imagen del funcionamiento el detector de manos", use_container_width=True)

st.image("https://github.com/gaabi-26/virtual-hand-control/blob/main/img/ejemplos_manos.png?raw=true", caption="Esta es una imagen del funcionamiento el detector de manos", use_container_width=True)

st.image("https://github.com/gaabi-26/virtual-hand-control/blob/main/img/ejemplo_juego.jpg?raw=true", caption="Esta es una imagen del juego", use_container_width=True)

st.video("https://www.youtube.com/watch?v=ZO10bAn_8M8", start_time=0)


# Caracteristicas
st.write("")
st.write("")
st.markdown(
    """
    ### Como Jugar🕹️
    <ul>
        <li>Sustituimos las teclas originales del juego por movimientos de la mano, explicados a continuacion.</li>
        <ul>    
            <li>BARRA ESPACIADORA: PULGAR</li>
            <li>R: INDICE.</li>
            <li>E: DEDO DEL MEDIO.</li>
            <li>W: ANULAR.</li>
            <li>A: MEÑIQUE.</li>
        </ul>
    </ul>
    """,
unsafe_allow_html=True
)

# Requisitos
st.write("")
st.write("")
st.markdown(
    """
    ### Requisitos🖥️
    <ul>
        <li>**Python 3.8**.</li>
        <li>Librerias necesarias (instalables desde <code>requirements.txt</code>)</li>
            <ul>
                <li>opencv-python</li>
                <li>mediapipe</li>
                <li>pyautogui</li>
                <li>pynput</li>
                <li>streamlit</li>
            </ul>
    </ul>
    """,
unsafe_allow_html=True
)

# Función para descargar el contenido del script desde la URL
def obtener_contenido_script(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "Error al descargar el script."

# Función para ejecutar el script descargado
def ejecutar_script(contenido):
    with open("temp_script.py", "w") as file:
        file.write(contenido)
    os.system("python temp_script.py")

# Menú de selección
st.write("")
st.write("")
opcion = st.selectbox(
    "Seleccione el script que desea utilizar:",
    ("Inicio", "Control con 1 mano", "Control con 2 manos")
)

# URLs de los scripts
url_una_mano = "https://raw.githubusercontent.com/gaabi-26/virtual-hand-control/refs/heads/main/src/control_una_mano.py"
url_dos_manos = "https://raw.githubusercontent.com/gaabi-26/virtual-hand-control/refs/heads/main/src/control_dos_manos.py"

# Boton para ejecutar los juegos
if opcion == "Inicio":
    st.write("")

elif opcion == "Control con 1 mano":
    st.write("")
    st.write("Este botón permite interactuar con la aplicación usando solo los movimientos de una mano, gracias a un sistema de seguimiento de gestos. Al realizar un gesto con la mano (como cerrar el dedo índice o levantar el pulgar), se activa el botón sin necesidad de hacer clic físico. Es una forma innovadora y accesible de controlar la interfaz con el movimiento natural de las manos, mejorando la interacción y la experiencia del usuario.")
    contenido = obtener_contenido_script(url_una_mano)
    
    if "Error" in contenido:
        st.error("No se pudo cargar el script.")
    else:
        st.text_area("Contenido del script", contenido, height=300)
        if st.button("Boton para ejecutar el juego con 1 mano"):
            url1 = "https://raw.githubusercontent.com/gaabi-26/virtual-hand-control/refs/heads/main/src/control_una_mano.py"
            with st.spinner('Ejecutando el script...'):
                try:
                    response = requests.get(url1) #Descarga el script mediante el url de git
                    response.raise_for_status() #Verifica que se haya descargado bien
                    script_path = "Control con 1 mano"

                    with open(script_path, "w", encoding="utf-8") as script_file:
                        script_file.write(response.text) # Guarda el script temporalmente con codificacion UTF-8 (como á, é, o ñ) que no estan codificados

                    # Ejecutar el script y capturar la salida
                    proceso = subprocess.run(
                    ['python', script_path],
                    capture_output=True,
                    text=True
                    )
                    # Mostrar la salida o los errores en la pantalla
                    if proceso.returncode == 0:
                        st.success("¡El script se ejecutó correctamente!")
                        st.text("Salida del script:")
                        st.code(proceso.stdout)  # Muestra la salida del script
                    else:
                        st.error("Hubo un error al ejecutar el script.")
                        st.text("Error:")
                        st.code(proceso.stderr)  # Muestra el error del script
                except Exception as e:
                    st.error(f"Error inesperado: {e}")

elif opcion == "Control con 2 manos":
    st.write("")
    st.write("Este botón utiliza el seguimiento de gestos de ambas manos para interactuar con la aplicación. Al realizar movimientos específicos con las dos manos, como abrir o cerrar ciertos dedos, se activa el botón sin necesidad de hacer clic físico. Este sistema mejora la interacción, ofreciendo una experiencia más intuitiva y accesible al permitir controlar la interfaz con los gestos naturales de ambas manos.")
    contenido = obtener_contenido_script(url_dos_manos)
    
    if "Error" in contenido:
        st.error("No se pudo cargar el script.")
    else:
        st.text_area("Contenido del script", contenido, height=300)
        if st.button("Boton para ejecutar el juego con 2 manos"):
            url2 = "https://raw.githubusercontent.com/gaabi-26/virtual-hand-control/refs/heads/main/src/control_dos_manos.py"
            with st.spinner('Ejecutando el script...'):
                try:
                    response = requests.get(url2)
                    response.raise_for_status()
                    script_path = "Control con 2 mano"
                    with open(script_path, "w", encoding="utf-8") as script_file:
                        script_file.write(response.text)

                    proceso = subprocess.run(
                    ['python', script_path],
                    capture_output=True,
                    text=True
                    )
                   
                    if proceso.returncode == 0:
                        st.success("¡El script se ejecutó correctamente!")
                        st.text("Salida del script:")
                        st.code(proceso.stdout)  
                    else:
                        st.error("Hubo un error al ejecutar el script.")
                        st.text("Error:")
                        st.code(proceso.stderr)  
                except Exception as e:
                    st.error(f"Error inesperado: {e}")
