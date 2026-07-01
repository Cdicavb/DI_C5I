"""
Módulo: Análisis de Redes (SNA)
Rol: Topología relacional de amenazas
"""
import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
from utils_c5i import COMUNAS_PURGADAS

def render_sna(df_filtrado):
    st.subheader("🕸️ Topología Relacional de Amenazas (SNA Interactivo)")
    st.markdown("El nodo de inteligencia procesa las fricciones permitiendo el arrastre dinámico y el scroll del ratón. Los incidentes críticos poseen una jerarquía visual dominante (tamaño aumentado).")
    
    if not df_filtrado.empty:
        df_net = df_filtrado[["actor", "ubicacion", "tipologia_oficial", "nivel_alerta", "titular"]].dropna().copy()
        terminos_excluidos = ['desconocido', 'no atribuido', 'sin dato', 'no especificado', '', 'mzs', 'macrozona sur'] + COMUNAS_PURGADAS
        df_net = df_net[~df_net['actor'].str.lower().str.strip().isin(terminos_excluidos)]
        df_net = df_net[~df_net['ubicacion'].str.lower().str.strip().isin(terminos_excluidos)]
        
        if len(df_net) > 0:
            net = Network(height="650px", width="100%", bgcolor="#05080f", font_color="#f8fafc", directed=True)
            net.barnes_hut(gravity=-8000, central_gravity=0.2, spring_length=180, spring_strength=0.04, damping=0.1)
            
            net.set_options("""
            var options = {
              "interaction": {
                "dragNodes": true,
                "zoomView": true
              }
            }
            """)
            
            nodos_agregados = set()
            for _, row in df_net.head(75).iterrows():
                actor = str(row['actor']).strip()
                target = str(row['ubicacion']).strip()
                alerta = str(row['nivel_alerta']).upper()
                tipo_of = str(row['tipologia_oficial'])
                
                c_edge = "#334155"
                if tipo_of == 'Ataque Incendiario': c_edge = "#ff4b4b"
                elif 'Allanamiento' in tipo_of: c_edge = "#a855f7"
                elif tipo_of == 'Robo de Madera': c_edge = "#f6a821"
                elif tipo_of == 'Usurpación': c_edge = "#10b981"
                
                c_actor = "#ff4b4b" if alerta == 'CRÍTICO' else "#f6a821" if any(x in actor.upper() for x in ['CAM','RML','WAM','ORT']) else "#38bdf8"
                size_target = 35 if alerta == 'CRÍTICO' else 25 if alerta == 'ALTO' else 15
                
                if actor not in nodos_agregados:
                    net.add_node(actor, label=actor, color=c_actor, shape="dot", size=30)
                    nodos_agregados.add(actor)
                if target not in nodos_agregados:
                    net.add_node(target, label=target, color="#64748b", shape="square", size=size_target)
                    nodos_agregados.add(target)
                
                net.add_edge(actor, target, title=f"{tipo_of}: {str(row['titular'])[:50]}", color=c_edge)
            
            try:
                net.save_graph("matriz_sna_cmpc.html")
                with open("matriz_sna_cmpc.html", 'r', encoding='utf-8') as f:
                    components.html(f.read(), height=680)
            except Exception as e:
                st.error(f"Fallo al renderizar la topología del grafo: {e}")
        else:
            st.info("Pares relacionales insuficientes para trazar la topología.")