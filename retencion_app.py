import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Banfield Retention Tool",
    page_icon="🐾",
    layout="centered"
)

# --- ESTILOS PERSONALIZADOS (CSS para colores Banfield) ---
st.markdown("""
    <style>
    .big-font { font-size:24px !important; color: #004C85; font-weight: bold; }
    .stButton>button {
        background-color: #E87722;
        color: white;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #cf6618;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
# Usamos columnas para centrar o poner logo si quisieras
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown('<p class="big-font">Banfield Pet Hospital 🏥</p>', unsafe_allow_html=True)
    st.caption("Herramienta de Retención de Clientes")

st.markdown("---")

# --- FORMULARIO DE DATOS ---
st.subheader("📝 Datos del Cliente")

col_a, col_b = st.columns(2)

with col_a:
    antiguedad_txt = st.selectbox("Antigüedad", ["1 año", "2 años", "3 años", "4 años", "5 años o más"], index=2)
    pacientes_txt = st.selectbox("Número de Mascotas", ["1 mascota", "2 mascotas", "3 mascotas", "4 o más"], index=1)

with col_b:
    comportamiento = st.selectbox("Comportamiento", ["Bueno", "Conflictivo"])
    servicios_txt = st.selectbox("Uso de Servicios", ["Alto (Ratio > 0.8)", "Bajo (Ratio < 0.2)"])

# Dinero (Input de texto para limpiar simbolos)
dinero_txt = st.text_input("Dinero Invertido ($)", placeholder="Ej: 25,000")

# --- LÓGICA DEL BOTÓN ---
if st.button("CALCULAR BENEFICIO"):
    # 1. Limpieza de datos
    dinero_clean = dinero_txt.replace('$', '').replace(',', '').strip()
    
    if not dinero_clean:
        st.error("⚠️ Por favor ingresa el dinero invertido.")
    elif not dinero_clean.replace('.', '', 1).isdigit():
        st.error("⚠️ El campo de dinero debe contener solo números.")
    else:
        # 2. Conversión de datos
        dinero = float(dinero_clean)
        antiguedad = 5 if "5" in antiguedad_txt else int(antiguedad_txt.split()[0])
        pacientes = 4 if "4" in pacientes_txt else int(pacientes_txt.split()[0])
        servicios = 0.8 if "Alto" in servicios_txt else 0.2
        
        # 3. Cálculo de Puntos
        puntos = 0
        
        # Antigüedad
        if antiguedad >= 5: puntos += 5
        elif antiguedad == 4: puntos += 4
        elif antiguedad == 3: puntos += 3
        elif antiguedad == 2: puntos += 2
        else: puntos += 1
        
        # Pacientes
        if pacientes >= 4: puntos += 5
        elif pacientes == 3: puntos += 4
        elif pacientes == 2: puntos += 3
        else: puntos += 2 if pacientes == 1 else 1

        # Dinero
        if dinero >= 40000: puntos += 5
        elif dinero >= 30000: puntos += 4
        elif dinero >= 20000: puntos += 3
        elif dinero >= 15000: puntos += 2
        else: puntos += 1
        
        # Comportamiento y Servicios
        puntos += 5 if comportamiento == "Bueno" else 0
        puntos += 5 if servicios >= 0.8 else 0
        
        # Promedio
        promedio = puntos / 5
        score_final = int(promedio + 0.5)
        
        # 4. Mostrar Resultados
        st.markdown("---")
        st.subheader("📊 Resultados")
        
        col_res1, col_res2 = st.columns([1, 2])
        
        with col_res1:
            st.metric(label="Score Final", value=f"{promedio} pts")
        
        with col_res2:
            if score_final >= 5:
                st.success("🏆 **CLIENTE VIP (Nivel 5)**")
                st.write("• 2 Mensualidades (1/año)")
                st.write("• Nexgard de regalo")
            elif score_final == 4:
                st.info("💎 **ALTO VALOR (Nivel 4)**")
                st.write("• 1 Mensualidad (1/año)")
                st.write("• Nexgard de regalo")
            elif score_final == 3:
                st.warning("🐾 **ESTÁNDAR (Nivel 3)**")
                st.write("• Nexgard de regalo")
            elif score_final == 2:
                st.error("⚠️ **NIVEL BAJO (Nivel 2)**")
                st.write("• Sin beneficios adicionales")
            else:
                st.error("❌ **RIESGO (Nivel 1)**")
                st.write("• Evitar inversión en retención")

# Pie de página
st.markdown("---")
st.caption("Banfield Pet Hospital Internal Tool")