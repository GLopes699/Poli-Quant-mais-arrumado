import pandas as pd
import statsmodels.api as stat
import statsmodels.tsa.stattools as ts
#Retorna um CSV com todos os pares cointegrado em um determinado período antes da data inicial inserida pelo usuário (normalmente, o mesmo período de backtest, mas no passado)
#Ou seja, se o usuário deseja fazer um backtest de 2021-12-30 até 2024-12-30, essa função checa entre 2018-12-30 até 2021-12-30 se os pares são cointegrados

def melhores_pares(df_acoes, data_inicial, data_final, periodo):
    j=1
    filtro_data = df_acoes.iloc[data_inicial:data_final+1]
    pares_cointegrados = pd.DataFrame(columns = ['Par', 'Ação 1', 'Ação2','Correlação (Menor = Melhor)', 'Ação analisada'], )
    if data_inicial - periodo > 0:
    #Pega o inverso do périodo selecionado pelo usúario ou o período completo até o ínicio do período definido pelo usúario, para definir se as ações são cointegradas            
        filtro_data_treino = df_acoes.iloc[data_inicial-periodo:data_inicial]
    else:
        filtro_data_treino = df_acoes.iloc[0:data_inicial]
    colunas = filtro_data.columns
    for i, acao1 in enumerate(colunas[:-1]):
        if i != 0:
            for acao2 in colunas[i+1:]:
                resultado1 = stat.OLS(filtro_data_treino[acao1], filtro_data_treino[acao2]).fit()
                resultado2 = stat.OLS(filtro_data_treino[acao2], filtro_data_treino[acao1]).fit()
                c_t1=ts.adfuller(resultado1.resid)
                c_t2=ts.adfuller(resultado2.resid)
                pvalue1 = c_t1[1] 
                pvalue2 = c_t2[1]
                if (c_t1[1]<= 0.01) or (c_t2[1]<= 0.01):
                    if pvalue2 < pvalue1:
                    #Inverte o dataframe e a lista de tickers se o teste inverso for melhor
                        pares_cointegrados.loc[len(pares_cointegrados)] = [j, acao2, acao1, pvalue2, acao1]
                        j+=1
                    else:
                        pares_cointegrados.loc[len(pares_cointegrados)] = [j, acao1, acao2, pvalue1, acao1]
                        j+=1
    pares_cointegrados = pares_cointegrados.sort_values(by=['Correlação (Menor = Melhor)'], ascending=True)
    q = input("Quantos pares você deseja salvar?")
    lista_pares = [[acao1, acao2] for acao1, acao2 in zip(pares_cointegrados['Ação 1'][:q], pares_cointegrados['Ação2'][:q])]
    vontade_de_salvar = input('Deseja salvar os pares cointegrados? (S/N)')
    if vontade_de_salvar == "S":
        pares_cointegrados.to_csv('todos_pares_cointegrados.csv', index=False)
    return lista_pares