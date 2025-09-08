"""
Funções auxiliares de uso geral.
"""

import numpy as np


def clamp(a, lo, hi):
    """
    Limita um valor dentro de um intervalo [lo, hi].

    Args:
        a (float): Valor a ser limitado.
        lo (float): Valor mínimo permitido.
        hi (float): Valor máximo permitido.

    Returns:
        float: Valor limitado.
    """
    return max(lo, min(hi, a))


def point_to_rect_vec(p, rect):
    """
    Calcula o vetor entre um ponto e o retângulo mais próximo.

    Args:
        p (ndarray): Coordenada do ponto (x, y).
        rect (tuple): Retângulo definido como (xmin, ymin, xmax, ymax).

    Returns:
        tuple:
            - v (ndarray): Vetor do ponto até a borda mais próxima.
            - d (float): Distância até a borda.
            - closest (ndarray): Ponto mais próximo dentro do retângulo.
    """
    xmin, ymin, xmax, ymax = rect
    cx = clamp(p[0], xmin, xmax)
    cy = clamp(p[1], ymin, ymax)
    closest = np.array([cx, cy])
    v = p - closest
    d = np.linalg.norm(v)
    if d == 0.0:
        dx = min(p[0] - xmin, xmax - p[0])
        dy = min(p[1] - ymin, ymax - p[1])
        if dx < dy:
            v = np.array([-1.0, 0.0]) if (p[0] - xmin) < (xmax - p[0]) else np.array([+1.0, 0.0])
        else:
            v = np.array([0.0, -1.0]) if (p[1] - ymin) < (ymax - p[1]) else np.array([0.0, +1.0])
        d = 1e-6
    return v, d, closest

