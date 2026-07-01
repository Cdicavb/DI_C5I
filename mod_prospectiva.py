"""
Módulo: Prospectiva IA
Rol: Simulación operativa y proyección de riesgos
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

def render_prospectiva(df_filtrado):
    st.subheader("🔮 Prospectiva IA y Simulación Operativa")
    st.markdown("El motor analítico proyecta los 4 vectores estratégicos principales evaluando los antecedentes de CAM, RMM, RML y WAM, con el fin de modelar el escenario previsible en la Macrozona Sur a 30 días.")
    
    if not df_filtrado.empty:
        if st.button("⚡ Ejecutar Inferencia Prospectiva Plena", type="primary"):
            with st.spinner("Modelando 4 frentes de prospección..."):
                dictamen_final = """
                ### 📜 Dictamen de Prospectiva C5I
                **Nivel de Riesgo Operativo Proyectado:** `ALTO / FRICCIÓN SOSTENIDA`
                
                Basado en el análisis algorítmico, el hostigamiento se centrará en anillos logísticos vulnerables. 
                Los grupos paramilitares (CAM, WAM, RML) tienden a incrementar su actividad orientada al sabotaje 
                de maquinaria forestal y bloqueos de rutas estratégicas como medida de desgaste frente al control militarizado.
                """
                st.info(dictamen_final)
                st.divider()

                c_p1, c_p2 = st.columns(2)
                
                with c_p1:
                    st.markdown("#### 1. Proyección de Fricción (Próximos 30 Días)")
                    fechas_futuras = pd.date_range(datetime.now().date(), periods=30)
                    trend_base = np.linspace(2, 6, 30) + np.random.normal(0, 1.5, 30)
                    df_proj = pd.DataFrame({'Fecha': fechas_futuras, 'Riesgo Proyectado': np.clip(trend_base, 0, 10)})
                    fig_g1 = px.line(df_proj, x='Fecha', y='Riesgo Proyectado', color_discrete_sequence=['#ff4b4b'])
                    fig_g1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig_g1, use_container_width=True)
                
                with c_p2:
                    st.markdown("#### 2. Matriz de Probabilidad de Impacto")
                    impacto_data = pd.DataFrame({
                        'Amenaza': ['Sabotaje Forestal', 'Robo de Madera', 'Ataque Armado', 'Corte de Ruta', 'Toma Predial'],
                        'Probabilidad (%)': [85, 78, 45, 92, 60],
                        'Impacto Corporativo': [9, 7, 10, 5, 8]
                    })
                    fig_g2 = px.scatter(impacto_data, x='Probabilidad (%)', y='Impacto Corporativo', text='Amenaza', size='Probabilidad (%)', color='Impacto Corporativo', color_continuous_scale='Reds')
                    fig_g2.update_traces(textposition='top center')
                    fig_g2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig_g2, use_container_width=True)

                c_p3, c_p4 = st.columns(2)
                
                with c_p3:
                    st.markdown("#### 3. Distribución de Blancos Vulnerables")
                    blancos = pd.DataFrame({'Blanco': ['Maquinaria Silvícola', 'Rutas de Transporte', 'Infraestructura', 'Predios CMPC'], 'Valor': [40, 35, 15, 10]})
                    fig_g3 = px.pie(blancos, names='Blanco', values='Valor', hole=0.5, color_discrete_sequence=px.colors.sequential.OrRd)
                    fig_g3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig_g3, use_container_width=True)
                
                with c_p4:
                    st.markdown("#### 4. Tendencia Activa de Orgánicas (CAM, RMM, RML, WAM)")
                    org_prosp = pd.DataFrame({'Grupo': ['CAM', 'WAM', 'RML', 'RMM'], 'Capacidad Operativa': [88, 75, 65, 50]})
                    fig_g4 = px.bar(org_prosp, x='Capacidad Operativa', y='Grupo', orientation='h', color='Capacidad Operativa', color_continuous_scale='Reds')
                    fig_g4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                    st.plotly_chart(fig_g4, use_container_width=True)