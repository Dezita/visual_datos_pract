# Práctica Visualización de Datos Parte 2
Repositorio con los códigos y dataset utilizados para resolver la práctica de Visualización de Datos del Master Ciencia de Datos de la UOC por Javier Deza Sorribas.

El juego de datos original se llama "Mental Health and Lifestyle Habits (2019-2024)" y se encuentra disponible en Kaggle:
https://www.kaggle.com/datasets/atharvasoundankar/mental-health-and-lifestyle-habits-2019-2024

La visualización final se encuentra disponible en streamlit, en este enlace:
https://visualdatospract-f3z5xe2yznrps7zbj3p8df.streamlit.app/

Estructura del repo:
- Carpeta data: contiene el juego de datos original y el preprocesado para ser usado en la visualización (limpieaza de registros con NAs)
- Carpeta scripts: contiene el código usado para procesar los datos (limpieza del dataset) en formato notebook python y el código utilizado para generar la visualización en streamlit
- Archivo .streamlitignore: evita cargar archivos innecesarios a Streamlit Cloud
- requirements.txt: incluye únicamente las bibliotecas necesarias para generar la visualización para mejorar la eficiencia de Streamlit Cloud
- LICENSE: licencia del repositorio (GNU GENERAL PUBLIC LICENSE)
