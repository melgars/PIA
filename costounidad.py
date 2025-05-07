import numpy as np
import matplotlib as plt
from scipy.optimize import minimize_scalar

def costo_por_validar(x):
    return 1000 / x+5

resultado = minimize_scalar(costo_por_validar,bounds=(1,1000),method = 'bounds')

x_opt = resultado.x
costo_opt = resultado.fun

print("cantidad optima por lote: {x_opt:.2f} unidades")
print("costo minimo por unidad: ${costo_opt:.2f}")