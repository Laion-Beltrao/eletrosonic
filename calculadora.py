from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__, title='Calculadora de Investimento')

# cores a serem utilizadas ---------------------------------------
COR_PRIMARIA   = '#00C896'   # verde
COR_SECUNDARIA = '#0A1628'   # azul escuro (fundo)
COR_CARD       = '#0F2040'   # fundo dos cards
COR_TEXTO      = '#8BAFC8'   # texto claro
COR_DESTAQUE   = '#FFD700'   # dourado para destaques
COR_BORDA      = '#1E3A5F'   # azul da borda

# estilo do card ---------------------------------------
estilo_card = {
    'backgroundColor': COR_CARD,
    'borderRadius': '12px',
    'padding': '20px',
    'border': f'1px solid {COR_BORDA}',
    'flex': '1',
    'minWidth': '200px',
    'textAlign': 'center',
}

# layout ---------------------------------------
app.layout = html.Div(
    style={
        'backgroundColor': '#F0F4F8',
        'minHeight': '100vh',
        'fontFamily': 'Segoe UI, Arial, sans-serif',
        'color': COR_TEXTO,
        'padding': '24px'
    },
    children=[

        # cabeçalho
        html.Div([
            html.H1('⚡ Calculadora de Negócio', style={'margin': '0px'}),
            html.P('Análise de Payback', style={'margin': '0px'})
        ], style={
            'color': COR_SECUNDARIA,
            'fontSize': '20px',
            'textAlign': 'center',
            'marginBottom': '30px',
            'borderBottom': f'2px solid {COR_PRIMARIA}',
            'paddingBottom': '16px'
        }),

        # título operação
        html.Div([
            html.H2('Operação com UC Própria (cativo)', style={'margin': '0px'}),
            html.P('Compra energia direto da distribuidora local', style={'margin': '0px 0px 20px 0px'})
        ], style={'color': COR_SECUNDARIA, 'fontSize': '15px', 'textAlign': 'center'}),

        # inputs de operação
        html.Div([
            # potência do carregador
            html.Div([
                html.H3('Potência do carregador (kW)',
                        style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                dcc.Input(
                    id='potencia_input',
                    type='number',
                    min=0, max=120, step=1, value=80,
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '6px', 'border': f'1px solid {COR_BORDA}'}
                ),
            ], style={'width': '350px'}),

            # tempo de operação
            html.Div([
                html.H3('Tempo de operação (h)',
                        style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                dcc.Slider(
                    id='tempo_operacao_slider',
                    min=0, max=24, step=1, value=12,
                    marks={i: str(i) for i in range(0, 25, 4)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={'width': '350px'}),

            # taxa de ocupação
            html.Div([
                html.H3('Taxa de Ocupação (%)',
                        style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                dcc.Slider(
                    id='taxa_ocupacao_slider',
                    min=0, max=100, step=1, value=15,
                    marks={i: f'{i}%' for i in range(0, 101, 20)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={'width': '350px'}),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'gap': '16px',
            'margin': '0px 100px 38px 100px',
            'flexWrap': 'wrap'
        }),

        # cards de energia
        html.Div([
            html.Div([
                html.P('Energia comercializada / dia',
                       style={'color': COR_TEXTO, 'margin': '0 0 8px 0', 'fontSize': '13px'}),
                html.H2(id='energia_dia',
                        style={'margin': '0', 'color': COR_PRIMARIA, 'fontSize': '28px'}),
            ], style=estilo_card),
            html.Div([
                html.P('Energia comercializada / mês',
                       style={'color': COR_TEXTO, 'margin': '0 0 8px 0', 'fontSize': '13px'}),
                html.H2(id='energia_mes',
                        style={'margin': '0', 'color': COR_PRIMARIA, 'fontSize': '28px'}),
            ], style=estilo_card),
        ], style={
            'display': 'flex',
            'gap': '16px',
            'margin': '0px 100px 24px 100px',
            'flexWrap': 'wrap'
        }),

        # inputs de custo/venda
        html.Div([
            html.Div([
                html.H3('Preço de custo (R$/kWh)',
                        style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                dcc.Input(
                    id='preco_custo',
                    type='number', min=0, max=5, step=0.01, value=0.95,
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '6px', 'border': f'1px solid {COR_BORDA}'}
                ),
            ], style={'width': '250px'}),

            html.Div([
                html.H3('Preço de venda (R$/kWh)',
                        style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                dcc.Input(
                    id='preco_venda',
                    type='number', min=0, max=10, step=0.01, value=2.40,
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '6px', 'border': f'1px solid {COR_BORDA}'}
                ),
            ], style={'width': '250px'}),

            html.Div([
                html.H3('Taxa de Software (%)',
                        style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                dcc.Input(
                    id='tx_software',
                    type='number', min=0, max=100, step=0.1, value=7,
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '6px', 'border': f'1px solid {COR_BORDA}'}
                ),
            ], style={'width': '250px'}),

            html.Div([
                html.H3('Custo fixo do Software (R$)',
                        style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                dcc.Input(
                    id='custo_fixo_software',
                    type='number', min=0, max=10000, step=0.1, value=200,
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '6px', 'border': f'1px solid {COR_BORDA}'}
                ),
            ], style={'width': '250px'}),

            html.Div([
                html.H3('Imposto (%)',
                        style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                dcc.Input(
                    id='imposto',          # <- ID corrigido (era duplicado antes)
                    type='number', min=0, max=100, step=0.1, value=15,
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '6px', 'border': f'1px solid {COR_BORDA}'}
                ),
            ], style={'width': '250px'}),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'margin': '0px 100px 24px 100px',
            'flexWrap': 'wrap',
            'gap': '16px'
        }),

        # investimento
        html.Div([
            html.Div(
                html.H2('Investimento',
                        style={'color': COR_SECUNDARIA, 'textAlign': 'center'})
            ),
            html.Div([
                html.Div([
                    html.H3('Investimento carregador (R$)',
                            style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                    dcc.Input(
                        id='valor_investimento',
                        type='number', min=0, max=200000, step=1000, value=90000,
                        style={'width': '100%', 'padding': '8px', 'borderRadius': '6px', 'border': f'1px solid {COR_BORDA}'}
                    ),
                ], style={'width': '350px'}),

                html.Div([
                    html.H3('Material para Instalação (R$)',
                            style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                    dcc.Input(
                        id='valor_material_instalacao',
                        type='number', min=0, max=100000, step=500, value=15000,
                        style={'width': '100%', 'padding': '8px', 'borderRadius': '6px', 'border': f'1px solid {COR_BORDA}'}
                    ),
                ], style={'width': '350px'}),

                html.Div([
                    html.H3('Mão de Obra (R$)',
                            style={'color': COR_SECUNDARIA, 'textAlign': 'center'}),
                    dcc.Input(
                        id='valor_mao_instalacao',
                        type='number', min=0, max=100000, step=500, value=5000,
                        style={'width': '100%', 'padding': '8px', 'borderRadius': '6px', 'border': f'1px solid {COR_BORDA}'}
                    ),
                ], style={'width': '350px'}),
            ], style={
                'display': 'flex',
                'justifyContent': 'space-between',
                'margin': '0px 100px 24px 100px',
                'flexWrap': 'wrap',
                'gap': '16px'
            }),
        ]),

        # cards de resultado
        html.Div([
            html.Div([
                html.P('Receita Bruta / mês',
                       style={'color': COR_TEXTO, 'margin': '0 0 8px 0', 'fontSize': '13px'}),
                html.H2(id='receita_bruta',
                        style={'margin': '0', 'color': COR_PRIMARIA, 'fontSize': '28px'}),
            ], style=estilo_card),

            html.Div([
                html.P('Resultado Operacional / mês',
                       style={'color': COR_TEXTO, 'margin': '0 0 8px 0', 'fontSize': '13px'}),
                html.H2(id='resultado_operacional',
                        style={'margin': '0', 'color': COR_PRIMARIA, 'fontSize': '28px'}),
            ], style=estilo_card),

            html.Div([
                html.P('Lucratividade',
                       style={'color': COR_TEXTO, 'margin': '0 0 8px 0', 'fontSize': '13px'}),
                html.H2(id='lucratividade',
                        style={'margin': '0', 'color': COR_PRIMARIA, 'fontSize': '28px'}),
            ], style=estilo_card),

            html.Div([
                html.P('Payback Estimado',
                       style={'color': COR_TEXTO, 'margin': '0 0 8px 0', 'fontSize': '13px'}),
                html.H2(id='payback_estimado',
                        style={'margin': '0', 'color': COR_DESTAQUE, 'fontSize': '28px'}),
            ], style=estilo_card),
        ], style={
            'display': 'flex',
            'gap': '16px',
            'margin': '0px 100px 24px 100px',
            'flexWrap': 'wrap'
        }),
    ]
)


# callback ---------------------------------------

@app.callback(
    # cards de energia
    Output('energia_dia',             'children'),
    Output('energia_mes',             'children'),
    # cards de resultado
    Output('receita_bruta',           'children'),
    Output('resultado_operacional',   'children'),
    Output('lucratividade',           'children'),
    Output('payback_estimado',        'children'),
    # inputs de operação
    Input('potencia_input',            'value'),
    Input('tempo_operacao_slider',     'value'),
    Input('taxa_ocupacao_slider',      'value'),
    # inputs de custo/venda
    Input('preco_custo',               'value'),
    Input('preco_venda',               'value'),
    Input('tx_software',               'value'),
    Input('custo_fixo_software',       'value'),
    Input('imposto',                   'value'),
    # inputs de investimento
    Input('valor_investimento',        'value'),
    Input('valor_material_instalacao', 'value'),
    Input('valor_mao_instalacao',      'value'),
)
def calcular(
    potencia, tempo_operacao, taxa_ocupacao,
    preco_custo, preco_venda, tx_software, custo_fixo_software, imposto,
    valor_investimento, valor_material_instalacao, valor_mao_instalacao
):
    # Valores padrão para evitar erros se algum campo estiver vazio
    potencia                  = potencia                  or 0
    tempo_operacao            = tempo_operacao            or 0
    taxa_ocupacao             = taxa_ocupacao             or 0
    preco_custo               = preco_custo               or 0
    preco_venda               = preco_venda               or 0
    tx_software               = tx_software               or 0
    custo_fixo_software       = custo_fixo_software       or 0
    imposto                   = imposto                   or 0
    valor_investimento        = valor_investimento        or 0
    valor_material_instalacao = valor_material_instalacao or 0
    valor_mao_instalacao      = valor_mao_instalacao      or 0

    # energia ---------------------------------------
    ocupacao_frac          = taxa_ocupacao / 100
    energia_dia            = potencia * tempo_operacao * ocupacao_frac          
    energia_mes            = energia_dia * 30                                   

    # receitas e custos (mensais) ---------------------------------------
    receita_bruta          = energia_mes * preco_venda                          
    custo_energia          = energia_mes * preco_custo                          
    custo_software_var     = receita_bruta * (tx_software / 100)                
    custo_impostos         = receita_bruta * (imposto / 100)                    
    custo_total            = custo_energia + custo_software_var + custo_fixo_software + custo_impostos

    resultado_operacional  = receita_bruta - custo_total                        

    lucratividade          = (resultado_operacional / receita_bruta * 100) if receita_bruta > 0 else 0 

    # investimento total ---------------------------------------
    investimento_total     = valor_investimento + valor_material_instalacao + valor_mao_instalacao

    # Payback em meses (investimento / resultado operacional mensal)
    if resultado_operacional > 0:
        payback_meses      = investimento_total / resultado_operacional
        #payback_anos       = payback_meses / 12
        payback_txt        = f'{payback_meses:.1f} meses'
    elif resultado_operacional == 0:
        payback_txt        = '∞'
    else:
        payback_txt        = 'Prejuízo'

    #  formatação ---------------------------------------
    def brl(v):
        return f'R$ {v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    return (
        f'{energia_dia:.2f} kWh',
        f'{energia_mes:.2f} kWh',
        brl(receita_bruta),
        brl(resultado_operacional),
        f'{lucratividade:.1f}%',
        payback_txt,
    )


if __name__ == '__main__':
    app.run(debug=True)