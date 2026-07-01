import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="C5I | Plataforma de Inteligencia",
    layout="wide",
    page_icon="🛡️"
)

# --- 2. CARGA DE CREDENCIALES ---
@st.cache_resource
def load_config():
    with open('config.yaml') as file:
        return yaml.load(file, Loader=SafeLoader)

config = load_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- 3. LOGIN (API v0.4.2) ---
authenticator.login()

# --- 4. VERIFICACIÓN DE AUTENTICACIÓN ---
if st.session_state.get('authentication_status'):
    # Usuario autenticado correctamente
    username = st.session_state['username']
    name = st.session_state['name']
    user_role = config['credentials']['usernames'][username].get('role', 'analista')
    
    st.sidebar.success(f"🛡️ Conectado: {name}")
    st.sidebar.info(f"Rango: {'COMANDANTE (Admin)' if user_role == 'admin' else 'ANALISTA'}")
    authenticator.logout('Cerrar Sesión', 'sidebar')
    
    st.title("🏛️ CENTRAL DE MANDO C5I")
    st.markdown("### *Plataforma Unificada de Inteligencia Territorial, Forense y Estratégica*")
    st.divider()
    st.info("Seleccione un módulo en la barra lateral izquierda para iniciar operaciones.")

elif st.session_state.get('authentication_status') == False:
    st.error('🚫 Usuario o contraseña incorrectos.')
elif st.session_state.get('authentication_status') is None:
    st.warning('Ingrese sus credenciales de acceso.')