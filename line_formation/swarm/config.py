"""
Configurações globais para o ambiente e algoritmos de enxame.
"""

import numpy as np

# ===================== CONFIGURAÇÃO DO AMBIENTE =====================
WORLDX, WORLDY = 12.0, 8.0
DT = 0.08

# Fenda/paredes
GAP_X = 6.0
GAP_CENTER_Y = 4.0
GAP_HEIGHT = 1.0
WALL_WIDTH = 1.0
WALL_XMIN = GAP_X - WALL_WIDTH / 2.0
WALL_XMAX = GAP_X + WALL_WIDTH / 2.0
WALL_BOTTOM = (WALL_XMIN, 0.0, WALL_XMAX, GAP_CENTER_Y - GAP_HEIGHT / 2.0)
WALL_TOP = (WALL_XMIN, GAP_CENTER_Y + GAP_HEIGHT / 2.0, WALL_XMAX, WORLDY)

GOAL = np.array([10.0, GAP_CENTER_Y])
FENDA_CENTER = np.array([GAP_X, GAP_CENTER_Y])

# Linhas imaginárias (R0, R1)
RADII = [2.5, 1.2]

# ===================== PARÂMETROS DO ALGORITMO =====================
K_ATT = 1.2
K_REP_ROB = 0.5
K_REP_WALL = 1.2
DELTA_ROB = 0.6
DELTA_WALL = 1.0

K_COH = 0.08
K_ALI = 0.10
K_SEP = 0.14
R_NEI = 2.2
R_SEP = 0.55

VMAX = 0.25
VMIN = 0.03

ROBOT_RADIUS = 0.10
COLOR_ROB = "#1f77b4"

