import numpy as np
#Calcula a volatilidade de um portifólio durante um determinado período (em dias)

def volatilidade_dp(retorno_diario_portifolio, dias):
    dp_portifolio = np.std(retorno_diario_portifolio, ddof=1)
    volatilidade_portifolio = dp_portifolio * np.sqrt(dias)
    return volatilidade_portifolio, dp_portifolio
