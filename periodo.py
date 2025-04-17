def periodo (df_acoes, datai,dataf):
    #Pede um período de análise para o usúario

    datas=list(df_acoes.iloc[:,0])
    k=0
    l=0
    lista_datas=[]
    while k < 1 or l < 1:
        errado=False
        if k < 1 and errado==False:
            
            if datai in datas:
                lista_datas.append(datai)
                k+=1
            else:
                errado=True
                print("Essa data não era um dia comercial")
        if l < 1 and errado==False:
            
            if dataf in datas:
                lista_datas.append(dataf)
                l+=1
            else:
                errado==True
                print("Essa data não era um dia comercial")
        if errado == False:
            data_inicial=datas.index(lista_datas[0])
            data_final=datas.index(lista_datas[1])
            dias = data_final - data_inicial
            if dias <= 0:
                print("Você inseriu a data final como a data inicial ou duas datas iguais")
                k=0
                l=0
                lista_datas = []
    return data_inicial, data_final, dias