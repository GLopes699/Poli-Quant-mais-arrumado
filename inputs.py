def inputs():
   
    arquivo = input("O arquivo CSV dos preços das ações já foi formatado? (S/N) ")

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

    return arquivo, datai, dataf, quantidade_pares, valor_total, vontade2, vontade3
        