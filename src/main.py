from src.scraper import IndecScraper
from src.transformaciones import TransformadorDatos
import logging
import pandas as pd
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Crear directorios si no existen
def crear_directorios():
    """Crea los directorios necesarios para almacenar los datos"""
    os.makedirs('data/', exist_ok=True)

def run():
    """Función principal para ejecutar el scraper y las transformaciones"""
    try:
        # Crear directorios
        crear_directorios()
        
        # Ejecutar el scraper
        scraper = IndecScraper()
        url_excel = scraper.obtener_url_excel()
        
        if url_excel:
            df_nacional = scraper.obtener_datos_nacional(url_excel)
            
            if df_nacional is not None: 
                # Guardar datos crudos
                scraper.guardar_csv(df_nacional, "data/nacional_crudo.csv")
                
                # Aplicar transformaciones
                transformador = TransformadorDatos(df_nacional)
                df_transformado = transformador.identificar_encabezados()
                
                # Guardar resultados procesados
                df_transformado.to_csv("data/nacional_procesado.csv", index=False, encoding='utf-8')
                logging.info("Datos procesados guardados exitosamente en carpeta data.'")
                
                return df_transformado
            else:
                logging.error("No se pudieron obtener los datos de la hoja Nacional")
                return None
        else:
            logging.error("No se pudo obtener la URL del archivo Excel")
            return None
            
    except Exception as e:
        logging.error(f"Error en la ejecución: {str(e)}")
        return None

if __name__ == "__main__":
    df = run()
    if df is not None:
        print("\nPrimeras filas del DataFrame procesado:")
        print(df.head())
        print("\nInformación del DataFrame:")
        print(df.info())
