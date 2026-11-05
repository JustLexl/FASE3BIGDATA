import pandas as pd
import numpy as np
import random
from datetime import timedelta

num_registros = 1000000

departamentos_reales = ['Cocina', 'AyB', 'Steward', 'Almacén', 'Spa', 'Mantenimiento']
unidades_reales = ['Hotel Nyx', 'Nyx Spa', 'Tacos Villanos', 'Tienda Nyx']

datos_masivos = {
    'ID_Empleado': np.arange(1, num_registros + 1),
    'Departamento': np.random.choice(departamentos_reales, num_registros, p=[0.3, 0.3, 0.15, 0.1, 0.05, 0.1]),
    'Unidad_de_Negocio': np.random.choice(unidades_reales, num_registros, p=[0.8, 0.1, 0.05, 0.05]),
    'Dias_Restantes': np.random.randint(-60, 365, num_registros)
}

df_bigdata = pd.DataFrame(datos_masivos)

df_bigdata['Estatus'] = np.where(df_bigdata['Dias_Restantes'] < 0, 'Vencido',
                        np.where(df_bigdata['Dias_Restantes'] <= 30, 'Próximo a Vencer', 'Vigente'))

df_bigdata.to_parquet('Tarjetas_BigData_Simulado.parquet', index=False)
print("Dataset masivo de 1 millón de registros generado en formato Parquet.")

