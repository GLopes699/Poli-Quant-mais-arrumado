#Calcula o indíce sharpe de um portifólio

def calc_indice_sharpe(lucro_acumulado_portifolio, volatilidade, taxa_zero_risco):
    indice_sharpe = ((lucro_acumulado_portifolio-1)-taxa_zero_risco)/volatilidade
    return indice_sharpe