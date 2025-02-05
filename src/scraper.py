from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from typing import Optional
import logging
import pandas as pd
import requests
import io
import os
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class IndecScraper:
    def __init__(self):
        self.url_indec = "https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31"
        self.base_url = "https://www.indec.gob.ar"  
        self.texto_buscado = "Índice de precios al consumidor. Precios promedio de un conjunto de elementos de la canasta del IPC, según regiones"
    
    def obtener_url_excel(self) -> Optional[str]:
        """
        Obtiene la URL del archivo Excel del INDEC.
        
        Returns:
            Optional[str]: URL del archivo Excel o None si no se encuentra
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
                )
                
                context = browser.new_context(viewport={'width': 1280, 'height': 720})
                page = context.new_page()
                
                logging.info("Abriendo la página del INDEC...")
                page.goto(self.url_indec, timeout=30000)
                
                logging.info("Esperando a que el contenedor cargue...")
                selector = "div.contSH.hide[id='1']"
                try:
                    page.wait_for_selector(selector, timeout=10000)
                except PlaywrightTimeoutError:
                    logging.error(f"Tiempo de espera agotado esperando el selector: {selector}")
                    return None
                
                logging.info("Buscando el enlace del archivo Excel...")
                enlace_excel = page.locator(f"xpath=//a[contains(text(), '{self.texto_buscado}')]")
                
                try:
                    url_relativa = enlace_excel.get_attribute("href")
                    if url_relativa:
                        url_completa = f"{self.base_url}{url_relativa}"
                        logging.info(f"Enlace al archivo Excel encontrado: {url_completa}")
                        return url_completa
                    else:
                        logging.warning("No se encontró el enlace al archivo Excel.")
                        return None
                except Exception as e:
                    logging.error(f"Error al obtener el atributo href: {str(e)}")
                    return None
                finally:
                    context.close()
                    browser.close()
        except Exception as e:
            logging.error(f"Error durante la ejecución: {str(e)}")
            return None

    def obtener_datos_nacional(self, url: str) -> Optional[pd.DataFrame]:
        """
        Descarga y lee el archivo Excel, extrayendo los datos de la hoja Nacional.
        
        Args:
            url (str): URL del archivo Excel
            
        Returns:
            Optional[pd.DataFrame]: DataFrame con los datos de la hoja Nacional o None si hay error
        """
        try:
            logging.info("Descargando archivo Excel...")
            response = requests.get(url)
            
            if response.status_code == 200:
                excel_data = pd.read_excel(
                    io.BytesIO(response.content), 
                    sheet_name=None,
                    engine='xlrd'
                )
                
                hojas = list(excel_data.keys())
                logging.info(f"Hojas encontradas: {hojas}")
                
                if 'Nacional' in excel_data:
                    return excel_data['Nacional']
                else:
                    logging.warning("No se encontró la hoja Nacional en el archivo Excel")
                    return None
            else:
                logging.error(f"Error al descargar el archivo: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error al procesar el archivo Excel: {str(e)}")
            return None

    def guardar_csv(self, df: pd.DataFrame, nombre_archivo: str) -> None:
        """
        Guarda un DataFrame en un archivo CSV.
        
        Args:
            df (pd.DataFrame): DataFrame a guardar
            nombre_archivo (str): Ruta completa del archivo CSV de salida
        """
        try:
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)
            
            df.to_csv(nombre_archivo, index=False, encoding='utf-8')
            logging.info(f"Datos guardados en {nombre_archivo}")
        except Exception as e:
            logging.error(f"Error al guardar CSV: {str(e)}")

    def obtener_fecha_proximo_informe(self) -> Optional[str]:
        """
        Obtiene la fecha del próximo informe técnico del INDEC.
        
        Returns:
            Optional[str]: Fecha en formato YYYY-MM-DD o None si no se encuentra
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
                )
                
                context = browser.new_context(viewport={'width': 1280, 'height': 720})
                page = context.new_page()
                
                logging.info("Buscando fecha del próximo informe...")
                page.goto(self.url_indec, timeout=30000)
                
                # Buscar el texto que contiene la fecha del próximo informe
                proximo_informe = page.locator("text=/Próximo informe técnico: \d{1,2}\/\d{1,2}\/\d{2,4}/")
                
                try:
                    texto = proximo_informe.text_content()
                    # Extraer la fecha del texto (ejemplo: "Próximo informe técnico: 13/2/25")
                    fecha_match = re.search(r'(\d{1,2})\/(\d{1,2})\/(\d{2,4})', texto)
                    
                    if fecha_match:
                        dia, mes, anio = fecha_match.groups()
                        # Convertir año de dos dígitos a cuatro dígitos
                        if len(anio) == 2:
                            anio = '20' + anio
                        # Formatear fecha en YYYY-MM-DD
                        fecha = f"{anio}-{int(mes):02d}-{int(dia):02d}"
                        logging.info(f"Próximo informe programado para: {fecha}")
                        return fecha
                    else:
                        logging.warning("No se encontró la fecha del próximo informe")
                        return None
                    
                except Exception as e:
                    logging.error(f"Error al extraer la fecha: {str(e)}")
                    return None
                finally:
                    context.close()
                    browser.close()
                
        except Exception as e:
            logging.error(f"Error al buscar fecha del próximo informe: {str(e)}")
            return None
