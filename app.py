import streamlit as st
import os #Para rutas y archivos
import subprocess
import threading #Para hilos dentro de un proceso
import zipfile #Para archivos .zip

# Título de la página
st.title("Control de Juego con Gestos de Manos")

# Descripción del proyecto
st.write("Bienvenido a la aplicación de control de gestos para videojuegos.")
st.write("""
Esta aplicación te permite descargar y ejecutar un juego controlado por el movimiento de las manos. 
Utiliza las bibliotecas de Streamlit para proporcionar una interfaz intuitiva.
""")
st.write("Instrucciones:")
st.markdown("""
1. Asegúrate de estar frente a la cámara.
2. Utiliza movimientos de manos para controlar las teclas de dirección en el juego.
3. Presiona el botón de abajo para iniciar el juego y activar el control de gestos.
""")

# Ruta del archivo ejecutable del juego y del zip que se generará
ruta_juego = r"D:\Aplicaciones\test\Surgeon Simulator Anniversary Edition Inside Donald Trump\ss2013.exe"
ruta_zip = r"D:\Aplicaciones\Surgeon Simulato\Surgeon Simulator Anniversary Edition Inside Donald Trump.zip"

#Generar archivo .zip
def crear_zip():
    #Verificamos si exsite la carpeta antes de comprimirla
    if not os.path.exists(ruta_juego):
        st.error(f"La carpeta no existe: {ruta_juego}")
        return False #False si no se puede generar el .zip
    
    try:
        with zipfile.ZipFile(ruta_zip , "w" , zipfile.ZIP_DEFLATED) as zipf: 
            for carpeta_raiz, subcarpetas , archivos in os.walk(ruta_juego):#Recoorre la carpeta principal y las subcarpetas
                    for archivo in archivos: 
                     ruta_completa = os.path.join(carpeta_raiz , archivo)
                #Agregamos todos los archivos al .zip con una ruta relativa, para mantener la estructura
                    ruta_relativa = os.path.join(ruta_completa, ruta_juego)
                    zipf.write(ruta_completa, ruta_relativa) #Agrega el archivo .zip
            return True #True si genera el .zip correctamente
    except Exception as e:
            st.error(f"Error al crear el archivo .zip: {e}")
            return False #Si se genera un error mostramos el mensaje de arriba

# Botón para descargar el juego
if st.button("Descargar Juego"):
    if crear_zip(): #Llamamos a la funcion, para crear el archivo .zip
        try:
            with open(ruta_zip, "rb") as archivos_zip: #El archivo .zip se abre en modo binario para descargarse bien
                st.download_button(
                    label="Haz clic aquí para descargar",
                    data=archivos_zip,
                    file_name="juego.zip",
                    mime="application/zip" #Tipo mine para archivos zip
        )
        except Exception as e: #Error en el caso de que nno se pueda leer el archivo
            st.error("No se encontró el archivo de juego. Por favor, asegúrate de que el archivo sea correcto")
        

# Botón para ejecutar el juego
if st.button("Ejecutar Juego"):
    if os.path.exists(ruta_juego): #Se ve si el archivo del juego existe
        # Ejecuta el juego en segundo plano
        st.write("Ejecutando el juego...")
        subprocess.Popen(["python", ruta_juego], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #Para ejecutar el juego en segundo planno sin bloquear el script
    else:
        st.error("El archivo del juego no se encuentra. Descárgalo primero o verifica la ruta.")

# Nota final
st.write("Espero lo disfrutes.")