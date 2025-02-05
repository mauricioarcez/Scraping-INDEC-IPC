<<<<<<< HEAD
# Scraper de Precios INDEC
Este proyecto automatiza la recolección y procesamiento de datos de precios desde el INDEC (Instituto Nacional de Estadística y Censos de Argentina).

## 📋 Requisitos
- Python 3.10 o superior
- Dependencias listadas en requirements.txt:

## 🚀 Instalación

1. Clonar el repositorio.
2. Crear y activar entorno virtual.
3. Instalar dependencias:
```bash
pip install -r requirements.txt
playwright install
```

## 💻 Uso

### Ejecución Manual

Para ejecutar el scraping manualmente:
```bash
python -m src.main
```

## 📊 Proceso de Datos

   - Obtiene la URL del archivo Excel de forma dinamica, adelantandose a cambios en nombres de archivo.
   - Extrae datos de la hoja "Nacional"
   - Limpieza de datos, Identificación de encabezados, Procesamiento de fechas y precios.
   - Melt de archivo ancho a largo. 
   - Generación de IDs únicos por producto
   - Validacion de datos.
   - Guardado de archivo limpio en formato .csv
   - Obtencion de la proxima fecha de informe.
   - Actualiza el cronograma de ejecución
   - Se ejecuta automáticamente en la fecha del informe
   - Guarda y commitea los cambios del nuevo informe

## 📝 Notas

- Los datos se actualizan automáticamente según el calendario del INDEC
- Los archivos CSV se guardan en el repositorio
- El workflow se puede ejecutar manualmente desde GitHub Actions si es necesario

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📄 Desarrollado por Mauricio Arce. 
=======
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
>>>>>>> b7c06fe22400c80d5faa44d71b151770d61fe8c8
