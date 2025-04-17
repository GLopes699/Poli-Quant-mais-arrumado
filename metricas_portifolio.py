import numpy as np
import matplotlib.pyplot as plt

def metricas_portifolio (lista_retorno_diario_par, retorno_diario_portifolio, quantidade_pares, valor_total, vontade1, retorno_diario_ibov, lista_tickers):
    #Cálculo das métricas de desempenho do portifólio
    for r in range(quantidade_pares):
        if r == 0:
            retorno_diario_portifolio = lista_retorno_diario_par[r]
        else:
            retorno_diario_portifolio = np.add(lista_retorno_diario_par[r], retorno_diario_portifolio)
        if r >= quantidade_pares-1:
            #Interface do usúario para analise das métricas de desempenho do portifólio
            retorno_esperado = np.mean(retorno_diario_portifolio)
            lucro_acumulado_portifolio = np.prod(1 + retorno_diario_portifolio)
            print("O lucro acumulado do portifólio "+str(lista_tickers)+" foi: "+str((lucro_acumulado_portifolio-1)*100)+"%")
            print("Retorno diário médio do portifólio:",str(retorno_esperado*100)+"%")
            if vontade1 == "N":
                print("Distribuindo igualmente entre os pares "+str(lista_tickers)+" o valor total investido no portifólio, ao final da simulação, você teria: "+str(valor_total*lucro_acumulado_portifolio)+" reais")
            else:
                print("Usando o valor atribuído a cada par, ao final da simulação, você teria: "+str(valor_total*lucro_acumulado_portifolio)+" reais")
            #Gráfico comparando o desempenho do portifólio com o da IBOV
            plt.figure(figsize=(10,6))
            plt.plot(np.append(1,np.cumprod(1 + retorno_diario_portifolio)), label = 'Portifólio')
            plt.plot(np.append(1,np.cumprod(1 + retorno_diario_ibov)), label = 'IBOV')
            plt.legend()
            plt.title('Portfolio vs IBOV')
            plt.xlabel('Dias')
            plt.ylabel('Retorno')
            plt.grid(True)
            plt.show()
    return retorno_diario_portifolio, lucro_acumulado_portifolio