# ==============================================================================
# Archivo: cerebro_rag_macrozona.py
# Rol C5I: Consola Maestra RAG de Inteligencia Relacional y Prospectiva
# Versión: 8.0 (Arquitectura macOS Optimizada | Extracción SNA Temporal)
# Descripción: Conecta Supabase con ChromaDB y Ollama local (qwen2.5:14b nativo).
#              1. Estabilización de flujos de tensores para Apple Silicon M5.
#              2. Extracción de aristas SNA enriquecidas con anclaje temporal.
#              3. Pluma ejecutiva corporativa y blindaje de activos CMPC.
#              4. Supresión nativa de alucinaciones visuales y texto redundante.
# ==============================================================================

import sys
import os
import re
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# --- IMPORTACIONES OPERATIVAS OSINT ---
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# --- 1. CREDENCIALES DE LA BÓVEDA SUPABASE ---
URL_SUPABASE = "https://wffttolclywvofzakmfd.supabase.co"
API_KEY_SUPABASE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZnR0b2xjbHl3dm9memFrbWZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5MjMyOTksImV4cCI6MjA5MzQ5OTI5OX0.8vzHsEjPvZBf49VMCl1G8PtFYXLoxYSrzhbrYIBNEcU"
supabase: Client = create_client(URL_SUPABASE, API_KEY_SUPABASE)

def construir_fragmento_limpio(fila):
    """Construye el bloque de texto RAG eliminando ruido y aplicando limpieza estricta."""
    actor_part = f"ACTOR_ORIGEN: {fila['actor']} | " if str(fila['actor']).strip().lower() != 'desconocido' else ""
    return (
        f"FECHA: {fila['fecha']} | UBICACIÓN: {fila['ubicacion']} | {actor_part}"
        f"TÁCTICA: {fila['accion_digital']}\n"
        f"AFECTADOS: {fila['modificadores']}\n"
        f"TITULAR: {fila['titular']}\n"
        f"RESUMEN: {fila['resumen_ia']}"
    )

def sincronizar_memoria_supabase(directorio_db="./bd_macrozona_vectorial"):
    print("🗄️ [1] Descargando inventario estratégico desde la bóveda Supabase...")
    registros = []
    try:
        inicio, lote = 0, 1000
        while True:
            res = supabase.table("inteligencia_tactica").select("*").order("id").range(inicio, inicio + lote - 1).execute()
            if not res.data: break
            registros.extend(res.data)
            print(f"   ↳ Consolidando: {len(registros)} trazas fácticas capturadas...")
            if len(res.data) < lote: break
            inicio += lote
        df = pd.DataFrame(registros)
        print(f"✔️ Sincronización exitosa: {len(df)} incidentes tácticos listos para destilación.")
    except Exception as e:
        print(f"❌ Error crítico de conexión con Supabase: {e}")
        return None

    if df.empty: return None

    df['contexto_completo'] = df.apply(construir_fragmento_limpio, axis=1)

    loader = DataFrameLoader(df, page_content_column="contexto_completo")
    documentos = loader.load()
    
    print("🧠 [2] Compilando tensores locales y Embeddings Multilingües...")
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    
    print("📂 [3] Generando persistencia en base vectorial ChromaDB...")
    return Chroma.from_documents(documents=documentos, embedding=embeddings, persist_directory=directorio_db)

def obtener_cadenas_analiticas(vector_db):
    """Estructura las compuertas de razonamiento conectadas de forma nativa a qwen2.5:14b."""
    llm = Ollama(model="qwen2.5:14b", temperature=0.0)
    fecha_actual_sistema = datetime.now().strftime("%A %d de %B de %Y, %H:%M hrs")

    # ==========================================================================
    # CEREBRO 1: MODO SNA GRAFOS TEMPORALES (Extracción Optimizada | k=30)
    # ==========================================================================
    plantilla_sna = """
    ESTADO MAYOR C5I - MÓDULO DE EXTRACCIÓN DE ARISTAS TEMPORALES
    
    Analiza la información fáctica contenida en el siguiente bloque de memoria ({context}) y procesa la solicitud: {question}
    
    DOCTRINA DE EXTRACCIÓN DE GRAFOS:
    1. Identifica actores operacionales reales: Orgánicas (CAM, RML, WAM), perfiles de RRSS infiltrados, empresas forestales, predios y contratistas.
    2. Es mandatorio capturar la fecha o mes aproximado del suceso para dotar de dinamismo temporal al análisis de red.
    3. Genera exclusivamente líneas de texto limpias estructuradas bajo el siguiente formato estricto:
       [Actor Origen] -> [Acción/Relación (Fecha)] -> [Nodo Destino]
    4. Tienes terminantemente prohibido generar diálogos, explicaciones introductorias, enumeraciones o conclusiones de cierre. Escribe únicamente las aristas extraídas.
    
    EJEMPLO DE SALIDA ESPERADA:
    CAM -> reivindica sabotaje (23/05/2025) -> CMPC Fundo Porvenir
    Resistencia Mapuche Lavkenche -> ejecuta ataque (06/12/2024) -> Faena Forestal Contulmo
    radiokurruf -> amplifica comunicado (12/04/2025) -> Caso Prisioneros Políticos
    
    Matriz pura de aristas extraídas:
    """
    prompt_sna = PromptTemplate(template=plantilla_sna, input_variables=["context", "question"])
    cadena_sna = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 30}), # Equilibrio óptimo de densidad y rendimiento M5
        chain_type_kwargs={"prompt": prompt_sna}
    )

    # ==========================================================================
    # CEREBRO 2: MODO GENERAL (k=25 | PLUMA EJECUTIVA | BLINDAJE CMPC)
    # ==========================================================================
    plantilla_general = f"""
    ESTADO MAYOR C5I - UNIDAD DE ANÁLISIS ESTRATÉGICO Y PROSPECTIVA
    LÍNEA TEMPORAL ACTUAL DEL SISTEMA: {fecha_actual_sistema}
    
    Utiliza de forma exclusiva la información fáctica presente en nuestra memoria vectorial para responder el requerimiento:
    {{context}}
    
    Parámetro de Batida Estratégica: {{question}}
    
    DOCTRINA DE REDACCIÓN CORPORATIVA (PLUMA DE ÉLITE):
    1. ROL: Eres el analista jefe de prospectiva corporativa. Redacta con un estilo sobrio, institucional, fluido y altamente persuasivo, diseñado para ser leído por el Directorio y la Gerencia General. Utiliza léxico técnico avanzado (vectores de amenaza, escalada de conflicto, anillos de contención, tracción orgánica).
    2. REGLA DE ACTIVOS CMPC: Aplica máxima rigurosidad al ponderar sucesos que involucren directa o indirectamente a CMPC, sus contratistas o predios. Por mandato doctrinal, todo incidente contra la compañía debe ser expuesto como un vector de riesgo CRÍTICO.
    3. FORMATO AUTOMATIZADO: Estructura tu respuesta en bloques lógicos limpios, listos para integrarse en el documento automatizado Word bajo la doctrina "Radar de crisis".
    4. SUPRESIÓN DE RUIDO VISUAL: Si el contexto carece por completo de trazas fácticas asociadas a la consulta, imprime de forma solitaria: "Sin registros fácticos detectados en esta batida de monitoreo". Si logras redactar al menos una viñeta o hito válido en una sección, TIENES ESTRICTAMENTE PROHIBIDO imprimir esa frase de resguardo al final del bloque.
    
    Minuta Oficial C5I:
    """
    prompt_general = PromptTemplate(template=plantilla_general, input_variables=["context", "question"])
    cadena_general = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 25}),
        chain_type_kwargs={"prompt": prompt_general}
    )

    return cadena_sna, cadena_general

def post_procesar_aristas(texto_bruto):
    """Filtra y normaliza líneas de aristas puras eliminando cualquier residuo conversacional de la IA."""
    lineas = texto_bruto.split('\n')
    aristas_unicas = []
    vistas = set()
    for l in lineas:
        l_str = l.strip()
        if '->' in l_str:
            norm = " ".join(l_str.split())
            norm = re.sub(r'^\d+[\.\-\)]\s*', '', norm) # Elimina viñetas numéricas accidentales
            if norm not in vistas:
                vistas.add(norm)
                aristas_unicas.append(norm)
    return "\n".join(aristas_unicas) if aristas_unicas else texto_bruto.strip()

if __name__ == "__main__":
    carpeta_db_local = "./bd_macrozona_vectorial"
    print("="*65)
    print("🛡️ COMANDO C5I - CONSOLA DE INTELIGENCIA Y ARS (v8.0 macOS) 🛡️")
    print("="*65)

    if os.path.exists(carpeta_db_local) and os.listdir(carpeta_db_local):
        print("📂 Interrogando tensores de memoria vectorial activa...")
        embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
        db_conocimiento = Chroma(persist_directory=carpeta_db_local, embedding_function=embeddings)
        actualizar = input("¿Forzar resincronización y purga desde Supabase? (s/n): ").strip().lower()
        if actualizar == 's':
            db_conocimiento = sincronizar_memoria_supabase(carpeta_db_local)
    else:
        db_conocimiento = sincronizar_memoria_supabase(carpeta_db_local)

    if db_conocimiento:
        cadena_grafos, cadena_libre = obtener_cadenas_analiticas(db_conocimiento)
        while True:
            print("\n" + "─"*65)
            print(" SELECCIONE COMPUERTA DE MANDO:")
            print(" [S] Extracción de Aristas SNA Temporales (CSV / Gephi)")
            print(" [G] Destilación Ejecutiva / Radar de Crisis Corporativo")
            print(" [Q] Desconectar Terminal")
            print("─"*65)
            
            modo = input(" MODO ❯ ").strip().upper()
            if modo == 'Q' or modo == 'SALIR': break
            if modo not in ['S', 'G']: continue

            prefijo = "SNA GRAFOS" if modo == 'S' else "RADAR / EJECUTIVO"
            pregunta = input(f"\n COMANDO C5I ({prefijo}) ❯ ").strip()
            if not pregunta: continue

            print("⏳ Proyectando inferencia neuronal profunda en qwen2.5:14b...\n")
            try:
                if modo == 'S':
                    res_bruta = cadena_grafos.invoke({"query": pregunta})
                    salida_limpia = post_procesar_aristas(res_bruta['result'])
                    print("─── MATRIZ DE ARISTAS TEMPORALES PURAS (GEPHI) ────────────────")
                    print(salida_limpia)
                    print("───────────────────────────────────────────────────────────────")
                else:
                    res_bruta = cadena_libre.invoke({"query": pregunta})
                    print("─── MINUTA DE INTELIGENCIA ESTRATÉGICA C5I ────────────────────")
                    print(res_bruta['result'].strip())
                    print("───────────────────────────────────────────────────────────────")
            except Exception as e:
                print(f"❌ Fallo crítico en el hilo de razonamiento: {e}")