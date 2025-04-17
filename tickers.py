def tickers(nome_acoes_atualizado, quantidade_pares):
    #Pede quantas ações o usúario deseja analisar e coloca elas em uma lista

    lista_tickers = []
    lista_tickers_temp=[]
    i=0
    j=1
    
    while i < 2*quantidade_pares:
        ticker = input("Por favor, digite o ticker da empresa "+(str((i%2)+1))+" do par "+str(j)+" (em CAPS):") + "3.SA"
        if ticker in nome_acoes_atualizado:
            lista_tickers_temp.append(ticker)
            if i%2 == 1:
                lista_tickers.append(lista_tickers_temp)
                lista_tickers_temp=[]
                j+=1
            i+=1
        else:
            print("Essa empresa não estava na Bolsa durante o período")

    return lista_tickers