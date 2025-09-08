"""
Módulo de cálculo das forças de interação entre robôs e ambiente.
"""

import numpy as np
from swarm import config
from swarm.utils import point_to_rect_vec


def attractive(Q, target):
    """
    Força atrativa em direção a um alvo.

    Args:
        Q (ndarray): Posições dos robôs (N x 2).
        target (ndarray): Coordenada do alvo (x, y).

    Returns:
        ndarray: Vetores de força atrativa para cada robô (N x 2).
    """
    return config.K_ATT * (target - Q)


def repulsive_from_robots(Q):
    """
    Força repulsiva entre robôs para evitar colisões.

    Args:
        Q (ndarray): Posições dos robôs (N x 2).

    Returns:
        ndarray: Vetores de força repulsiva para cada robô (N x 2).
    """
    n = Q.shape[0]
    rep = np.zeros((n, 2))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = np.linalg.norm(Q[i] - Q[j])
            if d < config.DELTA_ROB and d > 1e-9:
                rep[i] += config.K_REP_ROB * (1.0 / d - 1.0 / config.DELTA_ROB) * ((Q[i] - Q[j]) / d)
    return rep


def repulsive_from_walls(Q, rects):
    """
    Força repulsiva de paredes/obstáculos.

    Args:
        Q (ndarray): Posições dos robôs (N x 2).
        rects (list): Lista de retângulos representando paredes.

    Returns:
        ndarray: Vetores de força repulsiva (N x 2).
    """
    n = Q.shape[0]
    rep = np.zeros((n, 2))
    for i in range(n):
        for rect in rects:
            v, d, _ = point_to_rect_vec(Q[i], rect)
            if d < config.DELTA_WALL and d > 1e-9:
                rep[i] += config.K_REP_WALL * (1.0 / d - 1.0 / config.DELTA_WALL) * (v / (d ** 2))
    return rep


def flocking_forces(Q, V):
    """
    Forças de coesão, alinhamento e separação (modelo Boids).

    Args:
        Q (ndarray): Posições dos robôs (N x 2).
        V (ndarray): Velocidades dos robôs (N x 2).

    Returns:
        ndarray: Vetores de força de flocking (N x 2).
    """
    n = Q.shape[0]
    F_flock = np.zeros((n, 2))
    for i in range(n):
        neighbors = [j for j in range(n) if i != j and np.linalg.norm(Q[i] - Q[j]) < config.R_NEI]
        if neighbors:
            center = np.mean([Q[j] for j in neighbors], axis=0)
            F_coh = config.K_COH * (center - Q[i])
            avg_velocity = np.mean([V[j] for j in neighbors], axis=0)
            F_ali = config.K_ALI * (avg_velocity - V[i])
            F_flock[i] += F_coh + F_ali
        for j in neighbors:
            d = np.linalg.norm(Q[i] - Q[j])
            if d < config.R_SEP:
                F_flock[i] += config.K_SEP * (Q[i] - Q[j]) / (d ** 2)
    return F_flock

