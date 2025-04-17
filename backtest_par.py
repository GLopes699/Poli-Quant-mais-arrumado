import pandas as pd
import numpy as np
import scipy.optimize as spop
import statsmodels.api as stat
import matplotlib.pyplot as plt


def backtest_par(lista_filtro_data, lista_tickers, data_inicial, data_final, retorno_diario_ibov, c_t, quantidade_pares,valor_total):
    #Faz o backtest de cada par
    valores_acoes = pd.DataFrame()
    retorno = pd.DataFrame()
    lista_valor_pares = []

    for p in range (quantidade_pares):
        if quantidade_pares > 1 and p == 0:
            vontade1 = input("Gostaria de definir a divisão desse valor entre os pares? Se não quiser, o valor total investido no portifólio será distribuido igualmente entre todos os pares (S/N) ")
        elif quantidade_pares == 1:
            vontade1 = "N"

        if vontade1 == "S":
            #Define, caso o usúario deseje, pesos, os quais escalonam os resultados de cada par.
            for i in range (quantidade_pares):
                valor_par = (int(input("Qual valor será investido no par "+str(lista_tickers[p])+"?: ")))
                lista_valor_pares.append(valor_par)
            soma_valor_par = sum(lista_valor_pares)
            while soma_valor_par != valor_total:
                ajuste = input("A soma dos valores não bate com o valor total. Deseja ajustar o valor de algum par? Se não quiser, o valor total investido será alterado para igualar a soma dos valores investidos em cada par (S/N): ").strip().upper()
                if ajuste == "S":
                    print("\nLista de pares e seus respectivos investimentos:")
                    for indice, par in enumerate(lista_tickers):
                        print(f"{indice + 1} - Par: {par} - Investimento: {lista_valor_pares[indice]} reais - Correlação: {c_t[indice][0]}")
                    try:
                        indice_input = int(input("Digite o número do par que deseja alterar: "))
                        if 1 <= indice_input <= quantidade_pares:
                            novo_valor = int(input(f"Digite o novo valor para o par {lista_tickers[indice-1]}: "))
                            lista_valor_pares[indice - 1] = novo_valor
                            soma_investimento = sum(lista_valor_pares)
                        else:
                            print("Índice inválido. Tente novamente.")
                    except Exception as e:
                        print("Entrada inválida. Tente novamente.")
                elif ajuste == "N":
                    valor_total = soma_investimento
                    break
            if soma_investimento == valor_total:
                print("\nOs investimentos foram ajustados corretamente!")
            else:
                print("\nOs investimentos não coincidiam, então o valor total foi ajustado para:", valor_total)    

        elif vontade1 == "N":
            #Caso o usúario não queria definir esses pesos, divide o valor do investimento simulado igualmente entre os pares
            valor_par = valor_total/quantidade_pares
            lista_valor_pares.append(valor_par)

        for j in range(2):
            #Coloca o valor das ações que fazem parte de um determinado par em um novo dataframe e calcula o retorno diário dessas mesmas ações
            acao = lista_filtro_data[p][lista_tickers[p][j]]
            valores_acoes[lista_tickers[p][j]] = acao
            retorno.loc[data_inicial, lista_tickers[p][j]] = 0
            for data_temp in range(data_inicial+1, data_final):
                retorno.loc[data_temp, lista_tickers[p][j]] = valores_acoes[lista_tickers[p][j]].loc[data_temp+1] / valores_acoes[lista_tickers[p][j]].loc[data_temp] -1

        #fonte das próximas linhas:https://www.youtube.com/watch?v=jvZ0vuC9oJk
        lucros=np.array([])
        #Mudar o t_limite altera a "rigidez" da simulação (quão fácil é para o algoritmo entender que uma ação está valorizada ou desvalorizada em relação à outra e se isso é suficiente para determinar que deve haver uma trade)
        t_limite = c_t[p][4]["10%"]
        retorno_diario_par = np.zeros(data_final - data_inicial + 1)
        for d in range (data_inicial, data_final+1):
            if d != data_final:
                #Determina um "b" afim de minimizar a razão entre os valores das ações, determinando assim um preço "real" que a ação 2 deveria ter.
                def unit_root (b): #ação2 = a + b*ação1
                    a = np.average(valores_acoes[lista_tickers[p][1]][d-data_inicial:d] - b*valores_acoes[lista_tickers[p][0]][d-data_inicial:d])
                    valor_real = a + b*valores_acoes[lista_tickers[p][0]][d-data_inicial:d]
                    diferenca = np.array(valor_real - valores_acoes[lista_tickers[p][1]][d-data_inicial:d])
                    diferenca_da_diferenca = diferenca[1:] - diferenca[:-1]
                    resultado = stat.OLS(diferenca_da_diferenca, diferenca[:-1]).fit()
                    return resultado.params[0]/resultado.bse[0]
                resultado_otimizado = spop.minimize(unit_root, valores_acoes[lista_tickers[p][1]][d]/valores_acoes[lista_tickers[p][0]][d], method="Nelder-Mead")
                t_otimizado = resultado_otimizado.fun   
                b_otimizado = float(resultado_otimizado.x)
                a_otimizado = np.average(valores_acoes[lista_tickers[p][1]][d-data_inicial:d] - b_otimizado*valores_acoes[lista_tickers[p][0]][d-data_inicial:d])
                valor_real = a_otimizado + b_otimizado*valores_acoes[lista_tickers[p][0]][d]
            else:
                t_otimizado = 0
            if t_otimizado > t_limite:
                #Define se deve ou não ter trade no dia
                lucro = 0
            else:
                #Determina qual trade deve ser feita no dia, se baseando no fato da ação 2 estar abaixo ou acima do preço real (Short quando está acima e Long quando está abaixo)
                sinal_de_troca = np.sign(valor_real - valores_acoes[lista_tickers[p][1]][d])
                lucro = sinal_de_troca*retorno[lista_tickers[p][1]][d] - sinal_de_troca*retorno[lista_tickers[p][0]][d]
            lucros = np.append(lucros, lucro)
            retorno_diario_par[d - data_inicial] = lucro*lista_valor_pares[p]/valor_total


            #Interface do usúario para analise das métricas de desempenho de um par
            print("Dia:",d-data_inicial)
            if sinal_de_troca == 0:
                print("Não houve trade hoje.")
            elif sinal_de_troca == 1:
                print("Long em "+lista_tickers[p][1]+" e short em "+lista_tickers[p][0])
            else:
                print("Long em "+lista_tickers[p][0]+" e short em "+lista_tickers[p][1])
            print("Retorno do par no dia: "+str(lucro*100)+"%.")
            print("Retorno desse par desde o início da simulação: "+str((np.prod(1+lucros)*100)-100)+"%.")
            print("Dinheiro ganho por esse par desde o início da simulação: "+str(((np.prod(1+lucros)-1)*lista_valor_pares[p]))+" reais.")
            print("Dinheiro atualmente investido no par: "+str(np.prod(1+lucros)*lista_valor_pares[p])+" reais.")
        #Gráfico comparando o desempenho do algoritmo para um determinado par com o da IBOV"
        plt.figure(figsize=(10,6))
        plt.plot(np.append(1,np.cumprod(1 + lucros)), label = 'Par '+str((p+1)))
        plt.plot(np.append(1,np.cumprod(1 + retorno_diario_ibov.values)), label = 'IBOV')
        plt.legend()
        plt.title(f'Par {p+1} vs IBOV')
        plt.xlabel('Dias')
        plt.ylabel('Retorno')
        plt.grid(True)
        plt.show()
    return retorno_diario_par, valor_total, vontade1