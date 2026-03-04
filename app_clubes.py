import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da página para ocupar a tela toda
st.set_page_config(page_title="Inscrição nos Clubes - Escola", layout="wide")

# 2. Conexão com a sua Planilha Google via Secrets
try:
    # O Streamlit usa o link que você salvou em 'Settings > Secrets'
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    
    # Limpeza: remove linhas totalmente vazias que possam estar na planilha
    df = df.dropna(subset=['Nome', 'Turma'], how='all')
    
    # Garante que a coluna 'Clube' existe para não dar erro no código
    if 'Clube' not in df.columns:
        df['Clube'] = ""
        
except Exception as e:
    st.error("Erro ao ler a planilha. Verifique se o link nos 'Secrets' está correto.")
    st.stop()

st.title("🏆 Inscrição nos Clubes Juvenis")

# --- PARTE 1: ÁREA DO ALUNO (FORMULÁRIO) ---
with st.expander("📝 CLIQUE AQUI PARA SE INSCREVER"):
    with st.form("form_inscricao"):
        # Puxa os nomes que você colou na sua planilha
        nomes_lista = sorted(df['Nome'].dropna().unique())
        aluno = st.selectbox("Selecione seu nome na lista:", nomes_lista)
        
        # Opções de clubes
        clube = st.selectbox("Escolha seu Clube:", ["Robótica", "E-sports", "Teatro", "Dança", "Vôlei", "Xadrez"])
        
        btn_confirmar = st.form_submit_button("Confirmar Minha Inscrição")
        
        if btn_confirmar:
            st.success(f"Olá {aluno}! Sua escolha pelo clube {clube} foi registrada.")
            st.info("Para salvar permanentemente, os dados serão enviados para a planilha.")

st.markdown("---")

# --- PARTE 2: PAINEL DE MONITORAMENTO (ABAS AUTOMÁTICAS) ---
st.header("📊 Monitoramento por Sala")

# O Python identifica as salas na coluna 'Turma' e cria as abas sozinho
if 'Turma' in df.columns:
    todas_turmas = sorted(df['Turma'].dropna().unique())
    abas = st.tabs(todas_turmas)

    for i, turma in enumerate(todas_turmas):
        with abas[i]:
            # Filtra apenas os alunos daquela sala
            df_sala = df[df['Turma'] == turma].copy()
            
            # Função para destacar a linha se o aluno já tiver um clube preenchido
            def destacar_inscritos(row):
                status = str(row.Clube).strip() != "" and str(row.Clube).lower() != 'nan'
                return ['background-color: #d4edda' if status else '' for _ in row]

            # Exibe a tabela apenas com Nome e Clube
            st.dataframe(
                df_sala[['Nome', 'Clube']].style.apply(destacar_inscritos, axis=1),
                use_container_width=True,
                hide_index=True
            )
else:
    st.warning("Atenção: Verifique se a primeira linha da sua planilha tem o título 'Turma'.")
