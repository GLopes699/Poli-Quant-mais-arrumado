import numpy as np
#Calcula o drawdown histórico, máximo (em decimal) e máximo em valores monetários de um portifólio
def calc_drawdown (retorno_diario_portifolio, valor_total_investido, dias):
    lucro_acumulado_max_portifolio = np.maximum.accumulate(np.cumprod(1+retorno_diario_portifolio))
    drawdown_serie = ((np.cumprod(1+retorno_diario_portifolio))-lucro_acumulado_max_portifolio) / lucro_acumulado_max_portifolio
    drawdown_serie_monetario = np.zeros(dias)
    for i in range (dias):
        drawdown_serie_monetario[i] = drawdown_serie[i] * valor_total_investido * lucro_acumulado_max_portifolio[i]
    drawdown_max_abs = np.min(drawdown_serie[1:])
    drawdown_max_index = np.argmin(drawdown_serie[1:])
    retorno_acumulado_maximo_drawdown = lucro_acumulado_max_portifolio[drawdown_max_index]
    drawdown_max_monetario = retorno_acumulado_maximo_drawdown * valor_total_investido * drawdown_max_abs
    
    return drawdown_serie, drawdown_max_abs, drawdown_max_monetario, drawdown_serie_monetario,