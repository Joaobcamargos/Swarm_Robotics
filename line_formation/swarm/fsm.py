#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Lógica da Máquina de Estados Finitos (FSM) para formação de fila.
"""

import numpy as np
from swarm.states import RobotStatus
from swarm import config

def _dist(a, b):
    """Calcula a distância euclidiana entre dois pontos."""
    return np.linalg.norm(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))

def _in_left_R0(robot):
    """
    Verdadeiro se o robô estiver dentro de R0 (raio REARRANGING_REGIONS_RADII[0]
    centrado em FENDA_CENTER) e no semiplano esquerdo (x <= GAP_X).
    """
    p = robot.pos
    R0 = config.REARRANGING_REGIONS_RADII[0]
    return (_dist(p, config.FENDA_CENTER) <= R0) and (p[0] <= config.GAP_X)

def _is_left(robot):
    """Semiplano esquerdo em relação à fenda (antes da boca): x <= GAP_X."""
    return robot.pos[0] <= config.GAP_X

def _any_line_active(robots):
    """True se existir qualquer robô em LEADER ou IN_LINE (fila ativa)."""
    return any(r.state in (RobotStatus.LEADER, RobotStatus.IN_LINE) for r in robots)

def update_line_states(robots):
    """
    Executa a lógica da FSM para criar a 'linha indiana' (ignora R1).
    
    Regras:
    - Nunca formar nova fila enquanto houver LEADER/IN_LINE ativos.
    - 1º gatilho: ao primeiro GROUP entrar em R0-esquerda, elege 1 líder.
    - Encadeia IMEDIATAMENTE todos os robôs em GROUP do lado esquerdo.
    """
    if not robots or _any_line_active(robots):
        return

    # Candidatos de gatilho: apenas GROUP em R0-esquerda
    trigger_candidates = [r for r in robots if r.state == RobotStatus.GROUP and _in_left_R0(r)]
    if not trigger_candidates:
        return

    # Elege líder = mais próximo do centro da fenda entre os candidatos de gatilho
    leader = min(trigger_candidates, key=lambda r: _dist(r.pos, config.FENDA_CENTER))
    leader.state = RobotStatus.LEADER
    leader.inline_following_robot = None

    # Bootstrap: TODOS os GROUP no lado esquerdo entram de uma vez (fila instantânea)
    bootstrap_set = [r for r in robots
                     if (r is not leader) and (r.state == RobotStatus.GROUP) and _is_left(r)]

    # Encadeia por proximidade incremental a partir do líder
    current = leader
    remaining = list(bootstrap_set)
    while remaining:
        closest = min(remaining, key=lambda r: _dist(r.pos, current.pos))
        closest.state = RobotStatus.IN_LINE
        closest.inline_following_robot = current
        remaining.remove(closest)
        current = closest

def reset_post_fenda(robots):
    """
    Reset posicional simples: Robôs LEADER/IN_LINE voltam para GROUP
    após cruzar a fenda (x > WALL_XMAX + EPS_RESET).
    """
    x_cut = config.WALL_XMAX + config.EPS_RESET
    for r in robots:
        if r.state in (RobotStatus.LEADER, RobotStatus.IN_LINE) and r.pos[0] > x_cut:
            r.state = RobotStatus.GROUP
            r.inline_following_robot = None