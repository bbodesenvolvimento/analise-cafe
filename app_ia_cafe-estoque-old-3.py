
import streamlit as st
import pandas as pd
import itertools

st.set_page_config(page_title="IA Café Estratégico", layout="wide")
st.title("☕ IA Estratégica para Compra e Venda de Café")
st.markdown("Automatize decisões de estoque com base em catação, custo médio e valor de mercado.")

st.header("📥 Envie o arquivo de estoque (.csv)")
arquivo = st.file_uploader("Seu arquivo precisa conter as colunas: Lote, Volume, Catacao, Custo", type=["csv"])

# Campos para inserção do mercado
st.sidebar.header("📈 Parâmetros de Análise")
valor_mercado = st.sidebar.number_input("💲 Valor de mercado da saca (R$)", min_value=0.0, value=2200.0, step=10.0)
catacao_minima = st.sidebar.number_input("📌 Catação mínima desejada (%)", min_value=0.0, value=25.0, step=1.0)
lucro_minimo = 60.0
custo_ideal_estoque = 2000.0

if arquivo:
    df = pd.read_csv(arquivo)
    df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")
    df["Catacao"] = pd.to_numeric(df["Catacao"], errors="coerce")
    df["Custo"] = pd.to_numeric(df["Custo"], errors="coerce")
    df = df.dropna(subset=["Volume", "Catacao", "Custo"])
    df = df[df["Volume"] > 0]

    st.subheader("📦 Estoque Atual")
    st.dataframe(df)

    st.header("🔁 Estratégias de Liga com Múltiplos Lotes")
    volumes_alvo = [250, 500, 750, 1000]
    ligas_multiplas = []

    for r in range(2, 6):  # combinações de 2 até 5 lotes
        for combinacao in itertools.combinations(df.iterrows(), r):
            lotes = [lote["Lote"] for _, lote in combinacao]
            volumes = [lote["Volume"] for _, lote in combinacao]
            catacoes = [lote["Catacao"] for _, lote in combinacao]
            custos = [lote["Custo"] for _, lote in combinacao]

            vol_total = sum(volumes)
            for alvo in volumes_alvo:
                if abs(vol_total - alvo) <= 10:
                    cat_media = sum(v * c for v, c in zip(volumes, catacoes)) / vol_total
                    custo_medio = sum(v * custo for v, custo in zip(volumes, custos)) / vol_total
                    lucro_por_saca = valor_mercado - custo_medio
                    if cat_media >= catacao_minima and lucro_por_saca >= lucro_minimo:
                        ligas_multiplas.append({
                            "Lotes combinados": ", ".join(lotes),
                            "Volume Total": round(vol_total, 2),
                            "Catação Média (%)": round(cat_media, 2),
                            "Custo Médio (R$)": round(custo_medio, 2),
                            "Lucro estimado/saca (R$)": round(lucro_por_saca, 2),
                            "Meta de Volume": alvo
                        })

    df_ligas = pd.DataFrame(ligas_multiplas)

    if not df_ligas.empty:
        st.success(f"✅ {len(df_ligas)} estratégias encontradas com lucro ≥ R$ {lucro_minimo}")
        st.dataframe(df_ligas)
        csv = df_ligas.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar estratégias de venda", csv, "estrategias_lucro.csv", "text/csv")
    else:
        st.warning("⚠️ Nenhuma liga encontrada com os critérios.")

    st.header("📉 Análise do custo médio do estoque")
    total_volume = df["Volume"].sum()
    custo_total = sum(df["Volume"] * df["Custo"])
    custo_medio_atual = custo_total / total_volume

    st.metric("🎯 Custo médio atual (R$/saca)", f"R${custo_medio_atual:.2f}")
    if custo_medio_atual > custo_ideal_estoque:
        st.error("⚠️ Custo médio está acima da meta de R$ 2000.")
        st.markdown("🔽 Sugerido: Comprar cafés com custo menor para equilibrar o estoque.")
    else:
        st.success("✅ Custo médio está dentro do ideal.")

else:
    st.info("Envie o arquivo CSV para iniciar a análise.")
