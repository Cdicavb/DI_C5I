import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

st.set_page_config(page_title="C5I | Plataforma de Inteligencia", layout="wide", page_icon="🛡️")

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

name, authentication_status, username = authenticator.login('main', 'Login C5I - Macrozona Sur')

if authentication_status:
    st.sidebar.success(f"🛡️ Conectado: {name}")
    role = config['credentials']['usernames'][username].get('role', 'analista')
    st.sidebar.info(f"Rango: {role.upper()}")
    authenticator.logout('Cerrar Sesión', 'sidebar')
    
    st.title("🏛️ CENTRAL DE MANDO C5I")
    st.markdown("### *Plataforma Unificada de Inteligencia Territorial, Forense y Estratégica*")
    st.divider()
    st.info("Seleccione un módulo en la barra lateral izquierda para iniciar operaciones.")

elif authentication_status == False:
    st.error('🚫 Usuario o contraseña incorrectos.')
elif authentication_status == None:
    st.warning('Ingrese sus credenciales de acceso.')
