#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Script principal para executar a simulação de formação em linha
com robôs em enxame.
"""

from swarm.simulator import Simulator


def main():
    """Inicializa e executa a simulação."""
    sim = Simulator()
    sim.run()


if __name__ == "__main__":
    main()