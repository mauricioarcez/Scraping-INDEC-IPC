from src.scraper import IndecScraper
from src.transformaciones import TransformadorDatos
from src.publicar import publicar_tweet
import logging
import pandas as pd
import os
from datetime import datetime
import shutil


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run():
    """Función principal para ejecutar el scraper, las transformaciones y la publicación del tweet."""
    try:
        # Eliminar la carpeta data si existe y volver a crearla
        if os.path.exists("data"):
            shutil.rmtree("data")
        os.makedirs("data")  # Crear la carpeta nuevamente
        
        # Ejecutar el scraper
        scraper = IndecScraper()
        url_excel = scraper.obtener_url_excel()
        
        if url_excel:
            df_nacional = scraper.obtener_datos_nacional(url_excel)
            
            if df_nacional is not None: 
                # Generar un timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Nombres de archivos
                crudo_file = f"data/nacional_crudo_{timestamp}.csv"
                procesado_file = f"data/nacional_procesado_{timestamp}.csv"

                # Guardar datos crudos
                scraper.guardar_csv(df_nacional, crudo_file)
                
                # Aplicar transformaciones
                transformador = TransformadorDatos(df_nacional)
                df_transformado = transformador.identificar_encabezados()
                
                # Guardar resultados procesados
                df_transformado.to_csv(procesado_file, index=False, encoding='utf-8')
                logging.info("Datos procesados guardados exitosamente en carpeta data")
                
                # Publicar en Twitter
                publicar_tweet(df_transformado)
                
                return df_transformado, procesado_file
            else:
                logging.error("No se pudieron obtener los datos de la hoja Nacional")
                return None, None
        else:
            logging.error("No se pudo obtener la URL del archivo Excel")
            return None, None

    except Exception as e:
        logging.error(f"Error en la ejecución: {str(e)}")
        return None, None

if __name__ == "__main__":
    run()
