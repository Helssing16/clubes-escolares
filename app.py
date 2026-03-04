import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Inscrição nos Clubes", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

st.title("🏆 Inscrição nos Clubes Juvenis")

if 'Turma' in df.columns:
    turmas = sorted(df['Turma'].dropna().unique())
    abas = st.tabs(turmas)
    for i, turma in enumerate(turmas):
        with abas[i]:
            df_sala = df[df['Turma'] == turma]
            st.dataframe(df_sala[['Nome', 'Clube']], use_container_width=True, hide_index=True)
