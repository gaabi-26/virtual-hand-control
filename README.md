<h1 align="center">Control de Juego con Gestos de Manos</h1>

<p align="center">
  Este proyecto permite controlar videojuegos mediante gestos de las manos, utilizando visión computacional y una página web interactiva creada con <b>Streamlit</b>. Combina inteligencia artificial, procesamiento de imágenes y una interfaz intuitiva para brindar una experiencia innovadora.
</p>

---

## Características
<ul>
  <li>Controla el <b>mouse</b> y el <b>teclado</b> con gestos de la mano mediante MediaPipe y OpenCV.</li>
  <li>Descarga y ejecuta un juego directamente desde la aplicación web.</li>
  <li>Interfaz simple e intuitiva desarrollada con <b>Streamlit</b>.</li>
  <li>Compatible con cualquier cámara web estándar.</li>
</ul>

---

## Requisitos
<ul>
  <li><b>Python 3.8</b></li>
  <li>Librerías necesarias (instalables desde <code>requirements.txt</code>):</li>
  <ul>
    <li>opencv-python</li>
    <li>mediapipe</li>
    <li>pyautogui</li>
    <li>pynput</li>
    <li>streamlit</li>
  </ul>
</ul>

---

## Instalación
<ol>
  <li>Clona este repositorio:
    <pre><code>git clone https://github.com/tu-usuario/control-gestos-juego.git
cd control-gestos-juego
</code></pre>
  </li>
  <li>Instala las dependencias:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Inicia la aplicación web de Streamlit:
    <pre><code>streamlit run app.py</code></pre>
  </li>
  <li>Conecta tu cámara y sigue las instrucciones en la interfaz.</li>
</ol>

---

<h2> Instalación en un Entorno Virtual (Recomendado)</h2>

<p>Usar un entorno virtual para este proyecto te permitirá gestionar las dependencias de forma aislada y evitar conflictos con otras aplicaciones en tu sistema. Sigue estos pasos:</p>

<ol>
  <li>
    <strong>Crea el entorno virtual:</strong>
    <p>Navega hasta el directorio del proyecto y ejecuta:</p>
    <pre><code>python3.8 -m venv venv</code></pre>
    <p>Esto creará una carpeta llamada <code>venv</code> que contendrá el entorno virtual.</p>
  </li>
  <li>
    <strong>Activa el entorno virtual:</strong>
    <ul>
      <li><strong>En Windows:</strong></li>
      <pre><code>.\venv\Scripts\activate</code></pre>
      <li><strong>En macOS/Linux:</strong></li>
      <pre><code>source venv/bin/activate</code></pre>
    </ul>
  </li>
  <li>
    <strong>Instala las dependencias en el entorno virtual:</strong>
    <p>Con el entorno activado, ejecuta:</p>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>
    <strong>Inicia la aplicación web:</strong>
    <p>Asegúrate de que el entorno virtual esté activado y ejecuta:</p>
    <pre><code>streamlit run app.py</code></pre>
  </li>
  <li>
    <strong>Desactiva el entorno virtual</strong> (opcional):
    <p>Cuando termines de trabajar en el proyecto, puedes salir del entorno virtual ejecutando:</p>
    <pre><code>deactivate</code></pre>
  </li>
</ol>

<p>Este método asegura que todas las librerías se instalen exclusivamente en el entorno virtual, manteniendo tu sistema limpio y organizado.</p>
