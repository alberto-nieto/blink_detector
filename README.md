# Detección de Parpadeos y Duración de Ojos Cerrados

Este proyecto utiliza `dlib`, `cv2` y otras bibliotecas para detectar parpadeos y la duración de tiempo que los ojos permanecen cerrados en tiempo real a través de una webcam.

## Requisitos previos

- Python 3.6+
- Una cámara web

## Instalación

1. **Clonar el repositorio**:

```bash
git clone https://github.com/alberto-nieto/blink_detector.git
cd blink_detector
```

2. **Instalar dependencias**:

Recomendamos utilizar un entorno virtual para mantener las dependencias del proyecto aisladas. Aquí te muestro cómo hacerlo con venv:

```bash
python3 -m venv env
source env/bin/activate  # En linux
env\Scripts\activate # En Windows
pip install -r requirements.txt
```

## Uso
1. **Ejecutar el programa**:

```bash
python detect_blinks.py
```
2. Una vez que el programa esté en funcionamiento, te mostrará una ventana en tiempo real con la imagen de tu webcam. Verás información sobre la cantidad total de parpadeos, parpadeos por minuto, parpadeos por segundo y la máxima duración con los ojos cerrados.

3. Para salir del programa, simplemente presiona la tecla "q".

## Dependencias

cv2: Para la captura y procesamiento de video en tiempo real.

dlib: Para la detección de características faciales.

scipy: Utilizado para calcular distancias en el cálculo del ratio de aspecto del ojo.

imutils: Herramientas útiles para procesamiento de imagen.


