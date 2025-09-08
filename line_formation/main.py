"""
Script principal para executar a simulação de formação em linha
com robôs em enxame.
"""

from swarm.simulator import Simulator




def main():
    """
    Inicializa e executa a simulação.
    """
    sim = Simulator()
    sim.run()


if __name__ == "__main__":
    main()

