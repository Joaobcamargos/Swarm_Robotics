#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Módulo que define o ambiente da simulação (paredes, alvo, fenda).
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from swarm import config


class Environment:
    """
    Ambiente da simulação contendo paredes, alvo e linhas imaginárias.
    """

    def __init__(self):
        """Inicializa o ambiente com paredes, fenda e alvo."""
        self.rects = [config.WALL_BOTTOM, config.WALL_TOP]

    def draw(self, ax):
        """
        Desenha o ambiente em um eixo do matplotlib.
        
        Recebe como entrada:
        ax (matplotlib.axes.Axes): Eixo onde será desenhado.
        """
        # paredes
        for (xmin, ymin, xmax, ymax) in self.rects:
            ax.add_patch(Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   color='gray', alpha=0.6))

        # linhas imaginárias (R0 e R1 apenas visuais)
        for i, R in enumerate(config.RADII):
            color = 'orange' if i == 0 else 'green'
            ax.add_patch(Circle(config.FENDA_CENTER, R, fill=False, linestyle='--',
                                linewidth=1.0, edgecolor=color, alpha=0.7))

        # alvo
        ax.plot(config.GOAL[0], config.GOAL[1], marker='*', markersize=15,
                color='purple', label='Alvo')

        # Círculos para dar o efeito de borda arredondada
        ax.add_patch(Circle(config.CIRCLE_BOTTOM_CENTER, config.CIRCLE_RADIUS,
                           color='gray', alpha=0.6))
        ax.add_patch(Circle(config.CIRCLE_TOP_CENTER, config.CIRCLE_RADIUS,
                           color='gray', alpha=0.6))

        # Indicador visual de reset pós-fenda (mini-círculo, apenas visual)
        reset_center = (config.WALL_XMAX - 0.15, config.GAP_CENTER_Y)
        reset_radius = 0.22
        ax.add_patch(Circle(reset_center, reset_radius, fill=False,
                            linestyle=':', linewidth=1.2, edgecolor='cyan', alpha=0.85))