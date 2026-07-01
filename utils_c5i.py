"""
Archivo: utils_c5i.py
Rol: Núcleo de utilidades compartidas para todos los módulos C5I
"""
import streamlit as st
import pandas as pd
import numpy as np
from supabase import create_client, Client
from datetime import datetime, timedelta
import io
import os
import re
import matplotlib.pyplot as plt
import base64
from wordcloud import WordCloud

# --- CONEXIÓN A SUPABASE ---
URL_SUPABASE = "https://pnxprfqwgkprpbdlnxwo.supabase.co"
API_KEY_SUPABASE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBueHByZnF3Z2twcnBiZGxueHdvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4Mjc5NzIwOCwiZXhwIjoyMDk4MzczMjA4fQ.y2B3hzaE59Ww30ayUVMAJ5fHcxHawVdbJhhgN_K-2DE"
supabase: Client = create_client(URL_SUPABASE, API_KEY_SUPABASE)

# --- MAPEO DE PROVINCIAS ---
MAPEO_PROVINCIAS = {
    'Arauco': ['Tirúa', 'Contulmo', 'Cañete', 'Los Álamos', 'Curanilahue', 'Arauco', 'Lebu'],
    'Malleco': ['Collipulli', 'Ercilla', 'Traiguén', 'Lumaco', 'Purén', 'Angol', 'Los Sauces', 'Renaico', 'Victoria', 'Curacautín', 'Lonquimay', 'Temucuicui'],
    'Cautín': ['Temuco', 'Padre Las Casas', 'Vilcún', 'Freire', 'Pitrufquén', 'Gorbea', 'Loncoche', 'Toltén', 'Teodoro Schmidt', 'Saavedra', 'Carahue', 'Nueva Imperial', 'Cholchol', 'Galvarino', 'Lautaro', 'Perquenco', 'Cunco', 'Melipeuco', 'Pucón', 'Villarrica'],
    'Biobío': ['Mulchén', 'Nacimiento', 'Negrete', 'Quilleco', 'Santa Bárbara', 'Tucapel', 'Yumbel', 'Alto Biobío', 'Los Ángeles'],
    'Los Ríos': ['Panguipulli', 'Lanco', 'Máfil', 'Valdivia', 'Mariquina', 'Río Bueno', 'La Unión'],
    'Los Lagos': ['Osorno', 'San Juan de la Costa', 'Puyehue', 'Río Negro', 'Frutillar', 'Llanquihue', 'Puerto Varas', 'Puerto Montt']
}

MAPEO_REGIONES = {
    'Región del Biobío': ['Arauco', 'Biobío'],
    'Región de La Araucanía': ['Malleco', 'Cautín'],
    'Región de Los Ríos': ['Los Ríos'],
    'Región de Los Lagos': ['Los Lagos']
}

COMUNAS_PURGADAS = ['zuyituaín kufike kimün', 'wallmapuche', 'libredeterminacionmapuche', 'no especificado', 'desconocido', 'sin dato']

# --- FUNCIONES DE UTILIDAD ---
def deducir_jerarquia(ubicacion_str):
    u_norm = str(ubicacion_str).strip().lower()
    if any(p in u_norm for p in COMUNAS_PURGADAS):
        return 'Zona Focalizada', 'Macrozona Sur'
    for prov, comunas in MAPEO_PROVINCIAS.items():
        if any(c.lower() == u_norm or c.lower() in u_norm for c in comunas):
            for reg, provs in MAPEO_REGIONES.items():
                if prov in provs:
                    return prov, reg
    return 'Zona Focalizada', 'Macrozona Sur'

def normalizar_tipologia_profunda(titular, resumen, db_tipologia=""):
    txt = f"{titular} {resumen}".lower()
    db_tipo = str(db_tipologia).strip()
    
    positivos = ['inversión', 'aportados por la empresa cmpc', 'desafío levantemos chile', 'inauguración', 'apoyo comunitario', 'donación', 'millones aportados', 'obra contempló', 'entregó viviendas', 'aportes']
    if any(p in txt for p in positivos) and any(c in txt for c in ['cmpc', 'mininco', 'empresa']):
        return 'Informativo / Positivo corporativo', 'BAJO'
    
    es_allanamiento = 'allanamient' in txt or 'allanan' in txt or 'ingreso policial' in txt or 'libredeterminacionmapuche' in txt
    es_armado = any(a in txt for a in ['balazos', 'disparos', 'armado', 'munición', 'armas', 'emboscada', 'subametralladora', 'pistola'])
    
    if es_allanamiento and es_armado:
        return 'Allanamiento / Ataque Armado', 'ALTO'
    elif es_allanamiento:
        return 'Allanamiento', 'MEDIO'
    elif any(o in txt for o in ['incauta', 'operativo policial', 'carabineros detiene', 'pdi detiene', 'procedimiento policial', 'subametralladora', 'pistola']):
        return 'Operativo Policial / Incautación', 'MEDIO'
    
    politicos = ['ministra de seguridad', 'exigen liberación', 'preso político mapuche', 'comunicado', 'declaración pública', 'seremi de seguridad', 'gobierno', 'reinaldo penchulef', 'penchulef', 'wallmapuche']
    if any(pl in txt for pl in politicos) and not any(atk in txt for atk in ['quema', 'incendio', 'atentado', 'fundo cmpc']):
        return 'Declaración / Pauta Política', 'BAJO'
    
    if db_tipo and db_tipo != "None" and db_tipo != "No especificado":
        if db_tipo == 'Ataque Incendiario':
            return 'Ataque Incendiario', 'CRÍTICO'
        elif db_tipo == 'Robo de Madera':
            return 'Robo de Madera', 'ALTO'
        elif db_tipo == 'Ataque Armado':
            return 'Ataque Armado', 'CRÍTICO'
    
    if any(x in txt for x in ['incendio', 'incendiario', 'quema', 'fuego', 'siniestro']):
        return 'Ataque Incendiario', 'CRÍTICO'
    elif any(x in txt for x in ['madera', 'tala', 'hurto forestal', 'robo forestal', 'camión cargado']):
        return 'Robo de Madera', 'ALTO'
    elif any(x in txt for x in ['usurpación', 'toma', 'ocupación', 'desalojo', 'reivindicación']):
        return 'Usurpación', 'ALTO'
    elif any(x in txt for x in ['ruta', 'corte', 'barricada', 'bloqueo', 'despeje', 'árboles caídos']):
        return 'Corte de Ruta', 'MEDIO'
    elif es_armado:
        return 'Ataque Armado', 'CRÍTICO'
    
    return 'Sabotaje / Otros', 'MEDIO'

@st.cache_data(ttl=120)
def cargar_inteligencia_masiva():
    try:
        datos_totales = []
        chunk_size = 1000
        offset = 0
        
        while True:
            res = supabase.table("inteligencia_tactica").select("*").order("fecha", desc=True).range(offset, offset + chunk_size - 1).execute()
            filas = res.data
            if not filas:
                break
            datos_totales.extend(filas)
            if len(filas) < chunk_size:
                break
            offset += chunk_size
            if len(datos_totales) >= 15000:
                break
        
        df = pd.DataFrame(datos_totales)
        if not df.empty:
            df['fecha_limpia'] = df['fecha'].astype(str).str.slice(0, 10)
            df['fecha_dt'] = pd.to_datetime(df['fecha_limpia'], errors='coerce')
            df = df.dropna(subset=['fecha_dt'])
            df['fecha_eval'] = df['fecha_dt'].dt.date
            
            df['lat_clean'] = df['latitud'].astype(str).str.replace(',', '.').str.extract(r'(-?\d+\.\d+)')[0]
            df['lon_clean'] = df['longitud'].astype(str).str.replace(',', '.').str.extract(r'(-?\d+\.\d+)')[0]
            df['latitud_num'] = pd.to_numeric(df['lat_clean'], errors='coerce')
            df['longitud_num'] = pd.to_numeric(df['lon_clean'], errors='coerce')
            
            evals = df.apply(lambda r: normalizar_tipologia_profunda(r['titular'], r.get('analisis_ia', ''), r.get('tipologia_oficial', '')), axis=1)
            df['tipologia_oficial'] = [e[0] for e in evals]
            df['alerta_semantica'] = [e[1] for e in evals]
            
            mask_ig = (df['catalizador'].str.contains('Redes Sociales|Instagram', case=False, na=False)) | \
                      (df['titular'].str.contains('vía Instagram|@', case=False, na=False)) | \
                      (df['enlace_noticia'].str.contains('instagram.com', case=False, na=False))
            df['es_rrss'] = np.where(mask_ig, True, False)
            df['canal_origen'] = np.where(df['es_rrss'], 'Meta/Instagram', 'Monitoreo de Terreno (Prensa/RSS)')
            
            jerarquias = df['ubicacion'].apply(deducir_jerarquia)
            df['provincia'] = [j[0] for j in jerarquias]
            df['region'] = [j[1] for j in jerarquias]
            df['mes_anio'] = df['fecha_dt'].dt.strftime('%Y-%m')
            
            df['nivel_alerta'] = df['alerta_semantica']
            
            criterios_cmpc = "cmpc|mininco|forestal mininco|fundo cmpc|predio cmpc|camión forestal|maquinaria forestal"
            mask_cmpc = (df['titular'].str.contains(criterios_cmpc, case=False, na=False) | df.get('analisis_ia', pd.Series()).str.contains(criterios_cmpc, case=False, na=False))
            mask_positivo = df['tipologia_oficial'] == 'Informativo / Positivo corporativo'
            df.loc[mask_cmpc & ~mask_positivo, 'nivel_alerta'] = 'CRÍTICO'
            
            ruido = "platería|artesanía|teatro|concierto|festival|básquetbol|fútbol|receta|turismo|poesía"
            df = df[~df['titular'].str.contains(ruido, case=False, na=False)]
        
        return df
    except Exception as e:
        st.error(f"Error crítico en la extracción maestra: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def cargar_predios():
    try:
        res = supabase.table("predios_cmpc").select("*").limit(5000).execute()
        df = pd.DataFrame(res.data)
        if not df.empty and 'latitud' in df.columns:
            df['latitud_num'] = pd.to_numeric(df['latitud'].astype(str).str.replace(',', '.').str.extract(r'([-+]?\d*\.\d+|\d+)')[0], errors='coerce')
            df['longitud_num'] = pd.to_numeric(df['longitud'].astype(str).str.replace(',', '.').str.extract(r'([-+]?\d*\.\d+|\d+)')[0], errors='coerce')
            return df.dropna(subset=['latitud_num', 'longitud_num'])
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def inyectar_evidencia_b64(ruta_local, url_web):
    r_local = str(ruta_local).strip() if ruta_local else ""
    u_web = str(url_web).strip() if url_web else ""
    
    if r_local and r_local.lower() not in ['nan', 'none', 'no especificado'] and os.path.exists(r_local):
        try:
            es_video = any(ext in r_local.lower() for ext in ['.mp4', '.mov'])
            with open(r_local, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode()
            
            if es_video:
                return f"data:video/mp4;base64,{b64_data}", True
            else:
                ext = "png" if r_local.lower().endswith(".png") else "jpeg"
                return f"data:image/{ext};base64,{b64_data}", False
        except Exception as e:
            pass
    
    if u_web and len(u_web) > 5 and u_web.lower() != 'nan':
        es_video = any(ext in u_web.lower() for ext in ['.mp4', '.mov', 'reel', 'video'])
        return u_web, es_video
    
    return "", False