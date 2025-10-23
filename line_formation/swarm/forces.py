#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Módulo de cálculo das forças de interação entre robôs e ambiente.
"""

import numpy as np
from swarm import config
from swarm.utils import point_to_rect_vec, point_to_circle_vec


def attractive(Q, target):
    """Força atrativa em direção a um alvo."""
    return config.K_ATT * (target - Q)


def repulsive_from_robots(Q):
    """Força repulsiva entre robôs para evitar colisões."""
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
    """Força repulsiva de paredes/obstáculos (com bordas arredondadas)."""
    n = Q.shape[0]
    rep = np.zeros((n, 2))

    # Define quais círculos correspondem a quais retângulos
    wall_circles = {
        config.WALL_BOTTOM: config.CIRCLE_BOTTOM_CENTER,
        config.WALL_TOP: config.CIRCLE_TOP_CENTER
    }

    for i in range(n):
        for rect in rects:
            # Calcula a distância para a parte retangular da parede
            v_rect, d_rect, _ = point_to_rect_vec(Q[i], rect)

            # Calcula a distância para a parte circular da parede
            circle_center = wall_circles[rect]
            v_circ, d_circ = point_to_circle_vec(Q[i], circle_center, config.CIRCLE_RADIUS)

            # Escolhe a parte do obstáculo (reta ou curva) que está mais perto
            if d_rect < d_circ:
                v, d = v_rect, d_rect
            else:
                v, d = v_circ, d_circ

            # Calcula a força de repulsão usando a distância e o vetor do ponto mais próximo
            if d < config.DELTA_WALL and d > 1e-9:
                rep[i] += config.K_REP_WALL * (1.0 / d - 1.0 / config.DELTA_WALL) * (v / (d ** 2))
    return rep


def flocking_forces(Q, V):
    """Forças de coesão, alinhamento e separação (modelo Boids)."""
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