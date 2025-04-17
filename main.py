# =============================================================================
# # -*- coding: utf-8 -*-
# """
# Created on Sat Apr 12 16:57:02 2025
# 
# @author: teste
# """
# =============================================================================

# AQUI VOCE CHAMA AS FUNCOES
# AQUI VC IMPORTA ELAS DOS OUTROS ARQUIVOS

from backtest_par import backtest_par
from riscos import riscos
from checa_arquivo import checa_arquivo
from checa_pares import checa_pares
from backtest_par import backtest_par
from metricas_portifolio import metricas_portifolio
from riscos import riscos
from tickers import tickers
from periodo import periodo
import numpy as np
import pandas as pd


def main():

    arquivo = input("O arquivo CSV dos preços das ações já foi formatado? (S/N) ")
    df_acoes, df_ibov, nome_acoes_atualizado = checa_arquivo(arquivo)
    
    datai=input("Determine a data inicial (Ano-Mês-Dia):")
    dataf=input("Determine a data final (Ano-Mês-Dia):")
    data_inicial, data_final, dias = periodo(df_acoes,datai,dataf)
    
    quantidade_pares = int((input("Quantos pares você gostaria de analisar? ")))
    lista_tickers = tickers(nome_acoes_atualizado,quantidade_pares)
    
    c_t, lista_tickers, lista_filtro_data = checa_pares(df_acoes, lista_tickers, nome_acoes_atualizado, quantidade_pares, data_inicial, data_final, dias)
    
    retorno_diario_portifolio = np.zeros(data_final - data_inicial + 1)
    
    lista_retorno_diario_par = []
    retorno_diario_ibov = pd.to_numeric(df_ibov['Close'].str.replace('^BVSP', '')).iloc[data_inicial:data_final+1].pct_change().fillna(0)
    
    valor_total = int(input("Quanto se pretende investir, no total, em todos os pares? "))
    
    for p in range (quantidade_pares):
        vontade2 = input("Gostaria de executar uma simulação de Pairs Trading com o par "+lista_tickers[p][0]+", "+lista_tickers[p][1]+", durante o período selecionado? (S/N) ")
        if vontade2 == "S":
            
            retorno_diario_par, valor_total, vontade1 = backtest_par(lista_filtro_data, lista_tickers, data_inicial, data_final, retorno_diario_ibov, c_t, quantidade_pares, valor_total)
            lista_retorno_diario_par.append(retorno_diario_par)
    
    retorno_esperado, retorno_diario_portifolio = metricas_portifolio (lista_retorno_diario_par, retorno_diario_portifolio, quantidade_pares, valor_total, vontade1, retorno_diario_ibov, lista_tickers)
    
    vontade3 = input("Gostaria de saber as variáveis de risco desse portifólio?" "(S/N) ")
    if vontade3 == "S":
        riscos(retorno_esperado, retorno_diario_portifolio, dias, valor_total)
        
        
def main_inteligente(arquivo,datai,dataf,quantidade_pares,valor_total,vontade2,vontade3):
       
        df_acoes, df_ibov, nome_acoes_atualizado = checa_arquivo(arquivo)

        data_inicial, data_final, dias = periodo(df_acoes,datai,dataf)
        
        lista_tickers = tickers(nome_acoes_atualizado,quantidade_pares)
        
        c_t, lista_tickers, lista_filtro_data = checa_pares(df_acoes, lista_tickers, nome_acoes_atualizado, quantidade_pares, data_inicial, data_final, dias)
        
        retorno_diario_portifolio = np.zeros(data_final - data_inicial + 1)
        
        lista_retorno_diario_par = []
        retorno_diario_ibov = pd.to_numeric(df_ibov['Close'].str.replace('^BVSP', '')).iloc[data_inicial:data_final+1].pct_change().fillna(0)
        
                
        for p in range (quantidade_pares):
            
            if vontade2:
                
                retorno_diario_par, valor_total, vontade1 = backtest_par(lista_filtro_data, lista_tickers, data_inicial, data_final, retorno_diario_ibov, c_t, quantidade_pares, valor_total)
                lista_retorno_diario_par.append(retorno_diario_par)
        
        retorno_diario_portifolio, lucro_acumulado_portifolio = metricas_portifolio (lista_retorno_diario_par, retorno_diario_portifolio, quantidade_pares, valor_total, vontade1, retorno_diario_ibov, lista_tickers)
        
        
        if vontade3:
            riscos(retorno_diario_portifolio, lucro_acumulado_portifolio, dias, valor_total)

if __name__ == "__main__":
    arquivo='S'
    datai='2021-12-30'
    dataf='2024-12-30'
    quantidade_pares=1
    valor_total=100000
    roda_backtest= True
    roda_riscos= True
    
    main_inteligente(arquivo,datai,dataf,quantidade_pares,valor_total,roda_backtest,roda_riscos)
    
    
    