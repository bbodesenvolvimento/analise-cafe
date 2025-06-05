{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8fff062b",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# 📊 IA Café Commodity - Análise de Mercado + Estratégia Personalizada com Margem de Lucro\n",
    "\n",
    "# Etapa 1: Instalar bibliotecas\n",
    "!pip install yfinance ipywidgets --quiet\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ec1c9d02",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Etapa 2: Importar bibliotecas\n",
    "import yfinance as yf\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import ipywidgets as widgets\n",
    "from IPython.display import display, clear_output\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "46aefbc2",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Etapa 3: Coletar dados do Café Contrato C\n",
    "dados = yf.download(\"KC=F\", start=\"2020-01-01\")\n",
    "\n",
    "# Calcular médias móveis\n",
    "dados['SMA_10'] = dados['Close'].rolling(window=10).mean()\n",
    "dados['SMA_30'] = dados['Close'].rolling(window=30).mean()\n",
    "\n",
    "# Gerar sinais\n",
    "dados['Sinal'] = 0\n",
    "dados.loc[dados['SMA_10'] > dados['SMA_30'], 'Sinal'] = 1\n",
    "dados.loc[dados['SMA_10'] < dados['SMA_30'], 'Sinal'] = -1\n",
    "\n",
    "# Gráfico com médias móveis\n",
    "dados[['Close', 'SMA_10', 'SMA_30']].plot(figsize=(12, 6), grid=True)\n",
    "plt.title(\"📈 Preço do Café Contrato C com Médias Móveis\")\n",
    "plt.xlabel(\"Data\")\n",
    "plt.ylabel(\"Preço (USD)\")\n",
    "plt.show()\n",
    "\n",
    "# Mostrar último sinal\n",
    "ultimo_sinal = dados['Sinal'].iloc[-1]\n",
    "print(\"📍 Último sinal de operação:\", \"🔼 COMPRA\" if ultimo_sinal == 1 else \"🔽 VENDA\" if ultimo_sinal == -1 else \"⏸️ NEUTRO\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6bb5a6c9",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Etapa 4: Formulário de Estoque + Estratégia com Margem de Lucro\n",
    "\n",
    "# Widgets para entrada de dados\n",
    "volume_estoque = widgets.FloatText(description='Estoque (sacas):', value=1000)\n",
    "custo_medio = widgets.FloatText(description='Custo médio (R$/saca):', value=750)\n",
    "margem_desejada = widgets.FloatText(description='Margem desejada (R$):', value=150)\n",
    "botao_estoque = widgets.Button(description='Analisar Estratégia')\n",
    "saida_estoque = widgets.Output()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "50a8e23d",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Função de análise estratégica\n",
    "def analisar_estoque(b):\n",
    "    with saida_estoque:\n",
    "        clear_output()\n",
    "        print(\"🔍 Analisando mercado e estoque...\")\n",
    "\n",
    "        dados_atuais = yf.download(\"KC=F\", period=\"7d\", interval=\"1d\")\n",
    "\n",
    "        if not dados_atuais.empty and not dados_atuais['Close'].isna().all():\n",
    "            preco_dolar = dados_atuais['Close'].dropna().iloc[-1]\n",
    "            preco_atual = preco_dolar * 5.5  # conversão estimada\n",
    "\n",
    "            meta_venda = custo_medio.value + margem_desejada.value\n",
    "            margem = preco_atual - custo_medio.value\n",
    "\n",
    "            print(f\"📦 Volume atual: {volume_estoque.value} sacas\")\n",
    "            print(f\"💲 Custo médio: R${custo_medio.value:.2f}\")\n",
    "            print(f\"📈 Margem desejada: R${margem_desejada.value:.2f}\")\n",
    "            print(f\"🎯 Meta de venda (calculada): R${meta_venda:.2f}\")\n",
    "            print(f\"📉 Preço atual estimado: R${preco_atual:.2f}\")\n",
    "            print(f\"🧾 Margem atual: R${margem:.2f}\")\n",
    "\n",
    "            if preco_atual >= meta_venda:\n",
    "                print(\"\\n✅ Recomendação: Meta de lucro atingida! Avaliar venda parcial ou total.\")\n",
    "            elif margem > 0:\n",
    "                print(\"\\n🔄 Recomendação: Está no lucro, mas abaixo da margem esperada. Considere hedge ou venda parcial.\")\n",
    "            else:\n",
    "                print(\"\\n⏳ Recomendação: Preço abaixo do custo. Melhor segurar por enquanto.\")\n",
    "        else:\n",
    "            print(\"❌ Não foi possível obter a cotação atual do café. Tente novamente em alguns minutos.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "cfdd1a74",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Exibir formulário\n",
    "botao_estoque.on_click(analisar_estoque)\n",
    "display(volume_estoque, custo_medio, margem_desejada, botao_estoque, saida_estoque)\n"
   ]
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}
