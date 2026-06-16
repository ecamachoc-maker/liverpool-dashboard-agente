import streamlit as st
import pandas as pd
import docx2txt
import re

# 1. CONFIGURACIÓN PREMIUM DE LA PÁGINA
st.set_page_config(
    page_title="Control Interno - El Puerto de Liverpool",
    page_icon="📊",
    layout="wide"
)

# Estilos CSS Corporativos inyectados de forma segura (Línea por línea para evitar errores de Python 3.14)
st.markdown("<link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwindcss.min.css' rel='stylesheet'>", unsafe_allowed_html=True)
st.markdown("<style>.title-liverpool { color: #E01E5A; font-family: 'Arial', sans-serif; }</style>", unsafe_allowed_html=True)
st.markdown("<style>.bg-liverpool { background-color: #E01E5A; }</style>", unsafe_allowed_html=True)
st.markdown("<style>.card-dashboard { background: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-left: 4px solid #E01E5A; }</style>", unsafe_allowed_html=True)

# Variables por defecto (Datos del Almacén 195 L Tecámac)
info_tienda = {"Ubicación": "L Tecámac", "JA": "Irma Madrid Martínez", "Director": "José Manuel Luis Sánchez"}
calculo_adcoco = 1.48
monto_vales = 10142.85
monto_retiros = 13131489.00
monto_suministros = 62716.26
monto_materialidad = 52894.29

# --- SIDEBAR: AGENTE DE INGESTA ---
with st.sidebar:
    st.markdown("<h2 class='title-liverpool font-bold text-xl mb-4'>🤖 Agente de Ingesta</h2>", unsafe_allowed_html=True)
    st.write("Sube el archivo de informe en formato Word (`.docx`) para actualizar el dashboard dinámicamente.")
    uploaded_file = st.file_uploader("Cargar Informe de Revisión (.docx)", type=["docx"])
    st.markdown("---")
    st.caption("Contraloría Operativa - El Puerto de Liverpool (2026)")

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
        st.warning(f"No se pudo automatizar toda la extracción, mostrando interfaz base estructurada. Error: {e}")

# ==============================================================================
# INTERFAZ GRÁFICA DEL DASHBOARD EN PRODUCCIÓN
# ==============================================================================

# Encabezado Ejecutivo
st.markdown("<div class='flex justify-between items-center border-b-2 border-gray-200 pb-4 mb-6'><div><h1 class='title-liverpool font-bold text-3xl'>Plataforma de Control Interno y Dashboard Ejecutivo</h1><p class='text-gray-500 text-sm'>Ubicación: " + info_tienda['Ubicación'] + " | Director: " + info_tienda['Director'] + " | JA: " + info_tienda['JA'] + "</p></div><div class='text-right no-print'><button onclick='window.print()' class='bg-liverpool text-white font-bold px-4 py-2 rounded shadow hover:bg-pink-700 transition'>🖨️ Imprimir / Guardar PDF</button></div></div>", unsafe_allowed_html=True)

# --- PANEL DE REPORTE DE KPIs ---
st.markdown("### 📊 Resumen Ejecutivo de KPIs")
col1, col2, col3, col4 = st.columns(4)

with col1:
    color_adcoco = "text-green-600" if calculo_adcoco <= 1.49 else ("text-yellow-600" if calculo_adcoco <= 1.80 else "text-red-600")
    estatus_adcoco = "Riesgo Bajo" if calculo_adcoco <= 1.49 else ("Riesgo Medio" if calculo_adcoco <= 1.80 else "Riesgo Alto")
    st.markdown("<div class='card-dashboard p-5 bg-white'><p class='text-gray-400 font-semibold text-xs uppercase tracking-wider'>Índice ADCOCO</p><p class='text-3xl font-bold " + color_adcoco + "'>" + f"{calculo_adcoco:.2f}" + "</p><p class='text-xs font-medium text-gray-500 mt-1'>Estado: <b>" + estatus_adcoco + "</b></p></div>", unsafe_allowed_html=True)

with col2:
    monto_total_riesgo = monto_vales + monto_retiros + monto_suministros + monto_materialidad
    st.markdown("<div class='card-dashboard p-5 bg-white' style='border-left-color: #EF4444;'><p class='text-gray-400 font-semibold text-xs uppercase tracking-wider'>Monto Total en Riesgo</p><p class='text-3xl font-bold text-red-600'>$" + f"{monto_total_riesgo:,.2f}" + "</p><p class='text-xs font-medium text-gray-500 mt-1'>Valores y Riesgo Operativo</p></div>", unsafe_allowed_html=True)

with col3:
    st.markdown("<div class='card-dashboard p-5 bg-white' style='border-left-color: #3B82F6;'><p class='text-gray-400 font-semibold text-xs uppercase tracking-wider'>Venta Registrada Auditada</p><p class='text-3xl font-bold text-blue-600'>108 M</p><p class='text-xs font-medium text-gray-500 mt-1'>Curva Horaria de Retiros Completa</p></div>", unsafe_allowed_html=True)

with col4:
    st.markdown("<div class='card-dashboard p-5 bg-white' style='border-left-color: #10B981;'><p class='text-gray-400 font-semibold text-xs uppercase tracking-wider'>Evolución Histórica</p><p class='text-3xl font-bold text-emerald-600'>1.48</p><p class='text-xs font-medium text-gray-500 mt-1'>Estable (2024: 1.45 | 2025: 1.40)</p></div>", unsafe_allowed_html=True)

# --- GRÁFICOS INTERACTIVOS ---
st.markdown("<br>### 📈 Gráficos Interactivos de Operación", unsafe_allowed_html=True)
col_g1, col_g2 = st.columns([2, 1])

with col_g1:
    st.write("**Curva Horaria Acumulada: Ventas vs. Retiros (Evidencia de retrasos entre 13:00 y 17:00 hrs)**")
    horas_e = [f"{h}:00" for h in range(11, 24)]
    ventas_y = [31.5, 80.2, 99.2, 115.4, 108.1, 103.3, 101.9, 108.4, 115.9, 125.6, 112.0, 10.5, 0.3]
    retiros_x = [8.4, 42.2, 68.3, 91.5, 98.7, 90.2, 88.9, 105.7, 135.1, 162.4, 174.4, 22.1, 1.0]
    
    df_grafico = pd.DataFrame({"Importe Venta": ventas_y, "Importe Retiro": retiros_x}, index=horas_e)
    st.line_chart(df_grafico, color=["#E01E5A", "#64748B"])

with col_g2:
    st.write("**Distribución Cuantitativa del Riesgo Financiero ($)**")
    df_riesgos_monto = pd.DataFrame({
        "Monto ($)": [monto_vales, monto_retiros, monto_suministros, monto_materialidad]
    }, index=["Vales Vencidos", "Retiros Piso", "Suministros", "Materialidad"])
    st.bar_chart(df_riesgos_monto, color="#E01E5A")

# --- SIMULADOR DEL ÍNDICE ADCOCO ---
st.markdown("<br>### 🧮 Simulador del Índice ADCOCO (Control Interno)", unsafe_allowed_html=True)
st.write("Marca las observaciones críticas como solventadas para observar la reducción del riesgo de la tienda en tiempo real:")

col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    s_vales = st.checkbox(f"Comprobar vales provisionales vencidos (${monto_vales:,.2f}) - [Riesgo Medio]", value=False)
    s_retiros = st.checkbox(f"Regularizar frecuencia de retiros cada 2 horas (${monto_retiros:,.2f}) - [Riesgo Alto]", value=False)
    s_suministros = st.checkbox(f"Solventar diferencias absolutas en almacén suministros (${monto_suministros:,.2f}) - [Riesgo Medio]", value=False)
    s_materialidad = st.checkbox(f"Subir soporte completo de materialidad Alliax (${monto_materialidad:,.2f}) - [Riesgo Alto]", value=False)
    s_antilavado = st.checkbox("Completar avance del Curso Ley Antilavado (Actual: 10.1%) - [Riesgo Alto]", value=False)

with col_s2:
    bajo_base, medio_base, alto_base = 41, 6, 3
    
    if s_vales: medio_base -= 1; bajo_base += 1
    if s_suministros: medio_base -= 1; bajo_base += 1
    if s_retiros: alto_base -= 1; bajo_base += 1
    if s_materialidad: alto_base -= 1; bajo_base += 1
    if s_antilavado: alto_base -= 1; bajo_base += 1
    
    total_sim = bajo_base + medio_base + alto_base
    adcoco_proyectado = ((bajo_base * 1) + (medio_base * 3) + (alto_base * 5)) / total_sim
    
    delta = adcoco_proyectado - calculo_adcoco
    st.metric(label="Nuevo Índice ADCOCO Proyectado", value=f"{adcoco_proyectado:.2f}", delta=f"{delta:.2f} (Reducción de Riesgo)")
    st.info(f"Clasificación Proyectada: **{'Riesgo Bajo' if adcoco_proyectado <= 1.49 else 'Riesgo Medio'}**")

# --- PLAN DE ACCIÓN INTERACTIVO ---
st.markdown("### 📋 Plan de Acción para Jefatura Administrativa (Compromisos al 19 de Junio de 2026)", unsafe_allowed_html=True)
tareas = [
    {"Tarea": "Comprobación total de vales provisionales vencidos", "Responsable": "Irma Madrid", "Monto": f"${monto_vales:,.2f}"},
    {"Tarea": "Carga de evidencias faltantes en Alliax (6 pedidos observados)", "Responsable": "Jefatura Administrativa", "Monto": f"${monto_materialidad:,.2f}"},
    {"Tarea": "Depuración de objetos olvidados por clientes (>30 días) y envío de acta de destrucción", "Responsable": "Control Interno / JA", "Monto": "Validación Física"},
    {"Tarea": "Estrategia de choque para avance de capacitación en Ley Antilavado (Meta >80%)", "Responsable": "Dirección y Jefatura", "Monto": "Mitigación Multas"}
]

for idx, t in enumerate(tareas):
    c_t1, c_t2, c_t3 = st.columns([3, 1, 2])
    with c_t1:
        st.markdown(f"**{idx+1}. {t['Tarea']}**")
        st.caption(f"Responsable: {t['Responsable']} | Impacto Financiero: {t['Monto']}")
    with c_t2:
        st.selectbox("Estatus", ["Pendiente", "En Progreso", "Completado"], key=f"task_estatus_{idx}")
    with c_t3:
        st.text_input("Folio de Ajuste SAP / Testigo Alliax / Notas:", key=f"task_nota_{idx}")
    st.markdown("<hr style='margin:4px 0;' />", unsafe_allowed_html=True)
