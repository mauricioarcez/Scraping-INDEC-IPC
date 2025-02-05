import pandas as pd
import logging
import warnings

# Ignorar todos los warnings
warnings.filterwarnings('ignore')

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TransformadorDatos:
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el transformador con el DataFrame a procesar.
        
        Args:
            df (pd.DataFrame): DataFrame a procesar
        """
        self.df = df

    def identificar_encabezados(self) -> pd.DataFrame:
        """
        Identifica y establece los encabezados correctos.
        
        Returns:
            pd.DataFrame: DataFrame con los encabezados correctos
        """
        try:
            encabezados = ["Región", "Productos seleccionados", "Unidad de medida"]
            fila_inicio = None

            for i, fila in self.df.iterrows():
                if all(col in str(fila.values) for col in encabezados):
                    fila_inicio = i
                    break

            if fila_inicio is not None:
                # Filtrar encabezados no nulos
                encabezados_no_nulos = [
                    str(col) for col in self.df.iloc[fila_inicio] 
                    if pd.notna(col) and str(col).strip()
                ]
                
                logging.info(f"""
                Encabezados encontrados en la fila: {fila_inicio}
                Encabezados no nulos: {encabezados_no_nulos}
                """)
                
                self.df.columns = self.df.iloc[fila_inicio]
                self.df = self.df.iloc[fila_inicio + 1:]
                return self.eliminar_filas_nulas()
            else:
                logging.error("No se encontraron los encabezados esperados")
                raise ValueError("No se encontraron los encabezados esperados")
        except Exception as e:
            logging.error(f"Error al identificar encabezados: {str(e)}")
            raise

    def eliminar_filas_nulas(self) -> pd.DataFrame:
        """
        Elimina las filas 3 y 4 del DataFrame que contienen datos nulos.
        
        Returns:
            pd.DataFrame: DataFrame sin las filas eliminadas
        """
        try:
            self.df = self.df.drop(index=[3, 4])
            logging.info("Filas nulas eliminadas exitosamente")
            return self.identificar_ultima_fila_valida()
        except Exception as e:
            logging.error(f"Error al eliminar filas nulas: {str(e)}")
            raise

    def identificar_ultima_fila_valida(self) -> pd.DataFrame:
        """
        Identifica la última fila válida basada en las regiones válidas y
        filtra el DataFrame hasta esa fila.
        
        Returns:
            pd.DataFrame: DataFrame filtrado hasta la última fila válida
        """
        try:
            regiones_validas = ['GBA', 'Pampeana', 'Noreste', 'Noroeste', 'Cuyo', 'Patagonia']
            ultima_fila_valida = self.df[self.df["Región"].isin(regiones_validas)].index[-1]
            ultima_fila_info = self.df.loc[ultima_fila_valida]
            
            self.df = self.df.loc[:ultima_fila_valida]
            
            logging.info(f"""
            Última fila válida encontrada:
            - Índice: {ultima_fila_valida}
            - Región: {ultima_fila_info['Región']}
            - Producto: {ultima_fila_info['Productos seleccionados']}
            - Unidad: {ultima_fila_info['Unidad de medida']}
            """)
            
            return self.procesar_fechas()
            
        except Exception as e:
            logging.error(f"Error al identificar última fila válida: {str(e)}")
            raise

    def procesar_fechas(self) -> pd.DataFrame:
        """
        Procesa las fechas y crea el DataFrame con columnas en formato fecha YYYY-MM-DD.
        
        Returns:
            pd.DataFrame: DataFrame con las columnas en formato fecha
        """
        try:
            # Mapeo de meses a números
            meses_a_numeros = {
                'Enero': '01', 'Febrero': '02', 'Marzo': '03', 'Abril': '04',
                'Mayo': '05', 'Junio': '06', 'Julio': '07', 'Agosto': '08',
                'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12'
            }

            # Obtener los meses de la primera fila
            meses = self.df.iloc[0, 3:].values
            
            # Identificar columnas a mantener (las que no tienen NaN en la primera fila)
            columnas_validas = [0, 1, 2]  # Mantener las tres primeras columnas
            for i, mes in enumerate(meses, start=3):
                if pd.notna(mes) and isinstance(mes, str):
                    if i < self.df.shape[1]:
                        columnas_validas.append(i)

            # Filtrar el DataFrame para mantener solo las columnas válidas
            self.df = self.df.iloc[:, columnas_validas]

            # Obtener los meses nuevamente después del filtrado
            meses = self.df.iloc[0, 3:].values

            # Detectar año y mes de inicio
            primer_mes = next((mes.strip() for mes in meses if pd.notna(mes) and isinstance(mes, str)), None)
            if primer_mes is None:
                raise ValueError("No se encontró un mes válido")

            primera_columna = next((col for col in self.df.columns[3:] if 'Año' in str(col) or str(col).isdigit()), None)
            if primera_columna is None:
                raise ValueError("No se encontró una columna con año válido")

            if 'Año' in str(primera_columna):
                año_inicio = int(str(primera_columna).replace('Año ', ''))
            else:
                año_inicio = int(primera_columna)
                
            mes_inicio = int(meses_a_numeros[primer_mes])

            logging.info(f"Fecha de inicio detectada: {año_inicio}-{mes_inicio:02d}")

            # Crear nuevas columnas con formato de fecha
            nuevas_columnas = list(self.df.columns[:3])
            for mes in meses:
                mes = mes.strip()
                if mes in meses_a_numeros:
                    mes_num = int(meses_a_numeros[mes])
                    if mes_num == 1 and mes_inicio == 12:
                        año_inicio += 1
                    mes_inicio = mes_num
                    fecha = f"{año_inicio}-{mes_num:02d}-01"
                    nuevas_columnas.append(fecha)

            # Asignar las nuevas columnas al DataFrame
            self.df.columns = nuevas_columnas
            
            return self.realizar_melt()
            
        except Exception as e:
            logging.error(f"Error al procesar fechas: {str(e)}")
            raise

    def realizar_melt(self) -> pd.DataFrame:
        """
        Realiza la transformación melt del DataFrame y elimina la fila de meses.
        
        Returns:
            pd.DataFrame: DataFrame en formato melted
        """
        try:
            # Eliminar la primera fila que contiene los meses
            self.df = self.df.iloc[1:]
            self.df = self.df.reset_index(drop=True)
            
            # Realizar melt del DataFrame
            df_melted = pd.melt(
                self.df,
                id_vars=self.df.columns[:3],  # Las primeras tres columnas como identificadores
                var_name='Date',  # Nombre para la columna de fechas
                value_name='Price'  # Nombre para la columna de valores
            )

            logging.info(f"""
            Melt completado:
            - Columnas resultantes: {list(df_melted.columns)}
            - Total filas: {len(df_melted)}
            - Muestra de datos:
            {df_melted.head(2)}
            """)

            return self.validar_dataframe(df_melted)
            
        except Exception as e:
            logging.error(f"Error al realizar melt: {str(e)}")
            raise

    def validar_dataframe(self, df_melted: pd.DataFrame) -> pd.DataFrame:
        """
        Realiza validaciones en el DataFrame final y agrega un product_id único.
        
        Args:
            df_melted (pd.DataFrame): DataFrame en formato melted a validar
            
        Returns:
            pd.DataFrame: DataFrame validado con product_id
        """
        try:
            # Listas de valores válidos
            regiones_validas = ['GBA', 'Pampeana', 'Noreste', 'Noroeste', 'Cuyo', 'Patagonia']
            productos_validos = [
                'Pan francés', 'Harina de trigo común', 'Arroz blanco simple',
                'Fideos secos tipo guisero', 'Carne picada común', 'Pollo entero',
                'Aceite de girasol', 'Leche fresca entera sachet',
                'Huevos de gallina', 'Papa', 'Azúcar', 'Detergente líquido',
                'Lavandina', 'Jabón de tocador'
            ]

            # Filtrar filas válidas
            filas_validas = df_melted["Región"].isin(regiones_validas) & df_melted["Productos seleccionados"].isin(productos_validos)
            df_melted = df_melted[filas_validas]

            # Convertir y redondear precios
            df_melted["Price"] = pd.to_numeric(df_melted["Price"], errors="coerce")
            df_melted = self.fill_missing_with_adjacent(df_melted)
            df_melted["Price"] = df_melted["Price"].round(2)

            # Convertir fechas
            df_melted["Date"] = pd.to_datetime(df_melted["Date"], errors="coerce")
            
            # Crear product_id único
            df_melted['product_id'] = df_melted.groupby(['Productos seleccionados', 'Región', 'Unidad de medida']).ngroup() + 1
            
            # Validaciones adicionales
            logging.info(f"""
            Validaciones completadas:
            - Filas totales: {len(df_melted)}
            - Rango de fechas: {df_melted['Date'].min()} a {df_melted['Date'].max()}
            - Regiones únicas: {df_melted['Región'].nunique()}
            - Productos únicos: {df_melted['Productos seleccionados'].nunique()}
            - Product IDs únicos: {df_melted['product_id'].nunique()}
            - Valores más bajos en Price: \n{df_melted.nsmallest(5, 'Price')[['Date', 'Productos seleccionados', 'Price', 'product_id']]}
            - Valores más altos en Price: \n{df_melted.nlargest(5, 'Price')[['Date', 'Productos seleccionados', 'Price', 'product_id']]}
            """)

            return df_melted

        except Exception as e:
            logging.error(f"Error en la validación del DataFrame: {str(e)}")
            raise

    def fill_missing_with_adjacent(self, df_melted: pd.DataFrame) -> pd.DataFrame:
        """
        Rellena los valores faltantes en la columna "Price" utilizando los precios
        de los meses adyacentes para el mismo producto, región y unidad.

        Args:
            df_melted (pd.DataFrame): DataFrame en formato melted a procesar

        Returns:
            pd.DataFrame: DataFrame con los valores faltantes rellenados
        """
        try:
            # Ordenar el DataFrame por fecha
            df_melted = df_melted.sort_values(by="Date")
            
            # Iterar sobre cada fila con valores faltantes
            for index, row in df_melted[df_melted["Price"].isna()].iterrows():
                region = row["Región"]
                product = row["Productos seleccionados"]
                unit = row["Unidad de medida"]
                date = row["Date"]
                
                # Filtrar datos del mismo producto y región
                product_data = df_melted[
                    (df_melted["Región"] == region) & 
                    (df_melted["Productos seleccionados"] == product) & 
                    (df_melted["Unidad de medida"] == unit)
                ]
                
                # Obtener precios adyacentes
                previous_price = product_data[product_data["Date"] < date]["Price"].dropna().tail(1)
                next_price = product_data[product_data["Date"] > date]["Price"].dropna().head(1)
                
                # Calcular y asignar el valor
                if not previous_price.empty and not next_price.empty:
                    df_melted.at[index, "Price"] = (previous_price.iloc[0] + next_price.iloc[0]) / 2
                elif not previous_price.empty:
                    df_melted.at[index, "Price"] = previous_price.iloc[0]
                elif not next_price.empty:
                    df_melted.at[index, "Price"] = next_price.iloc[0]
            
            logging.info("Valores faltantes rellenados exitosamente")
            return df_melted

        except Exception as e:
            logging.error(f"Error al rellenar valores faltantes: {str(e)}")
            raise