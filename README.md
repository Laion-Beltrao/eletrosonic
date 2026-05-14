# ⚡ EletroSonic

Plataforma de análise e previsão da frota de veículos elétricos e híbridos no Brasil, com módulo de calculadora de viabilidade para negócios de recarga.

---

### `dashboard.py` — Dashboard de Frota Elétrica

Dashboard interativo construído com **Dash + Plotly** para visualização da frota de veículos elétricos e híbridos em cada estado brasileiro.

**Funcionalidades:**
- KPIs: total de elétricos/híbridos, participação na frota, estado líder
- Filtro por estado e alternância entre quantidade absoluta e proporção (%)
- Gráfico de barras por estado
- Ranking Top 10 estados por proporção da frota verde
- Gráfico de dispersão: frota total vs. elétricos+híbridos

**Fonte dos dados:** Ministério dos Transportes — Frota 2025

---

### `calculadora.py` — Calculadora de Negócio

Calculadora de viabilidade financeira para operação de pontos de recarga em Unidade Consumidora (UC) própria, no mercado cativo.

**Entradas configuráveis:**
| Potência do carregador (kW) - Capacidade instalada 
| Tempo de operação (h/dia) - Horas de funcionamento diário 
| Taxa de ocupação (%) - Percentual de uso do carregador 
| Preço de custo (R$/kWh) - Tarifa de compra da distribuidora
| Preço de venda (R$/kWh) - Tarifa cobrada do usuário final 
| Taxa de software (%) - Comissão variável da plataforma de gestão 
| Custo fixo do software (R$) - Mensalidade fixa da plataforma 
| Imposto (%) - Carga tributária sobre a receita 
| Investimento total (R$) - Carregador + material de instalação + mão de obra

**Resultados calculados:**
- Energia comercializada por dia e por mês (kWh)
- Receita bruta mensal
- Resultado operacional mensal
- Lucratividade (%)
- **Payback estimado** em meses

---

### `funcao.py` — Previsão de Frota por Município

Função de machine learning para projeção da frota elétrica de um município com base no histórico de registros mensais.

```python
prever_frota_eletrica(df, uf, municipio, meses_futuros=6)
```

**Parâmetros:**
| `df` - Base consolidada de veículos
| `uf` - Estado (ex: `'MINAS GERAIS'`)
| `municipio` - Cidade (ex: `'BELO HORIZONTE'`)
| `meses_futuros` - Horizonte de previsão (padrão: 6)

**Saída:**
- Crescimento mensal estimado (veículos/mês)
- Métricas do modelo: R2 e MAE
- Projeção mensal
- Gráfico histórico + linha de projeção

---

## 🛠️ Tecnologias
|  Dash - Framework web interativo
|  Plotly - Visualizações gráficas
|  Pandas - Manipulação de dados
|  Scikit-learn - Modelo de regressão linear
|  NumPy -  Operações numéricas
|  Matplotlib / Seaborn - Gráficos estáticos
|  os - Manipular arquivos