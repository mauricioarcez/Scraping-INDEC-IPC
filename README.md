# Scraper Automatizado de Precios por regiones INDEC
Este proyecto resuelve la complejidad estructural de los informes oficiales de precios de alimentos del [INDEC](https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31), donde los datos se publican en excels desorganizados con formatos inconsistentes, saltos de línea, contenido que cambia constantemente el nombre de sus archivos y renderizado dinámico con js que complica su obtencion automatizada. 

Mediante un sistema de scraping avanzado con Playwright (para superar las barreras de JavaScript), combinado con un pipeline de limpieza automatizada en Python, convertimos estas fuentes inutilizables en datasets analizables con informacion actualizada todos los meses.  

**Resultado**: Información lista y actualizada para análisis en .CSV, permitiendo estudios de inflación, tendencias regionales y evolución histórica con la fuente oficial pero sin el trabajo manual. 


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

### **Ejecución Automática (Recomendada)**
El sistema se ejecuta automáticamente mediante GitHub Actions:
 - Workflow Mensual: Actualiza la fecha del próximo informe (se ejecuta el día 1 de cada mes)
 - Workflow Diario: Verifica diariamente si es la fecha programada para el scraping


### **Ejecución Manual**

Para ejecutar el scraping manualmente:
```bash
python -m src.main
```
## ⚙️ GitHub Actions Workflow
### El proyecto utiliza dos workflows automatizados:**
1. **Update Next Scraping Date**
    - Se ejecuta el primer día de cada mes
    - Obtiene la próxima fecha de informe del INDEC
    - Actualiza el archivo next_date.txt

2. **Scrape on Target Date**
    - Verifica diariamente si es la fecha programada
    - Ejecuta el scraping solo cuando coincide con next_date.txt
    - Guarda los datos actualizados en el repositorio

## 📊 Proceso de Datos

1. Obtención dinámica de URL del archivo Excel
2. Extracción de datos de la hoja "Nacional"
3. Limpieza y transformación de datos:
    - Identificación de encabezados
    - Procesamiento de fechas y precios
    - Conversión de formato ancho a largo
    - Generación de IDs únicos por producto
    - Validación de datos
4. Guardado de archivos procesados en formato CSV
5. Actualización automática del repositorio

## 📝 Notas

- La ejecución automática usa UTC (ajustar zonas horarias si es necesario)
- Los datos se actualizan en la rama principal (main)
- El workflow puede ejecutarse manualmente desde GitHub Actions
- Historial de ejecuciones disponible en la pestaña "Actions"

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📄 Desarrollado por Mauricio Arce | [Linkedin](https://www.linkedin.com/in/mauricioarcez/)
