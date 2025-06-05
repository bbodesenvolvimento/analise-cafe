
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="IA Café Commodity", layout="centered")

st.title("☕ IA Café Commodity")
st.write("Análise de mercado e estratégia personalizada com base no seu estoque e margem de lucro.")

# Inputs do usuário
volume = st.number_input("📦 Volume do seu estoque (em sacas)", value=1000)
custo_medio = st.number_input("💰 Custo médio por saca (R$)", value=750.0)
margem_desejada = st.number_input("📈 Margem de lucro desejada por saca (R$)", value=150.0)

# Cotação atual
st.markdown("---")
st.subheader("📊 Cotação atual do Café Contrato C")
dados = yf.download("KC=F", period="7d", interval="1d")

if not dados.empty and not dados['Close'].isna().all():
    preco_dolar = dados['Close'].dropna().iloc[-1]
    preco_atual = preco_dolar * 5.5  # conversão estimada para R$/saca

    st.metric("💲 Preço atual estimado (R$/saca)", f"R${preco_atual:.2f}")

    # Cálculo da meta e da margem
    meta_venda = custo_medio + margem_desejada
    margem = preco_atual - custo_medio
    st.metric("📈 Margem atual", f"R${margem:.2f}")
    st.metric("🎯 Meta de venda", f"R${meta_venda:.2f}")

    # Estratégia sugerida
    st.markdown("---")
    st.subheader("📌 Recomendação Estratégica")

    if preco_atual >= meta_venda:
        st.success("✅ Meta de lucro atingida! Avalie venda parcial ou total do estoque.")
    elif margem > 0:
        st.warning("🔄 Está no lucro, mas ainda não atingiu a margem desejada. Considere hedge ou venda parcial.")
    else:
        st.info("⏳ Preço abaixo do custo. Melhor segurar por enquanto.")
else:
    st.error("❌ Não foi possível obter a cotação atual do café. Tente novamente em alguns minutos.")

st.markdown("---")
st.caption("Desenvolvido para produtores e negociadores de café. Dados via Yahoo Finance.")
