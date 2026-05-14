import streamlit as st

def main():
    st.set_page_config(page_title="Calculadora de Viabilidade EV", layout="wide")
    
    st.title("⚡ Calculadora de Negócio")
    st.markdown("---")

    # Layout em duas colunas para comparar os cenários
    col1, col2 = st.columns(2)

    with col1:
        st.header("Operação com UC Própria (Cativo)")
        
        # Inputs de Operação
        potencia = st.number_input("Potência do carregador (kW)", value=80.0, step=1.0, key="p1")
        tempo = st.slider("Tempo de operação (h)", 1, 24, 24, key="t1")
        taxa_ocupacao = st.slider("Taxa de ocupação (%)", 0, 100, 10, key="to1") / 100
        
        # Cálculos de Energia
        energia_dia = potencia * tempo * taxa_ocupacao
        energia_mes = energia_dia * 30
        
        st.info(f"**Energia comercializada/dia:** {energia_dia:.2f} kWh")
        st.info(f"**Energia comercializada/mês:** {energia_mes:.2f} kWh")

        # Financeiro
        preco_custo = st.number_input("Preço de custo (R$/kWh)", value=0.95, key="pc1")
        preco_venda = st.number_input("Preço de venda (R$/kWh)", value=2.40, key="pv1")
        
        receita_bruta = energia_mes * preco_venda
        csp = energia_mes * preco_custo # Custo do Serviço Prestado
        
        # Software e Impostos
        take_rate = st.number_input("Take Rate Software (%)", value=7.0, key="tr1") / 100
        custo_fixo_soft = st.number_input("Custo fixo Software (R$)", value=30.0, key="cf1")
        impostos_taxa = st.number_input("Impostos (%)", value=12.0, key="im1") / 100
        
        custo_total_soft = (receita_bruta * take_rate) + custo_fixo_soft
        custo_impostos = receita_bruta * impostos_taxa
        
        resultado_op = receita_bruta - csp - custo_total_soft - custo_impostos
        lucratividade = (resultado_op / receita_bruta) if receita_bruta > 0 else 0

        # Investimento
        st.subheader("Investimento")
        inv_carregador = st.number_input("Investimento Carregador (R$)", value=95000.0, key="ic1")
        inv_instalacao = st.number_input("Instalação (R$)", value=20000.0, key="ii1")
        total_invest = inv_carregador + inv_instalacao
        
        payback = total_invest / resultado_op if resultado_op > 0 else 0

        # Resultados em destaque
        st.metric("Receita Bruta", f"R$ {receita_bruta:,.2f}")
        st.metric("Resultado Operacional", f"R$ {resultado_op:,.2f}")
        st.metric("Lucratividade", f"{lucratividade*100:.2f}%")
        st.success(f"**Payback Estimado:** {payback:.1f} meses")

if __name__ == "__main__":
    main()