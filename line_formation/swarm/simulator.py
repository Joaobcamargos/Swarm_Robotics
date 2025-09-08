"""
Classe Simulator que executa a simulação do enxame.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

from swarm import config
from swarm.environment import Environment
from swarm.swarm import Swarm


class Simulator:
    """
    Controlador da simulação de enxame.
    """

    def __init__(self, N=20):
        """
        Inicializa a simulação.

        Args:
            N (int): Número de robôs no enxame.
        """
        self.env = Environment()
        self.swarm = Swarm(N)

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, config.WORLDX)
        self.ax.set_ylim(0, config.WORLDY)
        self.ax.set_title('Swarm com linhas imaginárias (POO modularizado)')

        # ambiente
        self.env.draw(self.ax)

        # robôs
        self.robots_patches = [
            Circle(r.pos, config.ROBOT_RADIUS, color=config.COLOR_ROB)
            for r in self.swarm.robots
        ]
        for patch in self.robots_patches:
            self.ax.add_patch(patch)

        self.ani = FuncAnimation(self.fig, self.animate, frames=500,
                                 init_func=self.init_anim, interval=40, blit=True)

    def init_anim(self):
        """Função de inicialização da animação."""
        return self.robots_patches

    def animate(self, frame):
        """
        Atualiza o estado da simulação a cada frame.

        Args:
            frame (int): Número do frame.
        """
        self.swarm.step(self.env)
        for patch, robot in zip(self.robots_patches, self.swarm.robots):
            patch.center = robot.pos
        return self.robots_patches

    def run(self):
        """Executa a simulação."""
        plt.legend()
        plt.show()

