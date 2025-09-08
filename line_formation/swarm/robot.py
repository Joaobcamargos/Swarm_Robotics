"""
Classe Robot representando um agente individual no enxame.
"""

import numpy as np
from swarm import config


class Robot:
    """
    Representa um robô individual.
    """

    def __init__(self, pos, vel=None):
        """
        Inicializa um robô.

        Args:
            pos (ndarray): Posição inicial (x, y).
            vel (ndarray, optional): Velocidade inicial (x, y). Default: vetor nulo.
        """
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel if vel is not None else np.zeros(2), dtype=float)

    def update(self, force, dt):
        """
        Atualiza posição e velocidade do robô dado um vetor de força.

        Args:
            force (ndarray): Vetor de força aplicado (2,).
            dt (float): Passo de tempo.
        """
        norm = np.linalg.norm(force)
        if norm > 0:
            self.vel = (force / norm) * np.clip(norm, config.VMIN, config.VMAX)
        self.pos += self.vel * dt
        self.pos[0] = np.clip(self.pos[0], 0, config.WORLDX)
        self.pos[1] = np.clip(self.pos[1], 0, config.WORLDY)

