import streamlit as st

# Dados simulados (que viriam do Google Sheets)
clubes = {
    "Robótica": {"pres": "João Silva", "vice": "Maria Oliveira", "vagas": 20, "ocupadas": 12},
    "E-sports": {"pres": "Pedro Santos", "vice": "Ana Costa", "vagas": 15, "ocupadas": 10},
    "Teatro": {"pres": "Lucas Lima", "vice": "Julia Souza", "vagas": 25, "ocupadas": 5}
}

st.title("🏆 Inscrição nos Clubes Juvenis")

# 1. Seleção do Clube
clube_selecionado = st.selectbox("Selecione o Clube para ver os detalhes:", list(clubes.keys()))

# 2. Exibição dos Responsáveis (Presidente e Vice)
info = clubes[clube_selecionado]
vagas_restantes = info['vagas'] - info['ocupadas']

col1, col2 = st.columns(2)
with col1:
    st.info(f"**👤 Presidente:** {info['pres']}")
    st.info(f"**👥 Vice-Presidente:** {info['vice']}")

with col2:
    st.metric(label="Vagas Restantes", value=vagas_restantes)

# 3. Formulário de Inscrição
with st.form("inscricao_aluno"):
    st.write("---")
    nome_aluno = st.text_input("Seu Nome Completo")
    turma = st.selectbox("Sua Turma", ["1ª Série A", "1ª Série B", "2ª Série A", "3ª Série A"])
    
    btn_confirmar = st.form_submit_button("Confirmar Inscrição")

if btn_confirmar:
    if vagas_restantes > 0:
        st.success(f"Inscrição realizada! Procure o(a) {info['pres']} para saber os horários.")
        # Lógica para salvar na planilha aqui
    else:
        st.error("Desculpe, este clube já atingiu o limite de vagas.")