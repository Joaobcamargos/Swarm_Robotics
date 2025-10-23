#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Funções auxiliares de uso geral.
"""

import numpy as np


def clamp(a, lo, hi):
    """Limita um valor dentro de um intervalo [lo, hi]."""
    return max(lo, min(hi, a))


def point_to_rect_vec(p, rect):
    """Calcula o vetor entre um ponto e o retângulo mais próximo."""
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


def point_to_circle_vec(p, circle_center, circle_radius):
    """Calcula o vetor e a distância entre um ponto e um círculo."""
    v = p - circle_center
    d_center = np.linalg.norm(v)
    
    # Evita divisão por zero se o ponto estiver no centro
    if d_center < 1e-9:
        return np.array([1.0, 0.0]), -circle_radius

    d_surface = d_center - circle_radius
    return v, d_surface