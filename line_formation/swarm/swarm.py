"""
Classe Swarm representando um conjunto de robôs.
"""

import numpy as np
from swarm.robot import Robot
from swarm import config, forces


class Swarm:
    """
    Conjunto de robôs que formam o enxame.
    """

    def __init__(self, N=20):
        """
        Inicializa o enxame de robôs.

        Args:
            N (int): Número de robôs.
        """
        np.random.seed(2)
        center0 = np.array([2.0, config.GAP_CENTER_Y])
        ang = 2 * np.pi * np.random.rand(N)
        rad = 1.4 * np.sqrt(np.random.rand(N))
        positions = center0 + np.column_stack([rad * np.cos(ang), rad * np.sin(ang)])
        self.robots = [Robot(pos) for pos in positions]

    def get_positions(self):
        """Retorna as posições de todos os robôs."""
        return np.array([r.pos for r in self.robots])

    def get_velocities(self):
        """Retorna as velocidades de todos os robôs."""
        return np.array([r.vel for r in self.robots])

    def step(self, environment):
        """
        Atualiza o estado de todos os robôs em um passo de simulação.

        Args:
            environment (Environment): Ambiente da simulação.
        """
        Q = self.get_positions()
        V = self.get_velocities()

        F_att = forces.attractive(Q, config.GOAL)
        F_rep_rob = forces.repulsive_from_robots(Q)
        F_rep_wall = forces.repulsive_from_walls(Q, environment.rects)
        F_flock = forces.flocking_forces(Q, V)

        F_total = F_att + F_rep_rob + F_rep_wall + F_flock

        for i, robot in enumerate(self.robots):
            robot.update(F_total[i], config.DT)

