import streamlit as st
import pandas as pd
import ollama

# Configuración de la página del War Room
st.set_page_config(page_title="War Room C5I - Análisis Local", layout="wide")
st.title("🛡️ War Room C5I - Dashboard de Inteligencia Local")

# 1. Carga de Datos Estructurados
st.header("1. Base de Datos Analizada")
try:
    df = pd.read_csv("db_inteligencia.csv")
    
    # Mostrar métricas rápidas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Registros Extraídos", len(df))
    with col2:
        # Contar alertas críticas si existe la columna
        criticos = len(df[df['nivel_riesgo'] == 'CRÍTICO']) if 'nivel_riesgo' in df.columns else 0
        st.metric("Alertas Críticas Activas", criticos)

    # Mostrar la tabla interactiva
    st.dataframe(df, use_container_width=True)
        
except FileNotFoundError:
    st.warning("Aún no hay datos. Ejecuta el motor_extraccion.py primero.")
    df = pd.DataFrame() # DataFrame vacío de respaldo

# 2. Chat Analítico con Qwen 2.5 14B
st.header("2. Interrogatorio de Datos (Chat PLN)")
st.write("Consulta a Qwen sobre la información extraída. El procesamiento es 100% local y privado.")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial de mensajes
for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Caja de texto para que el analista pregunte
pregunta_usuario = st.chat_input("Ej: ¿Cuáles son los RUTs extraídos de las alertas críticas de hoy?")

if pregunta_usuario:
    # Mostrar pregunta del usuario
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario})
    
    # Preparar el contexto pasándole la base de datos a Qwen
    contexto_datos = df.to_json(orient="records") if not df.empty else "No hay datos disponibles en la base."
    prompt_chat = f"Eres un analista de inteligencia. Base de datos actual: {contexto_datos}\n\nResponde la siguiente pregunta del usuario basándote ESTRICTAMENTE en la base de datos proporcionada: {pregunta_usuario}"
    
    # Consultar a Ollama localmente
    with st.chat_message("assistant"):
        respuesta_placeholder = st.empty()
        respuesta_completa = ""
        
        try:
            response = ollama.chat(
                model='qwen2.5:14b',
                messages=[
                    {'role': 'system', 'content': 'Eres un asistente analítico militar/corporativo. Responde de forma directa, estructurada y basándote solo en los datos proporcionados.'},
                    {'role': 'user', 'content': prompt_chat}
                ],
                stream=True # Escritura en tiempo real
            )
            
            # Efecto de máquina de escribir
            for chunk in response:
                if 'message' in chunk and 'content' in chunk['message']:
                    respuesta_completa += chunk['message']['content']
                    respuesta_placeholder.markdown(respuesta_completa + "▌")
            respuesta_placeholder.markdown(respuesta_completa)
            
        except Exception as e:
            respuesta_completa = f"Error de conexión con Qwen: {e}"
            respuesta_placeholder.markdown(respuesta_completa)
            
    # Guardar respuesta en el historial
    st.session_state.mensajes.append({"role": "assistant", "content": respuesta_completa})
