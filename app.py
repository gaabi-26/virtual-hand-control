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
unsafe_allow_html=True #El true es para incluir codigo HTML 
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

