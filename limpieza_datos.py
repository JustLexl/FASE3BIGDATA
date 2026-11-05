import pandas as pd
from datetime import datetime


df_real = pd.read_excel('Tarjetas_de_Salud_Activo_2026.xlsx', sheet_name='Tarjetas de Salud')

df_real['Comentario'] = df_real['Comentario'].fillna('Sin observaciones')

df_real['Fecha de Vencimiento'] = pd.to_datetime(df_real['Fecha de Vencimiento'], format='%d/%m/%Y')

fecha_actual = pd.to_datetime('today')
df_real['Dias_Restantes'] = (df_real['Fecha de Vencimiento'] - fecha_actual).dt.days


def clasificar_estatus(dias):
    if pd.isna(dias):
        return 'Sin Tarjeta'
    elif dias < 0:
        return 'Vencido'
    elif 0 <= dias <= 30:
        return 'Próximo a Vencer'
    else:
        return 'Vigente'

df_real['Estatus_Calculado'] = df_real['Dias_Restantes'].apply(clasificar_estatus)

df_real.to_csv('Tarjetas_Limpio_Real.csv', index=False)
print("Datos reales procesados y exportados correctamente.")

