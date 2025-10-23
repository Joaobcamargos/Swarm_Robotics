#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Classe Robot representando um agente individual no enxame.
"""

import numpy as np
from swarm import config
from swarm.states import RobotStatus


class Robot:
    """
    Representa um robô individual.
    
    Recebe como entrada:
    pos (ndarray): Posição inicial (x, y).
    vel (ndarray, optional): Velocidade inicial (x, y). Default: vetor nulo.
    """

    def __init__(self, pos, vel=None):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel if vel is not None else np.zeros(2), dtype=float)

        # Atributos de estado
        self.state = RobotStatus.GROUP
        self.inline_following_robot = None
        self.target_index = 0

    def update(self, force, dt):
        """Atualiza posição e velocidade do robô dado um vetor de força."""
        norm = np.linalg.norm(force)
        if norm < 1e-6:
            self.vel = np.zeros_like(self.vel)  # evita drift
        else:
            desired_speed = min(norm, getattr(config, "VMAX", norm))
            self.vel = (force / norm) * desired_speed

        self.pos += self.vel * dt

        # Clipping nos limites do mundo
        eps = 1e-9
        self.pos[0] = np.clip(self.pos[0], 0.0 + eps, config.WORLDX - eps)
        self.pos[1] = np.clip(self.pos[1], 0.0 + eps, config.WORLDY - eps)