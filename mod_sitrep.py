"""
Módulo: SITREP Táctico
Rol: Visualización de flujo de detecciones y distribución operativa
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils_c5i import inyectar_evidencia_b64

def render_sitrep(df_filtrado):
    st.subheader("📋 Flujo de Detecciones Fácticas y Custodia Visual")
    
    col_feed, col_stats = st.columns([2, 1])
    
    with col_feed:
        if not df_filtrado.empty:
            for _, row in df_filtrado.head(35).iterrows():
                alerta = str(row.get('nivel_alerta', 'MEDIO')).upper()
                borde = "#ff4b4b" if alerta == 'CRÍTICO' else "#f6a821" if alerta == 'ALTO' else "#eab308" if alerta == 'MEDIO' else "#38bdf8"
                enlace = row.get('enlace_noticia', '')
                fuente_txt = "🔗 Inspeccionar Fuente Original" if enlace and str(enlace).startswith("http") else " Registro Interno/Histórico"
                enlace_render = f'<a href="{enlace}" target="_blank" class="link-btn">{fuente_txt}</a>' if enlace and str(enlace).startswith("http") else f'<span style="font-size:0.8rem; color:#64748b;">{fuente_txt}</span>'
                
                actor_txt = str(row.get('actor', 'No Atribuido')).strip()
                actor_badge = actor_txt if actor_txt and actor_txt.lower() not in ['desconocido', 'no especificado', 'sin dato'] else "Sin Adjudicación"
                
                src_media, es_vid = inyectar_evidencia_b64(row.get('ruta_evidencia_local', ''), row.get('url_foto', ''))
                media_html = ""
                
                if src_media:
                    if es_vid:
                        media_html = f'<div class="media-container"><video class="media-img" controls muted preload="metadata"><source src="{src_media}" type="video/mp4">Tu navegador no soporta video HTML5.</video></div>'
                    else:
                        media_html = f'<div class="media-container"><img src="{src_media}" class="media-img" alt="Evidencia Multimedia" loading="lazy"></div>'
                
                resumen_txt = str(row.get('analisis_ia', '')).strip()
                if not resumen_txt or resumen_txt.lower() == 'nan':
                    resumen_txt = "Contenido multimedia resguardado en bóveda local sin síntesis textual."
                
                html_card = f'''<div class="card-alerta" style="border-left: 5px solid {borde};">
<div style="display: flex; justify-content: space-between; align-items: center;">
<span style="font-size: 0.8rem; color: #94a3b8;">📅 {row.get('fecha_limpia', '')} | 📍 <b>{row.get('ubicacion', 'MZS')}</b> ({row.get('provincia','Arauco')})</span>
<span class="badge-org">{actor_badge}</span>
</div>
<h4 style="margin-top: 8px; margin-bottom: 4px; color: #f8fafc;">{row.get('titular', 'Sin Titular')}</h4>
<p style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.4; margin-bottom: 8px;">{resumen_txt}</p>
{media_html}
<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
<span style="font-size: 0.75rem; color: {borde}; font-weight: bold;">{alerta} ❯ {row.get('tipologia_oficial','Otros')}</span>
{enlace_render}
</div>
</div>'''
                st.markdown(html_card, unsafe_allow_html=True)
        else:
            st.info("No se registran eventos fácticos en la base de datos para la ventana temporal y filtros activos.")
    
    with col_stats:
        st.subheader("📊 Distribución Operativa")
        if not df_filtrado.empty and 'nivel_alerta' in df_filtrado.columns:
            fig_pie = px.pie(
                df_filtrado, 
                names='nivel_alerta', 
                color='nivel_alerta',
                color_discrete_map={'CRÍTICO':'#ff4b4b', 'ALTO':'#f6a821', 'MEDIO':'#eab308', 'BAJO':'#38bdf8'},
                hole=0.4
            )
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.markdown("#### Matriz por Tipología Oficial")
            df_tipo = df_filtrado['tipologia_oficial'].value_counts().reset_index()
            fig_bar = px.bar(
                df_tipo, 
                x='count', 
                y='tipologia_oficial', 
                orientation='h', 
                color='count', 
                color_continuous_scale='Reds'
            )
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False, margin=dict(t=10, b=10, l=10, r=10), yaxis_title="")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.write("Volumen insuficiente para trazar distribuciones estadísticas.")