"""
Módulo: Pulso RRSS e Instagram
Rol: Monitoreo OSINT y dinámica de amplificación digital
"""
import streamlit as st
import pandas as pd
import plotly.express as px

def render_rrss(df_filtrado):
    st.subheader("📱 Monitoreo OSINT: Dinámica de Amplificación Digital")
    
    if not df_filtrado.empty:
        df_rrss = df_filtrado[df_filtrado['es_rrss'] == True].copy()
        if not df_rrss.empty:
            m1, m2, m3 = st.columns(3)
            df_rrss['cuenta_digital'] = df_rrss['titular'].str.extract(r'(@[a-zA-Z0-9_.]+)', expand=False).fillna("Monitoreo General")
            cuentas_unicas = df_rrss[df_rrss['cuenta_digital'] != "Monitoreo General"]['cuenta_digital'].nunique()
            volumen_pauta = len(df_rrss)
            
            with m1: st.metric("Volumen de Pauta Digital", volumen_pauta, "Menciones")
            with m2: st.metric("Nodos Amplificadores Detectados", cuentas_unicas, "Cuentas")
            with m3: 
                top_cuenta = df_rrss['cuenta_digital'].value_counts().index[0] if not df_rrss['cuenta_digital'].empty else "N/A"
                st.metric("Top Amplificador (Peak)", top_cuenta)
            
            st.divider()
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown("#### 🏆 Ranking de Amplificadores Digitales")
                top_rank = df_rrss['cuenta_digital'].value_counts().reset_index().head(10)
                fig_rank = px.bar(top_rank, x='count', y='cuenta_digital', orientation='h', color='cuenta_digital', color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_rank.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", yaxis_title="Cuenta", xaxis_title="Volumen", showlegend=False)
                fig_rank.update_yaxes(categoryorder='total ascending')
                st.plotly_chart(fig_rank, use_container_width=True)
            
            with col_r2:
                st.markdown("#### 🎯 Grupos Físicos Amplificados")
                grupos_objetivo = ['CAM', 'WAM', 'RML', 'RMM', 'ORT', 'PPM', 'COORDINADORA ARAUCO MALLECO', 'WEICHAN AUKA MAPU', 'RESISTENCIA MAPUCHE']
                mask_grupos = df_rrss['actor'].str.upper().apply(lambda x: any(g in str(x) for g in grupos_objetivo))
                df_cruce = df_rrss[mask_grupos].groupby(['actor']).size().reset_index(name='menciones')
                
                if not df_cruce.empty:
                    fig_cruz = px.bar(df_cruce, x='actor', y='menciones', color='menciones', color_continuous_scale='Reds')
                    fig_cruz.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig_cruz, use_container_width=True)
                else:
                    st.info("No se detecta apología directa a grupos armados.")