
import streamlit as st
import pandas as pd
import itertools

st.set_page_config(page_title="📈 IA Café Commodity - Gestão Estratégica", layout="centered")

st.title("☕ IA Café Commodity")
st.write("📦 Estratégia inteligente de ligas, compra e venda com base no seu estoque.")

# Upload do arquivo
uploaded_file = st.file_uploader("📂 Faça upload da sua planilha de estoque (formato CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Verificação de colunas obrigatórias
    colunas_necessarias = {"Lote", "Volume", "Catacao", "Custo"}
    if not colunas_necessarias.issubset(set(df.columns)):
        st.error(f"O CSV deve conter as colunas: {', '.join(colunas_necessarias)}")
    else:
        st.subheader("📋 Estoque Atual")
        st.dataframe(df)

        # Cálculo do estoque total e custo médio
        total_sacas = df["Volume"].sum()
        custo_medio_total = (df["Volume"] * df["Custo"]).sum() / total_sacas

        st.markdown(f"**📊 Total em estoque:** {total_sacas:.0f} sacas")
        st.markdown(f"**💰 Custo médio atual do estoque:** R${custo_medio_total:.2f}")

        st.markdown("---")
        st.subheader("🧪 Ligas Estratégicas")
        ligas = []
        for (i, lote1), (j, lote2) in itertools.combinations(df.iterrows(), 2):
            v1, c1, custo1 = lote1["Volume"], lote1["Catacao"], lote1["Custo"]
            v2, c2, custo2 = lote2["Volume"], lote2["Catacao"], lote2["Custo"]
            vol_total = v1 + v2
            cat_media = (c1 * v1 + c2 * v2) / vol_total
            custo_medio = (custo1 * v1 + custo2 * v2) / vol_total
            ligas.append({
                "Lote A": lote1["Lote"],
                "Lote B": lote2["Lote"],
                "Volume Liga": vol_total,
                "Catação Média (%)": round(cat_media, 2),
                "Custo Médio R$": round(custo_medio, 2)
            })

        df_ligas = pd.DataFrame(ligas)
        df_ligas = df_ligas.sort_values(by="Catação Média (%)", ascending=True)
        st.dataframe(df_ligas)

        st.markdown("---")
        st.subheader("🎯 Estratégia Recomendada")

        if total_sacas < 750:
            faltam = 750 - total_sacas
            st.warning(f"📉 Estoque abaixo do ideal. Recomendado comprar cerca de {faltam:.0f} sacas.")
        elif total_sacas > 1000:
            excedente = total_sacas - 1000
            st.warning(f"📈 Estoque acima do ideal. Avalie vender cerca de {excedente:.0f} sacas ou formar ligas estratégicas.")
        else:
            st.success("✅ Estoque dentro do intervalo ideal entre 750 e 1000 sacas.")

        st.caption("Critério de estoque ideal: 750 a 1000 sacas com custo médio de R$ 2000,00.")
else:
    st.info("⬆️ Faça upload de uma planilha .csv com colunas: Lote, Volume, Catacao, Custo")
