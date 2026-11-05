import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

csv_path = os.path.join(os.path.dirname(__file__), 'Tarjetas_Limpio_Real.csv')
df = pd.read_csv(csv_path)

total_empleados = len(df)
vencidos_iniciales = (df['Estatus_Calculado'] == 'Vencido').sum()
proximos_iniciales = (df['Estatus_Calculado'].str.contains('Próximo|Proximo', regex=True, na=False)).sum()
vigentes_iniciales = (df['Estatus_Calculado'] == 'Vigente').sum()

meses = np.arange(1, 13)
meses_labels = [f"Mes {i}" for i in meses]

promedio_mensual = round(total_empleados / 12)

vencidos_reactivo = [
    58, 48, 40, 35, 32, 28, 26, 29, 31, 27, 24, 28
]

vencidos_preventivo = [
    12, 4, 1, 1, 2, 0, 1, 1, 0, 1, 0, 0
]

costo_unitario_reactivo = 950
costo_unitario_preventivo = 450

costo_acum_reactivo = np.cumsum([promedio_mensual * costo_unitario_reactivo] * 12)
costo_acum_preventivo = np.cumsum([promedio_mensual * costo_unitario_preventivo] * 12)

# Crear figura con 2 gráficas (Riesgo y Costos)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle(f'Proyección Operativa y Financiera a 12 Meses\n(Basado en {total_empleados} Colaboradores - Tarjetas_Limpio_Real.csv)', 
             fontsize=14, fontweight='bold')

# Gráfica 1: Riesgo Operativo
ax1.plot(meses, vencidos_reactivo, marker='o', color='#d9534f', linewidth=2.5, label='Sin Sistema (Reactivo)')
ax1.plot(meses, vencidos_preventivo, marker='s', color='#5cb85c', linewidth=2.5, label='Con Sistema Analítico (Preventivo)')
ax1.axhline(0, color='gray', linestyle='--', alpha=0.7)
ax1.set_title('Proyección de Riesgo Sanitario\n(Personal con Tarjeta Vencida Activo)')
ax1.set_xlabel('Meses Operativos')
ax1.set_ylabel('Cantidad de Empleados Vencidos')
ax1.set_xticks(meses)
ax1.set_xticklabels(meses_labels, rotation=45)
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.legend(loc='upper right')

# Resaltar punto de partida real
ax1.annotate(f'Punto Inicial Real:\n{vencidos_iniciales} Vencidos ({vencidos_iniciales*100//total_empleados}%)',
             xy=(1, vencidos_reactivo[0]), xytext=(2.2, 52),
             arrowprops=dict(facecolor='#d9534f', shrink=0.05, width=1, headwidth=6),
             bbox=dict(boxstyle="round,pad=0.3", fc="#fdf2f2", ec="#d9534f", lw=1))

# Gráfica 2: Costos y Ahorro Acumulado
ax2.fill_between(meses, costo_acum_reactivo, color='#d9534f', alpha=0.15)
ax2.plot(meses, costo_acum_reactivo, color='#d9534f', linewidth=2.5, label=f'Gasto Reactivo (${costo_unitario_reactivo:,}/trámite)')

ax2.fill_between(meses, costo_acum_preventivo, color='#5cb85c', alpha=0.35)
ax2.plot(meses, costo_acum_preventivo, color='#5cb85c', linewidth=2.5, label=f'Gasto Preventivo/Brigada (${costo_unitario_preventivo:,}/trámite)')

ahorro_total = costo_acum_reactivo[-1] - costo_acum_preventivo[-1]
ax2.annotate(f'Ahorro Total Proyectado:\n${ahorro_total:,.0f} MXN', 
             xy=(12, costo_acum_preventivo[-1]), xytext=(4.5, costo_acum_reactivo[-1]*0.75),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#2e7d32", lw=1.5))

ax2.set_title('Proyección de Costos y Ahorro Acumulado')
ax2.set_xlabel('Meses Operativos')
ax2.set_ylabel('Costo Acumulado ($ MXN)')
ax2.set_xticks(meses)
ax2.set_xticklabels(meses_labels, rotation=45)
ax2.yaxis.set_major_formatter('${x:,.0f}')
ax2.grid(True, linestyle='--', alpha=0.4)
ax2.legend(loc='upper left')

plt.tight_layout()
plt.show()
