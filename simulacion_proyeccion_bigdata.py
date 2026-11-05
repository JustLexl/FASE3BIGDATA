import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

parquet_path = os.path.join(os.path.dirname(__file__), 'Tarjetas_BigData_Simulado.parquet')
print(f"Cargando dataset Big Data desde {os.path.basename(parquet_path)}...")
df = pd.read_parquet(parquet_path)

total_registros = len(df)
vencidos_iniciales = (df['Estatus'].astype(str).str.contains('Vencido', case=False, na=False)).sum()
proximos_iniciales = (df['Estatus'].astype(str).str.contains('Próximo|Proximo|Prximo', case=False, na=False)).sum()
vigentes_iniciales = (df['Estatus'].astype(str).str.contains('Vigente', case=False, na=False)).sum()

print(f"Total registros cargados: {total_registros:,}")
print(f"Vencidos iniciales: {vencidos_iniciales:,} ({vencidos_iniciales/total_registros*100:.1f}%)")

meses = np.arange(1, 13)
meses_labels = [f"Mes {i}" for i in meses]
promedio_mensual = round(total_registros / 12)
proporciones_reactivo = np.array([0.141, 0.165, 0.182, 0.210, 0.235, 0.250, 0.238, 0.260, 0.275, 0.245, 0.230, 0.255])
vencidos_reactivo = np.round(proporciones_reactivo * total_registros).astype(int)
proporciones_preventivo = np.array([0.080, 0.035, 0.015, 0.010, 0.008, 0.005, 0.006, 0.005, 0.004, 0.005, 0.003, 0.002])
vencidos_preventivo = np.round(proporciones_preventivo * total_registros).astype(int)

costo_unitario_reactivo = 950
costo_unitario_preventivo = 450

costo_acum_reactivo = np.cumsum([promedio_mensual * costo_unitario_reactivo] * 12)
costo_acum_preventivo = np.cumsum([promedio_mensual * costo_unitario_preventivo] * 12)

# Crear figura con 2 gráficas (Riesgo y Costos)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle(f'Proyección de Escala Big Data a 12 Meses\n(Dataset: {total_registros:,} Registros en Parquet)', 
             fontsize=14, fontweight='bold')

# Gráfica 1: Riesgo Operativo
ax1.plot(meses, vencidos_reactivo, marker='o', color='#d9534f', linewidth=2.5, label='Sin Sistema (Reactivo)')
ax1.plot(meses, vencidos_preventivo, marker='s', color='#5cb85c', linewidth=2.5, label='Con Sistema Analítico (Preventivo)')
ax1.set_title('Proyección de Riesgo Sanitario\n(Personal con Tarjeta Vencida)')
ax1.set_xlabel('Meses Operativos')
ax1.set_ylabel('Cantidad de Empleados Vencidos')
ax1.set_xticks(meses)
ax1.set_xticklabels(meses_labels, rotation=45)
ax1.yaxis.set_major_formatter('{x:,.0f}')
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.legend(loc='upper right')

# Resaltar punto inicial real del dataset masivo
ax1.annotate(f'Punto Inicial Big Data:\n{vencidos_iniciales:,} Vencidos ({vencidos_iniciales*100/total_registros:.1f}%)',
             xy=(1, vencidos_reactivo[0]), xytext=(2.2, vencidos_reactivo[0] * 1.15),
             arrowprops=dict(facecolor='#d9534f', shrink=0.05, width=1, headwidth=6),
             bbox=dict(boxstyle="round,pad=0.3", fc="#fdf2f2", ec="#d9534f", lw=1))

# Gráfica 2: Costos y Ahorro Acumulado (en Millones de MXN)
costo_mdp_reactivo = costo_acum_reactivo / 1_000_000
costo_mdp_preventivo = costo_acum_preventivo / 1_000_000
ahorro_mdp = costo_mdp_reactivo[-1] - costo_mdp_preventivo[-1]

ax2.fill_between(meses, costo_mdp_reactivo, color='#d9534f', alpha=0.15)
ax2.plot(meses, costo_mdp_reactivo, color='#d9534f', linewidth=2.5, label=f'Gasto Reactivo (${costo_unitario_reactivo:,}/trámite)')

ax2.fill_between(meses, costo_mdp_preventivo, color='#5cb85c', alpha=0.35)
ax2.plot(meses, costo_mdp_preventivo, color='#5cb85c', linewidth=2.5, label=f'Gasto Preventivo (${costo_unitario_preventivo:,}/trámite)')

ax2.annotate(f'Ahorro Total Proyectado:\n${ahorro_mdp:,.1f} MDP MXN\n({ahorro_mdp*1e6:,.0f} MXN)', 
             xy=(12, costo_mdp_preventivo[-1]), xytext=(4.2, costo_mdp_reactivo[-1]*0.72),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#2e7d32", lw=1.5))

ax2.set_title('Proyección Financiera y Ahorro Acumulado (Millones MXN)')
ax2.set_xlabel('Meses Operativos')
ax2.set_ylabel('Costo Acumulado (MDP MXN)')
ax2.set_xticks(meses)
ax2.set_xticklabels(meses_labels, rotation=45)
ax2.yaxis.set_major_formatter('${x:,.0f}M')
ax2.grid(True, linestyle='--', alpha=0.4)
ax2.legend(loc='upper left')

plt.tight_layout()
plt.show()

