"""
Módulo: Visor GEOINT
Rol: Inteligencia geoespacial dinámica
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_geoint(df_filtrado, df_predios):
    st.subheader("️ Inteligencia Geoespacial Dinámica")
    st.markdown("Navegación espacial habilitada mediante zoom de ratón (scroll) activado y nodos tácticos configurados para la Macrozona Sur.")
    
    if not df_filtrado.empty:
        df_geo = df_filtrado.dropna(subset=['latitud_num', 'longitud_num']).copy()
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1: capa_vivo = st.toggle(" Capa 1: Radar en Vivo (Últimos 7 Días)", value=True)
        with col_c2: capa_hist = st.toggle(" Capa 2: Histórico (KMZ general)", value=False)
        with col_c3: capa_cmpc = st.toggle("🌲 Capa 3: Predios CMPC", value=True)
        
        fig_map = go.Figure()
        fecha_limite_vivo = datetime.now().date() - timedelta(days=7)
        
        if capa_vivo:
            df_vivo = df_geo[df_geo['fecha_eval'] >= fecha_limite_vivo]
            if not df_vivo.empty:
                df_vivo['color_alerta'] = df_vivo['nivel_alerta'].map({'CRÍTICO': '#ff4b4b', 'ALTO': '#f6a821', 'MEDIO': '#eab308', 'BAJO': '#38bdf8'}).fillna('#64748b')
                df_vivo['size_alerta'] = df_vivo['nivel_alerta'].map({'CRÍTICO': 20, 'ALTO': 14, 'MEDIO': 10, 'BAJO': 6}).fillna(8)
                fig_map.add_trace(go.Scattermapbox(
                    lat=df_vivo['latitud_num'], lon=df_vivo['longitud_num'], mode='markers',
                    marker=go.scattermapbox.Marker(size=df_vivo['size_alerta'], color=df_vivo['color_alerta'], opacity=0.9),
                    text=df_vivo['titular'], hoverinfo='text', name='Radar Vivo (7 Días)'
                ))
        
        if capa_hist:
            df_hist = df_geo[df_geo['fecha_eval'] < fecha_limite_vivo]
            if not df_hist.empty:
                fig_map.add_trace(go.Scattermapbox(
                    lat=df_hist['latitud_num'], lon=df_hist['longitud_num'], mode='markers',
                    marker=go.scattermapbox.Marker(size=8, color='#64748b', opacity=0.5),
                    text=df_hist['titular'], hoverinfo='text', name='Histórico Atentados'
                ))
        
        if capa_cmpc and not df_predios.empty:
            fig_map.add_trace(go.Scattermapbox(
                lat=df_predios['latitud_num'], lon=df_predios['longitud_num'], mode='markers',
                marker=go.scattermapbox.Marker(size=12, color='#10b981', opacity=0.8),
                text=df_predios['nombre_predio'], hoverinfo='text', name='Predios CMPC'
            ))
        
        centro_lat = df_geo['latitud_num'].mean() if len(df_geo) > 0 else -38.73
        centro_lon = df_geo['longitud_num'].mean() if len(df_geo) > 0 else -72.59
        
        fig_map.update_layout(
            mapbox_style="carto-darkmatter",
            mapbox=dict(center=dict(lat=centro_lat, lon=centro_lon), zoom=6, pitch=10),
            margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(0,0,0,0.7)", font=dict(color="white")),
            dragmode="zoom"
        )
        st.plotly_chart(fig_map, use_container_width=True, height=750, config={'scrollZoom': True, 'displayModeBar': True})