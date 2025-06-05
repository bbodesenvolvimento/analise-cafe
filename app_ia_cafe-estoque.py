
import streamlit as st
import pandas as pd
import itertools

st.set_page_config(page_title="IA Café Estratégico", layout="wide")
st.title("☕ IA Estratégica para Compra e Venda de Café")
st.markdown("Automatize decisões de estoque com base em catação, custo médio e valor de mercado.")

st.header("📥 Envie o arquivo de estoque (.csv)")
arquivo = st.file_uploader("Seu arquivo precisa conter as colunas: Lote, Volume, Catacao, Custo", type=["csv"])

st.sidebar.header("📈 Parâmetros de Análise")
valor_mercado = st.sidebar.number_input("💲 Valor de mercado da saca (R$)", min_value=0.0, value=2200.0, step=10.0)
catacao_minima = st.sidebar.number_input("📌 Catação mínima desejada (%)", min_value=0.0, value=25.0, step=1.0)
catacao_maxima = st.sidebar.number_input("🚫 Catação máxima permitida (%)", min_value=0.0, value=85.0, step=1.0)
lucro_minimo = 60.0
custo_ideal_estoque = 2000.0
volumes_alvo = [1000, 750, 500, 250]  # Prioridade para maiores volumes

if arquivo:
    df = pd.read_csv(arquivo)
    df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")
    df["Catacao"] = pd.to_numeric(df["Catacao"], errors="coerce")
    df["Custo"] = pd.to_numeric(df["Custo"], errors="coerce")
    df = df.dropna(subset=["Volume", "Catacao", "Custo"])
    df = df[df["Volume"] > 0]
    estoque_original = df.copy()

    st.subheader("📦 Estoque Atual")
    st.dataframe(df)

    st.header("🔁 Estratégias de Liga com Múltiplos Lotes")
    ligas_multiplas = []
    lotes_utilizados = set()

    for alvo in volumes_alvo:
        candidatos = df[~df["Lote"].isin(lotes_utilizados)].copy()
        candidatos = candidatos[candidatos["Volume"] >= 1]

        for r in range(2, len(candidatos)+1):
            for combinacao in itertools.combinations(candidatos.iterrows(), r):
                lotes = [lote["Lote"] for _, lote in combinacao]
                if any(l in lotes_utilizados for l in lotes):
                    continue

                volumes = [lote["Volume"] for _, lote in combinacao]
                catacoes = [lote["Catacao"] for _, lote in combinacao]
                custos = [lote["Custo"] for _, lote in combinacao]

                vol_total = sum(volumes)
                if abs(vol_total - alvo) <= 10:
                    cat_media = sum(v * c for v, c in zip(volumes, catacoes)) / vol_total
                    if not (catacao_minima <= cat_media <= catacao_maxima):
                        continue
                    custo_medio = sum(v * custo for v, custo in zip(volumes, custos)) / vol_total
                    lucro_por_saca = valor_mercado - custo_medio
                    if lucro_por_saca >= lucro_minimo:
                        ligas_multiplas.append({
                            "Lotes combinados": ", ".join(lotes),
                            "Volume Total": round(vol_total, 2),
                            "Catação Média (%)": round(cat_media, 2),
                            "Custo Médio (R$)": round(custo_medio, 2),
                            "Lucro estimado/saca (R$)": round(lucro_por_saca, 2),
                            "Meta de Volume": alvo
                        })
                        lotes_utilizados.update(lotes)
                        break
            else:
                continue
            break

    df_ligas = pd.DataFrame(ligas_multiplas)

    if not df_ligas.empty:
        st.success(f"✅ {len(df_ligas)} estratégias encontradas com lucro ≥ R$ {lucro_minimo}")
        st.dataframe(df_ligas)

        total_sacas = df_ligas["Volume Total"].sum()
        cat_media_total = df_ligas["Catação Média (%)"].mean()
        custo_medio_total = df_ligas["Custo Médio (R$)"].mean()

        st.subheader("📊 Análise das Ligas Geradas")
        st.metric("🔢 Total de sacas utilizadas", f"{total_sacas:.0f}")
        st.metric("🧮 Catação média geral (%)", f"{cat_media_total:.2f}")
        st.metric("💰 Custo médio geral (R$)", f"R${custo_medio_total:.2f}")

        csv_ligas = df_ligas.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar estratégias de venda", csv_ligas, "estrategias_lucro.csv", "text/csv")
    else:
        st.warning("⚠️ Nenhuma liga encontrada com os critérios.")

    st.header("📦 Estoque Residual (não utilizado nas ligas)")
    estoque_residual = df[~df["Lote"].isin(lotes_utilizados)].copy()
    if not estoque_residual.empty:
        st.dataframe(estoque_residual)
        volume_residual = estoque_residual["Volume"].sum()
        catacao_residual = (estoque_residual["Volume"] * estoque_residual["Catacao"]).sum() / volume_residual
        custo_residual = (estoque_residual["Volume"] * estoque_residual["Custo"]).sum() / volume_residual

        st.metric("📉 Volume residual (sacas)", f"{volume_residual:.0f}")
        st.metric("📉 Catação média residual (%)", f"{catacao_residual:.2f}")
        st.metric("📉 Custo médio residual (R$)", f"R${custo_residual:.2f}")

        csv_residual = estoque_residual.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar estoque residual", csv_residual, "estoque_residual.csv", "text/csv")

else:
    st.info("Envie o arquivo CSV para iniciar a análise.")
