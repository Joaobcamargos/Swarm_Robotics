#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Classe Swarm representando um conjunto de robôs com formação de linha (R1 ignorado).
"""

import numpy as np
from swarm.robot import Robot
from swarm import config, forces
from swarm.states import RobotStatus
from swarm.fsm import update_line_states, reset_post_fenda


class Swarm:
    """
    Conjunto de robôs que formam o enxame.
    
    Recebe como entrada:
    N (int): Número de robôs no enxame (default=25).
    """

    def __init__(self, N=25):
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
        """Realiza um passo da simulação (FSM, Forças, Integração)."""
        Q = self.get_positions()
        V = self.get_velocities()

        # Reset primeiro 
        reset_post_fenda(self.robots)
        # Maquina de estados
        update_line_states(self.robots)

        #  Forças base
        F_rep_rob  = forces.repulsive_from_robots(Q)
        F_rep_wall = forces.repulsive_from_walls(Q, environment.rects)
        F_flock    = forces.flocking_forces(Q, V)

        # direção do corredor (do centro da fenda para o GOAL)
        dir_axis = config.GOAL - config.FENDA_CENTER
        norm_axis = np.linalg.norm(dir_axis)
        t_hat = dir_axis / norm_axis if norm_axis > 1e-9 else np.array([1.0, 0.0])

        # mistura por estado
        F_total = np.zeros_like(Q)
        for i, r in enumerate(self.robots):
            target = config.GOAL
            katt   = config.K_ATT
            alpha  = 1.0
            F_extra = np.zeros(2)

            if r.state == RobotStatus.LEADER:
                alpha  = 0.0
                target = config.GOAL
                katt   = config.K_ATT_INLINE

            elif r.state == RobotStatus.IN_LINE:
                alpha = config.ALPHA_INLINE
                if r.inline_following_robot is not None:
                    front  = r.inline_following_robot
                    target = front.pos + t_hat * config.D_STAR
                    F_extra = config.K_ALIGN_INLINE * (front.vel - V[i])
                else:
                    target = config.GOAL
                katt = config.K_ATT_INLINE

            F_att = katt * (target - Q[i])
            F = F_att + F_extra + F_rep_rob[i] + F_rep_wall[i] + alpha * F_flock[i]
            F_total[i] = F

        # 4) Integra
        for i, r in enumerate(self.robots):
            r.update(F_total[i], config.DT)