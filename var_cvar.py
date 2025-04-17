import numpy as np
import scipy.stats as sp
#Calcula o VaR e o CVaR de um portifólio de ações, considerando duas distribuições: normal e t-distribution.
#volatilidade = 0.6
#distribution = "normal"
#percentil = 0.05
def var(dp_portifolio, distribution, percentil, adl):
        if distribution == "normal":
            VaR = sp.norm.ppf(percentil) * dp_portifolio
        elif distribution == "t-distribution": 
            nu = adl
            VaR = np.sqrt((nu-2)/nu) * sp.t.ppf(percentil,nu) * dp_portifolio
        return VaR
#print(var(volatilidade, distribution, percentil, 6))
def cvar(dp_portifolio, distribution, percentil, adl):
    if distribution == "normal":
        CVaR = (sp.norm.pdf(sp.norm.ppf(percentil))/(percentil)) * dp_portifolio
    elif distribution == "t-distribution": 
        nu = adl
        x_anu = sp.t.ppf(percentil, nu)
        CVaR = (sp.t.pdf(x_anu, nu)/(percentil)) * ((nu+(x_anu**2))/(nu-1)) * np.sqrt((nu-2)/nu) * dp_portifolio
    return CVaR