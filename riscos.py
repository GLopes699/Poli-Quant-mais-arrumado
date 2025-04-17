import matplotlib.pyplot  as plt
import numpy as np
import scipy.stats as sp
from volatilidade_dp import volatilidade_dp
from drawdown import calc_drawdown
from indice_sharpe import calc_indice_sharpe
from var_cvar import var, cvar


def riscos(retorno_diario_portifolio, lucro_acumulado_portifolio, dias, valor_total):
    #Cálculo das métricas de risco: VaR, CVaR, volatilidade, Drawdown e Sharpe Ratio

    volatilidade_portifolio, dp_portifolio = volatilidade_dp(retorno_diario_portifolio, dias)

    percentil = 0.05
    adl=6
    distribution = "normal"
    nVaR = var(dp_portifolio, distribution, percentil, adl)
    nCVaR = -cvar(dp_portifolio, distribution, percentil, adl)
    distribution = "t-distribution"
    tVaR = var(dp_portifolio, distribution, percentil, adl)   
    tCVaR = -cvar(dp_portifolio, distribution, percentil, adl)

    taxa_zero_risco = (((1+0.085)**(1/252))**dias)-1 #Selic anual média entre 2010 e 2024, diarizada e esticada para o período de backtest
    indice_sharpe = calc_indice_sharpe(lucro_acumulado_portifolio, volatilidade_portifolio, taxa_zero_risco)

    drawdown_serie, drawdown_max_abs, drawdown_max_monetario, drawdown_serie_monetario = calc_drawdown(retorno_diario_portifolio, valor_total, dias)

    #Interface do usuário para análise das métricas de risco do portifólio
    print("VaR diário (distriuição normal) do portifólio: "+str(nVaR*100)+"%")
    print("CVaR diário (distribuição normal) portifólio: "+str(nCVaR*100)+"%")
    print("Var diário (distribuição em t) do portifólio: "+str(tVaR*100)+"%")
    print("CVaR diário (distriuição em t) do portifólio: "+str(tCVaR*100)+"%") 
    print("Drawdown máximo, monetário e percentual:",str(drawdown_max_monetario)+" reais e "+str(drawdown_max_abs*100)+"%")
    print("Volatilidade do portifólio:",str(volatilidade_portifolio*100)+"%")
    print("Indíce de Sharpe do portifólio:", indice_sharpe)

    #Gráfico do drawdown do portifólio
    plt.figure(figsize=(10,6))
    plt.plot(drawdown_serie, label='Drawdown')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('Drawdown do Portifólio')
    plt.xlabel('Dias')
    plt.ylabel('Drawdown')
    plt.legend()
    plt.grid(True)
    plt.show()

    #Gráfico do drawdown monetário do portifólio
    plt.figure(figsize=(10,6))
    plt.plot(drawdown_serie_monetario, label='Drawdown')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('Drawdown monetário do Portifólio')
    plt.xlabel('Dias')
    plt.ylabel('Dinheiro')
    plt.legend()
    plt.grid(True)
    plt.show()

    #Gráfico do retorno diário do portifólio
    plt.figure(figsize=(10,6))
    plt.plot(retorno_diario_portifolio, label='Retorno Diário')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('Retorno Diário do Portifólio')
    plt.xlabel('Dias')
    plt.ylabel('Retorno')
    plt.legend()
    plt.grid(True)
    plt.show()