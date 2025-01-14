# Scraping y Normalización de Datos de canasta basica IPC - INDEC (2017- actualidad) - por Regiones

Este proyecto realiza la extracción, transformación y carga de datos (ETL) del Índice de Precios al Consumidor (IPC) por regiones de la canasta básica del **INDEC**, abarcando el período desde 2017 y manejando la carga de nuevos datos para mantenerla actualizada.  

El scraping y la normalización se realizaron completamente en un cuaderno de Jupyter, destacando el uso de técnicas avanzadas para superar las limitaciones del sitio web del INDEC, como el renderizado de contenido dinámico con **JavaScript**.  
**Ahora el proceso es completamente automático**: con un solo clic, puedes actualizar la información, incluso si el INDEC agrega más tablas o modifica la estructura de los datos.  

[**Dataset en Alphacast**](https://www.alphacast.io/datasets/prueba-tecnica-completada-43861)  

---

## **Características Destacadas del Proyecto**  

1. **Automatización completa:**  
   - El proceso se encuentra automatizado en su totalidad, desde la extracción hasta el guardado en CSV o la carga en Alphacast.  
   - Con un solo clic, puedes obtener los datos actualizados del INDEC, sin importar si se agregan nuevas tablas o se modifica la estructura del sitio.  

2. **Desafío del scraping:**  
   - El HTML del INDEC es renderizado dinámicamente con JavaScript, lo que imposibilita el scraping tradicional.  
   - Se implementaron soluciones avanzadas para obtener los datos de manera confiable, sin depender de URLs directas, que suelen cambiar con frecuencia.  

3. **Transformaciones avanzadas de datos:**  
   - Los datos descargados estaban en un **formato horizontal** y desestructurado, sin tablas ni columnas organizadas.  
   - Se realizaron transformaciones profundas para estructurar los datos de manera adecuada para su análisis con **Pandas**.  
   - Fechas mal formateadas y columnas desordenadas fueron normalizadas.  

4. **Manejo de datos faltantes y errores:**  
   - Se emplearon técnicas como la interpolación y el relleno de valores nulos utilizando datos de meses anteriores y posteriores.  
   - Validación de datos para garantizar integridad y coherencia.  

5. **Formato CSV para analisis:**  
   - Los datos transformados se guardan en formato CSV. O puedes facilitar tus claves para subirlos a Alphacast y facilitar su análisis y visualización.  

---

## **Estructura del Proyecto**  

- **`.gitignore`:** Archivo para excluir archivos y directorios como el entorno virtual.  
- **`explicacion.ipynb`:** Cuaderno Jupyter que detalla el scraping, la normalización y el análisis de los datos paso a paso.  
   - **Fuente de datos:** [INDEC - IPC](https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31).  
- **`requirements.txt`:** Librerías necesarias para ejecutar el cuaderno.  

---

## **Instalación y Uso**  

Para ejecutar el proyecto en tu entorno local:  

1. **Clonar el repositorio:**  
   ```bash
   git clone https://github.com/mauricioarcez/reto-tecnico.git

2. **Crear un entorno virtual:**

   ```bash
    python -m venv venv
   
3. **Activar el entorno virtual:**
  En Windows:
   ```bash
    venv\Scripts\activate
   
4. **Instalar las dependencias:**
   ```bash
    pip install -r requirements.txt
   
Ejecutar el cuaderno Jupyter: explicacion.ipynb
