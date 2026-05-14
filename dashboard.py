from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__, title='EletroSonic Dashboard')

# dados ---------------------------------------
df = pd.read_csv('df_final_uf')
df_ordem = df.sort_values('qtd_ele_hib', ascending=False)

opcoes_uf = [{'label': 'Todos os estados', 'value': 'Todos os estados'}] + \
            [{'label': uf, 'value': uf} for uf in sorted(df['uf'].unique())]

# KPIs ---------------------------------------
total_eletrico = df['qtd_ele_hib'].sum()
total_frota    = df['qtd_total'].sum()
proporcao_br   = (total_eletrico / total_frota) * 100
estado_lider   = df.sort_values('qtd_ele_hib', ascending=False).iloc[0]['uf']

# cores a serem utilizadas ---------------------------------------
COR_PRIMARIA   = '#00C896'   # verde
COR_SECUNDARIA = '#0A1628'   # azul escuro (fundo)
COR_CARD       = '#0F2040'   # fundo dos cards
COR_TEXTO      = '#8BAFC8'   # texto claro
COR_DESTAQUE   = '#FFD700'   # dourado para destaques
COR_BORDA      = '#1E3A5F'   # azul da borda

# gráfico ---------------------------------------
TEMPLATE_GRAFICO = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=COR_TEXTO, family='Segoe UI, Arial'),
    xaxis=dict(gridcolor='#1E3A5F', showline=False),
    yaxis=dict(gridcolor='#1E3A5F', showline=False),
    margin=dict(l=40, r=20, t=50, b=40),
)

#  estilo do card ---------------------------------------
estilo_card = {
    'backgroundColor': COR_CARD,
    'borderRadius': '12px',
    'padding': '20px',
    'border': f'1px solid #1E3A5F',
    'flex': '1',
    'minWidth': '200px',
    'textAlign': 'center',
}

# layout ---------------------------------------
app.layout = html.Div(
    style={'backgroundColor': COR_SECUNDARIA, 
           'minHeight': '100vh',
           'fontFamily': 'Segoe UI, Arial, sans-serif', 
           'color': COR_TEXTO, 
           'padding': '24px'},
    children=[
    html.Div(

        # cabeçalho
        html.Div([
            html.Div([
                html.H1('⚡ EletroSonic', 
                    style={'margin': '0', 
                           'color': COR_PRIMARIA, 
                           'fontSize': '28px'}
                    ),
                html.P('Frota de Veículos Elétricos e Híbridos no Brasil',
                       style={'margin': '4px 0 0 0', 
                              'color': COR_TEXTO, 
                              'fontSize': '14px'}
                    )
                ]),
            html.Div(
                html.Span('Fonte: Ministério dos Transportes • Frota 2025',
                          style={'color': COR_TEXTO, 
                                 'fontSize': '12px'}
                    )
                ),
        ], style={'display': 'flex', 
                  'justifyContent': 'space-between',
                  'alignItems': 'center', 
                  'marginBottom': '30px',
                  'borderBottom': '2px solid COR_PRIMARIA', 
                  'paddingBottom': '16px'}
        )
    ),

    # métricas
    html.Div([
    # primeiro card
        html.Div([
            html.P('Total de Elétricos + Híbridos', 
               style={'color': COR_TEXTO, 
                      'margin': '0 0 8px 0', 
                      'fontSize': '13px'}
            ),
            html.H2(f'{total_eletrico:,.0f}'.replace(',', '.'), 
                style={'margin': '0', 
                       'color': COR_PRIMARIA, 
                       'fontSize': '28px'}
            ),
            html.P('veículos no Brasil', 
               style={'color': COR_TEXTO, 
                      'margin': '4px 0 0 0', 
                      'fontSize': '12px'}
            ),
        ], style=estilo_card
        ),

    # segundo card
        html.Div([
            html.P('Participação na frota nacional', 
               style={'color': COR_TEXTO, 
                      'margin': '0 0 8px 0', 
                      'fontSize': '13px'}
            ),
            html.H2(f'{proporcao_br:,.2f}%', 
                style={'margin': '0', 
                       'color': '#FFD700', 
                       'fontSize': '28px'}
            ),
            html.P('do total de veículos', 
               style={'color': COR_TEXTO, 
                      'margin': '4px 0 0 0', 
                      'fontSize': '12px'}
            ),
        ], style=estilo_card
        ),

    # terceiro card
        html.Div([
            html.P('Estado com maior frota VERDE', 
               style={'color': COR_TEXTO, 
                      'margin': '0 0 8px 0', 
                      'fontSize': '13px'}
            ),
            html.H2(f'{estado_lider}', 
                style={'margin': '0', 
                       'color': COR_PRIMARIA, 
                       'fontSize': '28px'}
            ),
            html.P('em volume absoluto', 
               style={'color': COR_TEXTO, 
                      'margin': '4px 0 0 0', 
                      'fontSize': '12px'}
            ),
        ], style=estilo_card
        ),

    # quarto card (último)
        html.Div([
            html.P('Estados analisados', 
               style={'color': COR_TEXTO, 
                      'margin': '0 0 8px 0', 
                      'fontSize': '13px'}
            ),
            html.H2(str(len(df)), 
                style={'margin': '0', 
                       'color': COR_PRIMARIA, 
                       'fontSize': '28px'}
            ),
            html.P('unidades federativas', 
               style={'color': COR_TEXTO, 
                      'margin': '4px 0 0 0', 
                      'fontSize': '12px'}
            ),
        ], style=estilo_card
        ),
    ], style={'display': 'flex', 
              'gap': '16px', 
              'marginBottom': '24px', 
              'flexWrap': 'wrap'}
    ),

    # filtros
    # escolher o estado
    html.Div([
        html.Div([
            html.Label('Filtrar por estado:', style={'fontSize': '13px', 
                                                 'color': COR_TEXTO, 
                                                 'marginBottom': '6px', 
                                                 'display': 'block'}),
            dcc.Dropdown(
                    options=opcoes_uf,
                    value='Todos os estados',
                    id='uf_dropdown',
                    clearable=False,
                    style={'backgroundColor': COR_CARD, 
                           'color': COR_TEXTO, 
                           'border': '1px solid #1E3A5F'},
            ),
        ], style={'flex': '1', 'minWidth': '220px'}
        ),
        # visualizar quantidade absoluta ou proporção
        html.Div([
            html.Label('Visualizar por:', style={'fontSize': '13px', 
                                                 'color': COR_TEXTO, 
                                                 'marginBottom': '6px', 
                                                 'display': 'block'}),
            dcc.RadioItems(
                    id='metrica_radio',
                    options=[
                        {'label': ' Quantidade Absoluta', 'value': 'qtd_ele_hib'},
                        {'label': ' Proporção (%)','value': 'proporcao_%'},
                    ],
                    value='qtd_ele_hib',
                    inline=True,
                    inputStyle={'marginRight': '6px', 'accentColor': COR_PRIMARIA},
                    labelStyle={'marginRight': '20px', 'color':COR_TEXTO, 'fontSize': '14px'},
            ),
        ], style={'flex': '2', 
                  'minWidth': '300px', 
                  'display': 'flex', 
                  'flexDirection': 'column', 
                  'justifyContent': 'flex-end'}
        )
    ],style={
            'display': 'flex', 
            'gap': '24px', 
            'flexWrap': 'wrap', 
            'alignItems': 'flex-end',
            'backgroundColor': COR_CARD, 
            'padding': '16px 20px', 
            'borderRadius': '12px',
            'marginBottom': '24px', 
            'border': '1px solid #1E3A5F'}
    ),

# gráficos
    # exibir 2 gráficos lado a lado
    html.Div([
        # gráfico de barras
        html.Div([
            dcc.Graph(id='grafico_barras', 
                      config={'displayModeBar': False}
            ),
            ], style={'flex': '3', 
                      'backgroundColor': COR_CARD, 
                      'borderRadius': '12px',
                      'padding': '16px',
                      'border': '1px solid #1E3A5F'}
        ),

            # top 10 proporção
        html.Div([
            dcc.Graph(id='grafico_proporcao', 
                      config={'displayModeBar': False}
            ),
            ], style={'flex': '2', 
                      'backgroundColor': COR_CARD, 
                      'borderRadius': '12px',
                      'padding': '16px', 
                      'border': '1px solid #1E3A5F'}
        ),
        ], style={'display': 'flex', 
                  'gap': '16px', 
                  'marginBottom': '16px', 
                  'flexWrap': 'wrap'}
        ),

        # gráfico de dispersão
        html.Div([
            dcc.Graph(id='grafico_dispersao', 
                      config={'displayModeBar': False}
            ),
        ], style={'backgroundColor': COR_CARD, 
                  'borderRadius': '12px',
                  'padding': '16px', 
                  'border': '1px solid #1E3A5F'}
        ),

        # rodapé
        html.Div(
            html.P('EletroSonic © 2025 • Análise da frota de carros elétricos no Brasil • Desenvolvido por Laion Beltrão Araújo',
                   style={'color': '#4A6A8A', 
                          'fontSize': '12px', 
                          'textAlign': 'center', 
                          'margin': '0'}
            ),style={'marginTop': '24px', 
                     'paddingTop': '16px', 
                     'borderTop': '1px solid #1E3A5F'}
        )
]
)

# callbacks ---------------------------------------
@app.callback(
    Output('grafico_barras',    'figure'),
    Output('grafico_proporcao', 'figure'),
    Output('grafico_dispersao', 'figure'),
    Input('uf_dropdown',  'value'),
    Input('metrica_radio', 'value'),
)

def atualizar_graficos(uf_selecionada, metrica):
    # filtro ---------------------------------------
    if uf_selecionada == 'Todos os estados':
        df_filtrado = df.copy()
    else:
        df_filtrado = df[df['uf'] == uf_selecionada].copy()

    df_plot = df_filtrado.sort_values(metrica, ascending=False)

    label_metrica = 'Qtd. Elétricos + Híbridos' if metrica == 'qtd_ele_hib' else 'Proporção da Frota (%)'
    formato_hover = ',.0f' if metrica == 'qtd_ele_hib' else '.2f'

    # gráfico de barras ---------------------------------------
    fig_barras = px.bar(
        df_plot, x='uf', y=metrica,
        title=f'{label_metrica} por Estado',
        labels={'uf': 'Estado', metrica: label_metrica},
        color=metrica,
        color_continuous_scale=[[0, '#0A4A3A'], [0.5, '#00A070'], [1, '#00FFB3']],
    )
    fig_barras.update_traces(
        hovertemplate=f'<b>%{{x}}</b><br>{label_metrica}: %{{y:{formato_hover}}}<extra></extra>',
    )
    fig_barras.update_layout(
        **TEMPLATE_GRAFICO,
        coloraxis_showscale=False,
        title_font_size=15,
        showlegend=False,
    )
    fig_barras.update_xaxes(tickangle=-40)

    # top 10 proporção ---------------------------------------
    top10 = df.sort_values('proporcao_%', ascending=True).tail(10)
    fig_prop = px.bar(
        top10, x='proporcao_%', y='uf',
        orientation='h',
        title='Top 10 — Maior Proporção (%)',
        labels={'proporcao_%': 'Proporção (%)', 'uf': ''},
        color='proporcao_%',
        color_continuous_scale=[[0, '#0A4A3A'], [1, COR_DESTAQUE]],
    )
    fig_prop.update_traces(
        hovertemplate='<b>%{y}</b><br>Proporção: %{x:.2f}%<extra></extra>',
    )
    fig_prop.update_layout(
        **TEMPLATE_GRAFICO,
        coloraxis_showscale=False,
        title_font_size=15,
    )

    # gráfico de dispersão ---------------------------------------
    fig_disp = px.scatter(
        df_filtrado,
        x='qtd_total', y='qtd_ele_hib',
        size='qtd_ele_hib',
        color='proporcao_%',
        hover_name='uf',
        title='Frota Total vs. Elétricos+Híbridos por Estado',
        labels={
            'qtd_total':   'Frota Total de Veículos',
            'qtd_ele_hib': 'Qtd. Elétricos + Híbridos',
            'proporcao_%': 'Proporção (%)',
        },
        color_continuous_scale=[[0, '#003D30'], [0.5, COR_PRIMARIA], [1, COR_DESTAQUE]],
        size_max=60,
    )
    fig_disp.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>Frota total: %{x:,.0f}<br>Elét.+Híb.: %{y:,.0f}<extra></extra>',
    )
    fig_disp.update_layout(
        **TEMPLATE_GRAFICO,
        title_font_size=15,
        coloraxis_colorbar=dict(title='Proporção (%)'),
    )

    return fig_barras, fig_prop, fig_disp





if __name__ == '__main__':
    app.run(debug=True)