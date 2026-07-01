"""
Módulo: Estadísticas MZS
Rol: Cuadros estadísticos y nube de conceptos
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def render_estadisticas(df_filtrado, st_session):
    st.subheader("📊 Cuadros Estadísticos y Nube de Conceptos (Bigramas/Trigramas)")
    st.markdown("Selecciona variables en los menús para filtrar el sistema. El análisis léxico está programado para utilizar estrictamente n-gramas, eliminando el ruido de palabras individuales.")
    
    if not df_filtrado.empty:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            provs_disponibles = ["Todas"] + sorted(df_filtrado['provincia'].unique().tolist())
            sel_prov = st.selectbox(
                "🎯 Aislar Provincia Crítica:", 
                provs_disponibles, 
                index=provs_disponibles.index(st_session.filtro_provincia_activo) if st_session.filtro_provincia_activo in provs_disponibles else 0
            )
            if sel_prov != st_session.filtro_provincia_activo:
                st_session.filtro_provincia_activo = sel_prov
                st.rerun()
        
        with col_f2:
            tipos_disponibles = ["Todas"] + sorted(df_filtrado['tipologia_oficial'].unique().tolist())
            sel_tipo = st.selectbox(
                "📌 Aislar Tipología Operativa:", 
                tipos_disponibles,
                index=tipos_disponibles.index(st_session.filtro_tipologia_activo) if st_session.filtro_tipologia_activo in tipos_disponibles else 0
            )
            if sel_tipo != st_session.filtro_tipologia_activo:
                st_session.filtro_tipologia_activo = sel_tipo
                st.rerun()
        
        with col_f3:
            canales_disponibles = ["Todos", "Meta/Instagram", "Monitoreo de Terreno (Prensa/RSS)"]
            sel_canal = st.selectbox(
                "📱 Aislar Canal de Ingestión:", 
                canales_disponibles,
                index=canales_disponibles.index(st_session.filtro_canal_activo) if st_session.filtro_canal_activo in canales_disponibles else 0
            )
            if sel_canal != st_session.filtro_canal_activo:
                st_session.filtro_canal_activo = sel_canal
                st.rerun()

        st.divider()
        
        st.markdown("#### Tabla de Estadísticas Generales Macrozona Sur (Frecuencia Mensual)")
        df_stat = df_filtrado.copy()
        tabla_cruzada = pd.crosstab(df_stat['region'], df_stat['mes_anio'], margins=True, margins_name="Total General")
        st.dataframe(tabla_cruzada, use_container_width=True)
        
        st.divider()
        col_ch1, col_ch2 = st.columns(2)
        with col_ch1:
            st.markdown("#### Evolución Temporal Tipificada")
            df_ev = df_filtrado.groupby(['mes_anio', 'tipologia_oficial']).size().reset_index(name='count')
            fig_ev = px.bar(df_ev, x='mes_anio', y='count', color='tipologia_oficial', barmode='stack',
                            color_discrete_map={
                                'Ataque Incendiario': '#ff4b4b',
                                'Robo de Madera': '#f6a821',
                                'Usurpación': '#10b981',
                                'Corte de Ruta': '#38bdf8',
                                'Ataque Armado': '#ec4899',
                                'Allanamiento / Ataque Armado': '#dc2626',
                                'Allanamiento': '#a855f7',
                                'Operativo Policial / Incautación': '#c084fc',
                                'Declaración / Pauta Política': '#3b82f6',
                                'Informativo / Positivo corporativo': '#059669',
                                'Sabotaje / Otros': '#64748b'
                            })
            fig_ev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", xaxis_title="Mes", yaxis_title="Sucesos")
            st.plotly_chart(fig_ev, use_container_width=True)
        
        with col_ch2:
            st.markdown("#### ☁️ Nube de Conceptos Tácticos (Solo N-gramas)")
            text_corpus = ""
            if 'palabra_clave' in df_filtrado.columns:
                n_gramas = df_filtrado['palabra_clave'].dropna().astype(str).tolist()
                conceptos_puros = [ngram.strip() for sublist in n_gramas for ngram in sublist.split(",") if len(ngram.strip().split()) > 1]
                text_corpus = " ".join([c.replace(" ", "_") for c in conceptos_puros])
            
            if text_corpus:
                wc = WordCloud(width=600, height=350, background_color="#05080f", colormap="Blues", collocations=False).generate(text_corpus)
                fig_wc, ax_wc = plt.subplots(figsize=(6, 3.5))
                fig_wc.patch.set_facecolor('#05080f')
                ax_wc.imshow(wc, interpolation='bilinear')
                ax_wc.axis('off')
                st.pyplot(fig_wc)
            else:
                st.info("No hay suficientes n-gramas detectados en las capturas filtradas.")
    else:
        st.warning("Base de datos sin registros suficientes.")