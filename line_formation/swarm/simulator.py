#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Classe Simulator que executa a simulação do enxame.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

from swarm import config
from swarm.environment import Environment
from swarm.swarm import Swarm
from swarm.states import RobotStatus


class Simulator:
    """
    Controlador da simulação de enxame.
    
    Recebe como entrada:
    N (int): Número de robôs no enxame (default=25).
    """

    def __init__(self, N=25):
        self.env = Environment()
        self.swarm = Swarm(N)

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, config.WORLDX)
        self.ax.set_ylim(0, config.WORLDY)
        self.ax.set_title('Simulação enxame')

        # ambiente
        self.env.draw(self.ax)

        # robôs
        self.robots_patches = [
            Circle(r.pos, config.ROBOT_RADIUS, color=config.COLOR_ROB)
            for r in self.swarm.robots
        ]
        for patch in self.robots_patches:
            self.ax.add_patch(patch)

        # FPS 
        self.ani = FuncAnimation(
            self.fig,
            self.animate,
            frames=500,
            init_func=self.init_anim,
            interval=40,
            blit=True,
            cache_frame_data=False
        )

    def init_anim(self):
        """Função de inicialização da animação."""
        return self.robots_patches

    def animate(self, frame):
        """Atualiza o estado da simulação a cada frame."""
        self.swarm.step(self.env)
        for patch, robot in zip(self.robots_patches, self.swarm.robots):
            patch.center = robot.pos
            # cores por estado
            if robot.state == RobotStatus.LEADER:
                patch.set_color("red")
            elif robot.state == RobotStatus.IN_LINE:
                patch.set_color("green")
            elif robot.state == RobotStatus.FINISHED:
                patch.set_color("black")
            else:
                patch.set_color(config.COLOR_ROB)
        return self.robots_patches

    def run(self):
        """Executa a simulação."""
        plt.legend()
        plt.show()