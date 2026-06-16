import streamlit as st
import pandas as pd
import docx2txt
import re

# 1. CONFIGURACIÓN NATIVA DE LA PÁGINA
st.set_page_config(
    page_title="Control Interno - El Puerto de Liverpool",
    page_icon="📊",
    layout="wide"
)

# Variables por defecto (Datos del Almacén 195 L Tecámac) [cite: 4, 5, 6, 390]
info_tienda = {"Ubicación": "L Tecámac", "JA": "Irma Madrid Martínez", "Director": "José Manuel Luis Sánchez"}
calculo_adcoco = 1.48
monto_vales = 10142.85
monto_retiros = 13131489.00
monto_suministros = 62716.26
monto_materialidad = 52894.29

# --- SIDEBAR: AGENTE DE INGESTA ---
with st.sidebar:
    st.title("🤖 Agente de Ingesta")
    st.write("Sube el archivo de informe en formato Word (`.docx`) para actualizar el dashboard dinámicamente.")
    uploaded_file = st.file_uploader("Cargar Informe de Revisión (.docx)", type=["docx"])
    st.divider()
    st.caption("Contraloría Operativa - El Puerto de Liverpool (2026)") [cite: 403]

# --- LÓGICA DE EXTRACCIÓN AUTOMÁTICA DEL AGENTE ---
if uploaded_file is not None:
    try:
        texto_completo = docx2txt.process(uploaded_file)
        
        tienda_match = re.search(r"Ubicación:\s*(.*)", texto_completo)
        ja_match = re.search(r"Jefe Administrativo:\s*(.*)", texto_completo)
        director_match = re.search(r"Director:\s*(.*)", texto_completo)
        adcoco_match = re.search(r"Total\s*,\s*,\s*([\d\.]+)", texto_completo) or re.search(r"Riesgo 2026:\s*([\d\.]+)", texto_completo)
        
        if tienda_match: info_tienda["Ubicación"] = tienda_match.group(1).strip()
        if ja_match: info_tienda["JA"] = ja_match.group(1).strip()
        if director_match: info_tienda["Director"] = director_match.group(1).strip()
        if adcoco_match: calculo_adcoco = float(adcoco_match.group(1).strip())
        
        st.success(f"✨ ¡Informe de {info_tienda['Ubicación']} procesado exitosamente por el agente!")
    except Exception as e:
        st.warning(f"Mostrando interfaz base estructurada. Nota: {e}")

# ==============================================================================
# INTERFAZ GRÁFICA DEL DASHBOARD (100% COMPONENTES NATIVOS DE STREAMLIT)
# ==============================================================================

# Encabezado Ejecutivo
st.title("Plataforma de Control Interno y Dashboard Ejecutivo")
st.text(f"Ubicación: {info_tienda['Ubicación']} | Director: {info_tienda['Director']} | JA: {info_tienda['JA']}") [cite: 4, 5, 6]
st.divider()

# --- PANEL DE REPORTE DE KPIs ---
st.subheader("📊 Resumen Ejecutivo de KPIs")
col1, col2, col3, col4 = st.columns(4)

with col1:
    estatus_adcoco = "Riesgo Bajo" if calculo_adcoco <= 1.49 else ("Riesgo Medio" if calculo_adcoco <= 1.80 else "Riesgo Alto") [cite: 391]
    st.metric(label="Índice ADCOCO", value=f"{calculo_adcoco:.2f}", delta=estatus_adcoco, delta_color="normal" if calculo_adcoco <= 1.49 else "inverse") [cite: 390, 391]

with col2:
    monto_total_riesgo = monto_vales + monto_retiros + monto_suministros + monto_materialidad [cite: 392]
    st.metric(label="Monto Total en Riesgo", value=f"${monto_total_riesgo:,.2f}", delta="Acciones Requeridas", delta_color="inverse") [cite: 392]

with col3:
    st.metric(label="Venta Registrada Auditada", value="108 M", delta="Flujo Total Efectivo") [cite: 244]

with col4:
    st.metric(label="Evolución Histórica", value="1.48", delta="Estable (2024: 1.45 | 2025: 1.40)") [cite: 390, 400, 401]

st.subheader("📈 Gráficos Interactivos de Operación")
col_g1, col_g2 = st.columns([2, 1])

with col_g1:
    st.write("**Curva Horaria Acumulada: Ventas vs. Retiros (Brecha observada de 13:00 a 17:00 hrs)**") [cite: 244]
    horas_e = [f"{h}:00" for h in range(11, 24)] [cite: 244]
    ventas_y = [31.5, 80.2, 99.2, 115.4, 108.1, 103.3, 101.9, 108.4, 115.9, 125.6, 112.0, 10.5, 0.3] [cite: 244]
    retiros_x = [8.4, 42.2, 68.3, 91.5, 98.7, 90.2, 88.9, 105.7, 135.1, 162.4, 174.4, 22.1, 1.0] [cite: 244]
    
    df_grafico = pd.DataFrame({"Importe Venta (Miles)": ventas_y, "Importe Retiro (Miles)": retiros_x}, index=horas_e) [cite: 244]
    st.line_chart(df_grafico)

with col_g2:
    st.write("**Distribución Cuantitativa del Riesgo Financiero ($)**") [cite: 392]
    df_riesgos_monto = pd.DataFrame({
        "Monto ($)": [monto_vales, monto_retiros, monto_suministros, monto_materialidad] [cite: 392]
    }, index=["Vales Vencidos", "Retiros Piso", "Suministros", "Materialidad"]) [cite: 392]
    st.bar_chart(df_riesgos_monto)

# --- SIMULADOR DEL ÍNDICE ADCOCO ---
st.divider()
st.subheader("🧮 Simulador del Índice ADCOCO")
st.write("Selecciona los hallazgos corregidos para observar la reducción del riesgo en vivo:") [cite: 392]

col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    s_vales = st.checkbox(f"Comprobar vales provisionales vencidos (${monto_vales:,.2f})", value=False) [cite: 21, 392]
    s_retiros = st.checkbox(f"Regularizar frecuencia de retiros cada 2 horas (${monto_retiros:,.2f})", value=False) [cite: 242, 392]
    s_suministros = st.checkbox(f"Solventar diferencias absolutas en suministros (${monto_suministros:,.2f})", value=False) [cite: 273, 392]
    s_materialidad = st.checkbox(f"Subir soporte completo de materialidad Alliax (${monto_materialidad:,.2f})", value=False) [cite: 368, 392]
    s_antilavado = st.checkbox("Completar avance del Curso Ley Antilavado (Actual: 10.1%)", value=False) [cite: 294]

with col_s2:
    bajo_base, medio_base, alto_base = 41, 6, 3 [cite: 390]
    
    if s_vales: medio_base -= 1; bajo_base += 1
    if s_suministros: medio_base -= 1; bajo_base += 1
    if s_retiros: alto_base -= 1; bajo_base += 1
    if s_materialidad: alto_base -= 1; bajo_base += 1
    if s_antilavado: alto_base -= 1; bajo_base += 1
    
    total_sim = bajo_base + medio_base + alto_base [cite: 390]
    adcoco_proyectado = ((bajo_base * 1) + (medio_base * 3) + (alto_base * 5)) / total_sim [cite: 390]
    
    delta = adcoco_proyectado - calculo_adcoco [cite: 390]
    st.metric(label="Índice ADCOCO Proyectado", value=f"{adcoco_proyectado:.2f}", delta=f"{delta:.2f} (Reducción)") [cite: 390]

# --- PLAN DE ACCIÓN ---
st.divider()
st.subheader("📋 Plan de Acción - Compromisos Obligatorios") [cite: 24, 170, 330, 376]

tareas = [
    {"Tarea": "Comprobación total de vales provisionales vencidos", "Responsable": "Irma Madrid", "Monto": f"${monto_vales:,.2f}"}, [cite: 5, 21]
    {"Tarea": "Carga de evidencias faltantes en Alliax (6 pedidos observados)", "Responsable": "Jefatura Administrativa", "Monto": f"${monto_materialidad:,.2f}"}, [cite: 368]
    {"Tarea": "Depuración de objetos olvidados por clientes y envío de acta de destrucción", "Responsable": "JA / Control Interno", "Monto": "Validación Física"}, [cite: 328, 329]
    {"Tarea": "Estrategia para avance de capacitación en Ley Antilavado (Meta >80%)", "Responsable": "Dirección y Jefatura", "Monto": "Mitigación Multas"} [cite: 294, 296]
]

for idx, t in enumerate(tareas):
    with st.container():
        c_t1, c_t2, c_t3 = st.columns([3, 1, 2])
        with c_t1:
            st.write(f"**{idx+1}. {t['Tarea']}**")
            st.caption(f"Responsable: {t['Responsable']} | Impacto: {t['Monto']}")
        with c_t2:
            st.selectbox("Estatus", ["Pendiente", "En Progreso", "Completado"], key=f"task_estatus_{idx}")
        with c_t3:
            st.text_input("Notas / Folio SAP:", key=f"task_nota_{idx}")
