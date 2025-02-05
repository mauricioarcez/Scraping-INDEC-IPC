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
