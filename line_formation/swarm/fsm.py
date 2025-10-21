import numpy as np
from swarm.states import RobotStatus
from swarm import config

def _dist(a, b):
    return np.linalg.norm(np.asarray(a) - np.asarray(b))

def elect_leader_and_make_line(robots, goal):
    """
    Se o robô mais próximo do GOAL estiver dentro de R0, elegemos LEADER
    e encadeamos IN_LINE iterativamente (cada um segue o anterior).
    """
    if not robots:
        return
    leader = min(robots, key=lambda r: _dist(r.pos, goal))
    if _dist(leader.pos, goal) < config.REARRANGING_REGIONS_RADII[0]:
        # Define líder
        leader.state = RobotStatus.LEADER
        leader.inline_following_robot = None
        # Demais robôs: formar fila seguindo proximidade ao atual
        remaining = [r for r in robots if r is not leader and r.state != RobotStatus.FINISHED]
        current = leader
        while remaining:
            # vizinho mais próximo do atual
            closest = min(remaining, key=lambda r: _dist(r.pos, current.pos))
            closest.state = RobotStatus.IN_LINE
            closest.inline_following_robot = current
            remaining.remove(closest)
            current = closest

def reset_states_if_in_R1(robots, goal):
    """
    Se qualquer robô entrar na região R1 (menor raio) após o gargalo,
    volte todos que não estejam FINISHED para GROUP (rearranjo pós-fila).
    """
    any_in_R1 = any(_dist(r.pos, goal) < config.REARRANGING_REGIONS_RADII[1] for r in robots)
    if any_in_R1:
        for r in robots:
            if r.state != RobotStatus.FINISHED:
                r.state = RobotStatus.GROUP
                r.inline_following_robot = None