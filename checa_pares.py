import statsmodels.api as stat
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
import seaborn as sn


def checa_pares(df_acoes, lista_tickers, nome_acoes_atualizado, quantidade_pares, data_inicial, data_final, dias):
    #Checa se as ações dos pares são cointegrados

    c_t1=[]
    c_t2=[]
    c_t=[]
    lista_filtro_data=[]
    for p in range(quantidade_pares):
        acao1 = lista_tickers[p][0]
        acao2 = lista_tickers[p][1]
        #Filtra o CSV das ações para ter somente os valores de um par das ações, durante o período, definidos pelo usúario
        filtro_data = df_acoes.filter(items=lista_tickers[p],axis=1).iloc[data_inicial:data_final+1]
        if data_inicial - dias > 0:
            #Pega o inverso do périodo selecionado pelo usúario ou o período completo até o ínicio do período definido pelo usúario, para definir se as ações são cointegradas
            filtro_data_treino = df_acoes.filter(items=lista_tickers[p],axis=1).iloc[data_inicial-dias:data_inicial]
        else:
            filtro_data_treino = df_acoes.filter(items=lista_tickers[p],axis=1).iloc[0:data_inicial]

        #Usa um teste aumentado de Dickey-Fuller para determinar se as ações eram cointegradas dentro do período de "teste"
        #fonte das próximas 5 linhas: https://blog.quantinsti.com/augmented-dickey-fuller-adf-test-for-a-pairs-trading-strategy/
        adf1 = ts.adfuller(filtro_data_treino[acao1])
        adf2 = ts.adfuller(filtro_data_treino[acao2])
        adf3 = ts.adfuller(filtro_data_treino[acao1] - filtro_data_treino[acao2])
        adf4 = ts.adfuller(filtro_data_treino[acao2] - filtro_data_treino[acao1])
        adf5 = ts.adfuller(filtro_data_treino[acao1] / filtro_data_treino[acao2])
        adf6 = ts.adfuller(filtro_data_treino[acao2] / filtro_data_treino[acao1])
        resultado1 = stat.OLS(filtro_data_treino[acao1], filtro_data_treino[acao2]).fit()
        resultado2 = stat.OLS(filtro_data_treino[acao2], filtro_data_treino[acao1]).fit()
        b1 = resultado1.params[acao2]        
        b2 = resultado2.params[acao1]
        spread1 = filtro_data_treino[acao1] - b1*filtro_data_treino[acao2]
        spread2 = filtro_data_treino[acao2] - b2*filtro_data_treino[acao1]
        c_t1.append(ts.adfuller(resultado1.resid))
        c_t2.append(ts.adfuller(resultado2.resid))
        print("adf " + acao1 + " = " + str(adf1))
        print("adf " + acao2 + " = " + str(adf2))
        print("adf " + acao1 + " - " + acao2 + " = " + str(adf3))
        print("adf " + acao2 + " - " + acao1 + " = " + str(adf4))
        print("adf " + acao1 + " / " + acao2 + " = " + str(adf5))
        print("adf " + acao2 + " / " + acao1 + " = " + str(adf6))
        print("adf regressão linear " + acao1 +" = B*"+acao2 +" = "+ str(c_t1[p]))
        print("adf regressão linear " + acao2 +" = B*"+acao1 +" = "+ str(c_t2[p]))
        plt.figure(figsize=(10, 6))
        plt.plot(filtro_data_treino[acao1], label=acao1, color = "red")
        plt.axhline(filtro_data_treino[acao1].mean(), color='red', linestyle='--')
        plt.title(f'Stock Prices for {acao1}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
        plt.figure(figsize=(10, 6))
        plt.plot(filtro_data_treino[acao2], label=acao2, color = "blue")
        plt.axhline(filtro_data_treino[acao2].mean(), color='blue', linestyle='--')
        plt.title(f'Stock Prices for {acao2}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
        plt.figure(figsize=(10, 6))
        plt.plot(filtro_data_treino[acao1]/filtro_data_treino[acao2], label=acao1)
        plt.axhline((filtro_data_treino[acao1]/filtro_data_treino[acao2]).mean(), color='red', linestyle='--')
        plt.title(f'Ratio {acao1} / {acao2}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
        plt.figure(figsize=(10, 6))
        a = filtro_data_treino[acao1]-filtro_data_treino[acao2] - (filtro_data_treino[acao1]-filtro_data_treino[acao2]).mean()
        plt.plot(a, label=acao2)
        plt.axhline(a.mean(), color='red', linestyle='--')
        plt.title(f'Diferença {acao1} - {acao2}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
        plt.figure(figsize=(10, 6))
        plt.plot(spread1, label=acao1+" - "+str(b1)+"*"+acao2)
        plt.axhline(spread1.mean(), color='red', linestyle='--')
        plt.title(f'spread 1')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
        plt.figure(figsize=(10, 6))
        plt.plot(spread2, label=acao2+" - "+str(b2)+"*"+acao1)
        plt.axhline(spread2.mean(), color='red', linestyle='--')
        plt.title(f'spread 2')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()     
        if ((c_t1[p][0]<= c_t1[p][4]['10%'] and c_t1[p][1]<= 0.01) or (c_t2[p][0]<= c_t2[p][4]['10%'] and c_t2[p][1]<= 0.01)):
            print("O par "+acao1+", "+acao2+" é recomendado para Pairs Trading.")
            if c_t2[p][0] < c_t1[p][0]:
                #Inverte o dataframe e a lista de tickers se o teste inverso for melhor 
                filtro_data = filtro_data[lista_tickers[p][::-1]]
                lista_filtro_data.append(filtro_data)
                lista_tickers[p] = lista_tickers[p][::-1]
                c_t.append(c_t2[p])
            else:
                lista_filtro_data.append(filtro_data)
                c_t.append(c_t1[p])
        else:
            print("O par "+acao1+", "+acao2+" não é recomendado para Pairs Trading.")
            print("Por favor, insira um novo par.")
            e=0
            while e < 2:
                ticker = input("Digite o ticker da empresa "+str(((e%2)+1))+" do novo par "+str((p+1))+" (em CAPS):") + "3.SA"
                if ticker in nome_acoes_atualizado:
                    lista_tickers[p][e] = ticker
                    e+=1
                else:
                    print("Essa empresa não estava na Bolsa durante o período")
                if e == 2:
                    #Calcula se o novo par é cointegrado ou não
                    filtro_data_treino = df_acoes.filter(items=lista_tickers[p],axis=1).iloc[data_inicial-dias:data_inicial] if data_inicial-dias > 0 else df_acoes.filter(items=lista_tickers[p],axis=1).iloc[0:data_inicial]
                    resultado1 = stat.OLS(filtro_data_treino[acao1], filtro_data_treino[acao2]).fit()
                    resultado2 = stat.OLS(filtro_data_treino[acao2], filtro_data_treino[acao1]).fit()
                    c_t1.append(ts.adfuller(resultado1.resid))
                    c_t2.append(ts.adfuller(resultado2.resid))
                    #c_t1[p] = ts.adfuller(resultado1.resid)
                    #c_t2[p] = ts.adfuller(resultado2.resid)
                    if (c_t1[p][0] <= c_t1[p][4]['10%'] and c_t1[p][1] <= 0.1) or (c_t2[p][0] <= c_t2[p][4]['10%'] and c_t2[p][1] <= 0.1):
                        print("O novo par "+acao1+", "+acao2+" é recomendado para Pairs Trading.")
                        if c_t2[p][0] < c_t1[p][0]:
                            filtro_data = filtro_data[lista_tickers[p][::-1]]
                            lista_filtro_data.append(filtro_data)
                            lista_tickers[p] = lista_tickers[p][::-1]
                            c_t.append(c_t2[p])
                        else:
                            lista_filtro_data.append(filtro_data)
                            c_t.append(c_t1[p])
                        break
                    else:
                        print("Este par também não é recomendado. Por favor, insira um novo par.")
                        e=0

    return c_t, lista_tickers, lista_filtro_data