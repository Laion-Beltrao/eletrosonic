"""
Dashboard — Previsão de Frota Elétrica
"""

from dash import Dash, html, dcc, Input, Output, State, callback, no_update
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# cores ---------------------------------------
FUNDO        = '#060E1A'
FUNDO_CARD   = '#0C1B2E'
FUNDO_INPUT  = '#0F2240'
BORDA        = '#1A3A5C'
VERDE        = '#00E5A0'
AZUL         = '#1E90FF'
LARANJA      = '#FF6B35'
TEXTO        = '#C8DDF0'
TEXTO_DIM    = '#5A7A96'
BRANCO       = '#F0F8FF'

COMBUSTIVEIS_ELETRICOS = [
    'ELETRICO/FONTE EXTERNA', 'GASOLINA/ALCOOL/ELETRICO',
    'GASOLINA/ELETRICO', 'HIBRIDO PLUG-IN', 'DIESEL/ELETRICO',
    'ELETRICO/FONTE INTERNA', 'HIBRIDO', 'ELETRICO',
    'ETANOL/ELETRICO', 'HIBRIDO/GAS NATURAL VEICULAR'
]

NOMES_MESES = ['JAN','FEV','MAR','ABR','MAI','JUN',
               'JUL','AGO','SET','OUT','NOV','DEZ']

# carregando os dados ---------------------------------------
df = pd.read_csv('/Users/laionbeltrao/Desktop/eletro_sonic/eletrosonic/pages/df_dash')

# função de previsão ---------------------------------------
def prever_frota_eletrica(df, uf, municipio, meses_futuros=6):
    uf        = uf.strip().upper()
    municipio = municipio.strip().upper()

    df_filtrado = df[
        (df['uf'] == uf) &
        (df['municipio'] == municipio) &
        (df['combustivel'].isin(COMBUSTIVEIS_ELETRICOS))
    ]

    if df_filtrado.empty:
        return None, f"Nenhum dado elétrico encontrado para '{municipio}' - '{uf}'."

    df_modelo = df_filtrado.groupby('mes')['qtd_veiculos'].sum().reset_index()
    X = df_modelo[['mes']].values
    y = df_modelo['qtd_veiculos'].values

    modelo = LinearRegression()
    modelo.fit(X, y)

    y_pred_hist = modelo.predict(X)
    ss_res = np.sum((y - y_pred_hist) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2  = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    mae = float(np.mean(np.abs(y - y_pred_hist)))

    ultimo_mes   = int(df_modelo['mes'].max())
    meses_proj   = np.arange(ultimo_mes + 1, ultimo_mes + meses_futuros + 1).reshape(-1, 1)
    valores_proj = np.maximum(modelo.predict(meses_proj), 0).astype(int)

    return {
        'municipio'     : municipio,
        'uf'            : uf,
        'r2'            : r2,
        'mae'           : mae,
        'coef'          : float(modelo.coef_[0]),
        'x_hist'        : X.flatten().tolist(),
        'y_hist'        : y.tolist(),
        'y_pred_hist'   : y_pred_hist.tolist(),
        'x_proj'        : meses_proj.flatten().tolist(),
        'y_proj'        : valores_proj.tolist(),
        'ultimo_mes'    : ultimo_mes,
        'projecao'      : dict(zip(meses_proj.flatten().tolist(), valores_proj.tolist()))
    }, None


# app ---------------------------------------
app = Dash(__name__, title='Frota Elétrica — Previsão')

ufs_disponiveis = sorted(df['uf'].dropna().unique().tolist())

estilo_input = {
    'backgroundColor': FUNDO_INPUT,
    'border': f'1px solid {BORDA}',
    'borderRadius': '8px',
    'color': BRANCO,
    'padding': '10px 14px',
    'fontSize': '14px',
    'width': '100%',
    'outline': 'none',
    'fontFamily': "'IBM Plex Mono', monospace",
}

estilo_label = {
    'color': TEXTO_DIM,
    'fontSize': '11px',
    'letterSpacing': '2px',
    'textTransform': 'uppercase',
    'marginBottom': '6px',
    'display': 'block',
    'fontFamily': "'IBM Plex Mono', monospace",
}

estilo_card_kpi = {
    'backgroundColor': FUNDO_CARD,
    'border': f'1px solid {BORDA}',
    'borderRadius': '12px',
    'padding': '20px 24px',
    'flex': '1',
    'minWidth': '160px',
}

# layout ---------------------------------------
app.layout = html.Div(
    style={
        'backgroundColor': FUNDO,
        'minHeight': '100vh',
        'fontFamily': "'IBM Plex Mono', 'Courier New', monospace",
        'color': TEXTO,
        'padding': '32px 40px',
    },
    children=[

        # cabeçalho ---------------------------------------
        html.Div([
            html.Div('⚡', style={'fontSize': '36px', 'lineHeight': '1'}),
            html.Div([
                html.H1('FROTA ELÉTRICA',
                        style={'margin': '0', 
                               'fontSize': '22px',
                               'color': VERDE, 
                               'letterSpacing': '4px',
                               'fontWeight': '700'}),
                html.P('SISTEMA DE PREVISÃO E ANÁLISE',
                       style={'margin': '2px 0 0 0', 
                              'fontSize': '10px',
                              'color': TEXTO_DIM, 
                              'letterSpacing': '3px'}),
            ]),
        ], style={'display': 'flex', 
                  'alignItems': 'center', 
                  'gap': '16px',
                  'marginBottom': '32px', 
                  'paddingBottom': '20px',
                  'borderBottom': f'1px solid {BORDA}'}),

        # editaveis ---------------------------------------
        html.Div([
            # uf
            html.Div([
                html.Label('Estado (UF)', style=estilo_label),
                dcc.Dropdown(
                    id='uf_dropdown',
                    options=[{'label': uf, 'value': uf} for uf in ufs_disponiveis],
                    value=ufs_disponiveis[0] if ufs_disponiveis else None,
                    clearable=False,
                    style={'backgroundColor': FUNDO_INPUT, 
                           'color': FUNDO,
                           'border': f'1px solid {BORDA}', 
                           'borderRadius': '8px'},
                ),
            ], style={'flex': '1', 
                      'minWidth': '200px'}),

            # município
            html.Div([
                html.Label('Município', style=estilo_label),
                dcc.Dropdown(
                    id='municipio_dropdown',
                    clearable=False,
                    style={'backgroundColor': FUNDO_INPUT, 
                           'color': FUNDO,
                           'border': f'1px solid {BORDA}', 
                           'borderRadius': '8px'},
                ),
            ], style={'flex': '1', 
                      'minWidth': '200px'}),

            # Meses futuros
            html.Div([
                html.Label('Meses a projetar', style=estilo_label),
                dcc.Slider(
                    id='meses_slider',
                    min=1, max=24, step=1, value=6,
                    marks={i: str(i) for i in [1, 6, 12, 18, 24]},
                    tooltip={'placement': 'bottom', 
                             'always_visible': True},
                ),
            ], style={'flex': '2', 
                      'minWidth': '260px', 
                      'paddingTop': '4px'}),

            # Botão
            html.Div([
                html.Label('\u00a0', style=estilo_label),
                html.Button(
                    '▶  PROJETAR',
                    id='btn_projetar',
                    n_clicks=0,
                    style={
                        'backgroundColor': VERDE,
                        'color': FUNDO,
                        'border': 'none',
                        'borderRadius': '8px',
                        'padding': '11px 28px',
                        'fontSize': '13px',
                        'fontWeight': '700',
                        'letterSpacing': '2px',
                        'cursor': 'pointer',
                        'fontFamily': "'IBM Plex Mono', monospace",
                        'width': '100%',
                    },
                ),
            ], style={'flex': '0 0 160px'}),
        ], style={
            'display': 'flex', 
            'gap': '24px', 
            'flexWrap': 'wrap',
            'alignItems': 'flex-end',
            'backgroundColor': FUNDO_CARD,
            'border': f'1px solid {BORDA}',
            'borderRadius': '14px',
            'padding': '24px',
            'marginBottom': '28px',
        }),

        # mensagem de erro ---------------------------------------
        html.Div(id='msg_erro', style={'color': LARANJA, 
                                       'fontSize': '13px',
                                        'marginBottom': '16px', 
                                        'minHeight': '20px'}),

        # KPIs ---------------------------------------
        html.Div(id='kpi_row', style={
            'display': 'flex', 
            'gap': '16px', 
            'flexWrap': 'wrap',
            'marginBottom': '28px',
        }),

        # gráfico principal ---------------------------------------
        html.Div([
            dcc.Graph(id='grafico_serie', config={'displayModeBar': False},
                      style={'height': '450px'})
        ], style={
            'backgroundColor': FUNDO_CARD,
            'border': f'1px solid {BORDA}',
            'borderRadius': '14px',
            'padding': '8px',
            'marginBottom': '28px',
        }),

        # tabela de projeção ---------------------------------------
        html.Div([
            html.P('TABELA DE PROJEÇÃO', style={
                'color': TEXTO_DIM, 
                'fontSize': '10px', 
                'letterSpacing': '3px',
                'margin': '0 0 16px 0'
            }),
            html.Div(id='tabela_projecao'),
        ], style={
            'backgroundColor': FUNDO_CARD,
            'border': f'1px solid {BORDA}',
            'borderRadius': '14px',
            'padding': '24px',
        }),
    ]
)

# callbacks ---------------------------------------
@app.callback(
    Output('municipio_dropdown', 'options'),
    Output('municipio_dropdown', 'value'),
    Input('uf_dropdown', 'value'),
)
def atualizar_municipios(uf):
    if not uf:
        return [], None
    municipios = sorted(df[df['uf'] == uf]['municipio'].dropna().unique().tolist())
    options    = [{'label': m, 'value': m} for m in municipios]
    return options, (municipios[0] if municipios else None)


@app.callback(
    Output('kpi_row',        'children'),
    Output('grafico_serie',  'figure'),
    Output('tabela_projecao','children'),
    Output('msg_erro',       'children'),
    Input('btn_projetar',    'n_clicks'),
    State('uf_dropdown',     'value'),
    State('municipio_dropdown', 'value'),
    State('meses_slider',    'value'),
    prevent_initial_call=False,
)
def atualizar_dashboard(n_clicks, uf, municipio, meses_futuros):
    if not uf or not municipio:
        return [], figura_vazia(), [], ''

    resultado, erro = prever_frota_eletrica(df, uf, municipio, meses_futuros or 6)

    if erro:
        return [], figura_vazia(), [], erro

    # KPIs ---------------------------------------
    crescimento_mes = resultado['coef']
    frota_atual     = resultado['y_hist'][-1] if resultado['y_hist'] else 0
    frota_proj_fim  = resultado['y_proj'][-1]  if resultado['y_proj'] else 0
    variacao_pct    = ((frota_proj_fim - frota_atual) / frota_atual * 100) if frota_atual else 0

    def kpi_card(titulo, valor, cor=VERDE, unidade=''):
        return html.Div([
            html.P(titulo, style={'color': TEXTO_DIM, 'fontSize': '10px',
                                  'letterSpacing': '2px', 'margin': '0 0 8px 0'}),
            html.Div([
                html.Span(valor, style={'color': cor, 'fontSize': '26px',
                                        'fontWeight': '700'}),
                html.Span(unidade, style={'color': TEXTO_DIM, 'fontSize': '12px',
                                          'marginLeft': '4px'}),
            ]),
        ], style=estilo_card_kpi)

    kpis = [
        kpi_card('FROTA ATUAL',      f"{frota_atual:,.0f}",        VERDE,   'veíc.'),
        kpi_card('PROJEÇÃO FINAL',   f"{frota_proj_fim:,.0f}",     AZUL,    'veíc.'),
        kpi_card('CRESCIM. MENSAL',  f"+{crescimento_mes:,.1f}",   VERDE,   'veíc./mês'),
        kpi_card('VARIAÇÃO',         f"{variacao_pct:+.1f}",
                 VERDE if variacao_pct >= 0 else LARANJA, '%'),
        kpi_card('R²',               f"{resultado['r2']:.4f}",     AZUL,    ''),
        kpi_card('MAE',              f"{resultado['mae']:,.1f}",   TEXTO_DIM,'veíc.'),
    ]

    # gráfico ---------------------------------------
    x_hist    = resultado['x_hist']
    y_hist    = resultado['y_hist']
    y_fit     = resultado['y_pred_hist']
    x_proj    = resultado['x_proj']
    y_proj    = resultado['y_proj']
    ult       = resultado['ultimo_mes']

    labels_hist = [NOMES_MESES[(m - 1) % 12] + f'<br>M{m}' for m in x_hist]
    labels_proj = [NOMES_MESES[(m - 1) % 12] + f'<br>M{m}' for m in x_proj]

    fig = go.Figure()

    # histórico real
    fig.add_trace(go.Scatter(
        x=x_hist, y=y_hist, mode='lines+markers',
        name='Histórico real',
        line=dict(color=AZUL, width=2),
        marker=dict(size=6, color=AZUL, symbol='circle'),
        hovertemplate='<b>Mês %{x}</b><br>Real: %{y:,.0f} veíc.<extra></extra>',
    ))

    # linha de fit (histórico)
    fig.add_trace(go.Scatter(
        x=x_hist, y=y_fit, mode='lines',
        name='Tendência (regressão)',
        line=dict(color=VERDE, width=1.5, dash='dot'),
        hoverinfo='skip',
    ))

    # projeção
    x_bridge = [x_hist[-1]] + x_proj
    y_bridge = [y_fit[-1]]  + list(y_proj)
    fig.add_trace(go.Scatter(
        x=x_bridge, y=y_bridge, mode='lines+markers',
        name='Projeção',
        line=dict(color=LARANJA, width=2, dash='dash'),
        marker=dict(size=7, color=LARANJA, symbol='diamond'),
        hovertemplate='<b>Mês %{x} (proj.)</b><br>%{y:,.0f} veíc.<extra></extra>',
    ))

    # linha vertical separando histórico / projeção
    fig.add_vline(
        x=ult + 0.5, line_width=1, line_dash='dot',
        line_color=TEXTO_DIM,
        annotation_text='início da<br>projeção',
        annotation_font_color=TEXTO_DIM,
        annotation_font_size=10,
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXTO, family="'IBM Plex Mono', monospace"),
        title=dict(
            text=f'Frota Elétrica — {municipio} · {uf}',
            font=dict(color=BRANCO, size=15),
            x=0.02,
        ),
        xaxis=dict(
            gridcolor=BORDA, zerolinecolor=BORDA,
            tickfont=dict(size=10), tickvals=x_hist + x_proj,
            ticktext=[NOMES_MESES[(m-1)%12]+f' M{m}' for m in x_hist + x_proj],
            tickangle=-40,
        ),
        yaxis=dict(gridcolor=BORDA, zerolinecolor=BORDA, tickfont=dict(size=11)),
        legend=dict(
            bgcolor='rgba(0,0,0,0)', bordercolor=BORDA, borderwidth=1,
            orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0,
        ),
        margin=dict(l=60, r=20, t=60, b=80),
        hovermode='x unified',
    )

    # ── Tabela de projeção ────────────────────────────────────────────────────
    header_style = {
        'color': TEXTO_DIM, 'fontSize': '10px', 'letterSpacing': '2px',
        'padding': '8px 16px', 'textAlign': 'left',
        'borderBottom': f'1px solid {BORDA}',
    }
    cell_style = {
        'padding': '10px 16px', 'fontSize': '13px',
        'borderBottom': f'1px solid {BORDA}',
    }

    linhas_tabela = []
    for i, (mes_num, qtd) in enumerate(zip(x_proj, y_proj)):
        bg = FUNDO_INPUT if i % 2 == 0 else 'transparent'
        label = NOMES_MESES[(mes_num - 1) % 12]
        var = qtd - frota_atual
        cor_var = VERDE if var >= 0 else LARANJA
        linhas_tabela.append(html.Tr([
            html.Td(f'Mês {mes_num}',       style={**cell_style, 'backgroundColor': bg}),
            html.Td(label,                  style={**cell_style, 'backgroundColor': bg}),
            html.Td(f'{qtd:,}',             style={**cell_style, 'backgroundColor': bg,
                                                   'color': BRANCO, 'fontWeight': '600'}),
            html.Td(f'{var:+,}',            style={**cell_style, 'backgroundColor': bg,
                                                   'color': cor_var}),
        ]))

    tabela = html.Table([
        html.Thead(html.Tr([
            html.Th('MÊS Nº', style=header_style),
            html.Th('MÊS',    style=header_style),
            html.Th('VEÍCULOS PROJETADOS', style=header_style),
            html.Th('Δ vs FROTA ATUAL',    style=header_style),
        ])),
        html.Tbody(linhas_tabela),
    ], style={'width': '100%', 'borderCollapse': 'collapse'})

    return kpis, fig, tabela, ''


def figura_vazia():
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        annotations=[dict(
            text='Selecione um estado e município para visualizar a previsão.',
            x=0.5, y=0.5, xref='paper', yref='paper',
            showarrow=False, font=dict(color=TEXTO_DIM, size=14),
        )],
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)