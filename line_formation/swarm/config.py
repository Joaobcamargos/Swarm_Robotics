#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Configurações globais para o ambiente e algoritmos de enxame.
"""

import numpy as np

# ===================== CONFIGURAÇÃO DO AMBIENTE =====================
WORLDX, WORLDY = 12.0, 8.0
DT = 0.04  # Passo de tempo (ajuste fino de dinâmica geral)

# Fenda/paredes (mantendo a geometria original da fenda)
GAP_X = 6.0
GAP_CENTER_Y = 4.0
GAP_HEIGHT = 1.6  # mantido (não vamos "abrir" mais a fenda)
WALL_WIDTH = 1.0
WALL_XMIN = GAP_X - WALL_WIDTH / 2.0
WALL_XMAX = GAP_X + WALL_WIDTH / 2.0
WALL_BOTTOM = (WALL_XMIN, 0.0, WALL_XMAX, GAP_CENTER_Y - GAP_HEIGHT / 2.0)
WALL_TOP    = (WALL_XMIN, GAP_CENTER_Y + GAP_HEIGHT / 2.0, WALL_XMAX, WORLDY)

# Círculos para arredondar as bordas da fenda
CIRCLE_RADIUS        = WALL_WIDTH / 2.0
CIRCLE_BOTTOM_CENTER = np.array([GAP_X, GAP_CENTER_Y - GAP_HEIGHT / 2.0])
CIRCLE_TOP_CENTER    = np.array([GAP_X, GAP_CENTER_Y + GAP_HEIGHT / 2.0])

GOAL         = np.array([10.0, GAP_CENTER_Y])       # alvo final
FENDA_CENTER = np.array([GAP_X, GAP_CENTER_Y])      # centro da fenda (referência visual)

# Linhas imaginárias (R0 visual; R1 ignorado na FSM)
RADII = [2.6, 1.2]
REARRANGING_REGIONS_RADII = [RADII[0], RADII[1]]

# ===================== PARÂMETROS DO ALGORITMO (tuning para menos "aperto") =====================
# Campo atrativo — levemente mais forte para vencer a boca da fenda
K_ATT         = 1.2
K_ATT_INLINE  = 2.5  # igual ao K_ATT para “tracionar” no corredor

# Cinemática — um pouco mais de velocidade máxima ajuda a atravessar
VMAX = 0.6
VMIN = 0.1

# Repulsões
DELTA_ROB  = 0.6
K_REP_ROB  = 0.35

# Parede: menos alcance e menos intensidade para evitar "espremer" na boca
DELTA_WALL = 0.65
K_REP_WALL = 0.25

# Flocking (Boids)
R_NEI = 1.5
R_SEP = 0.5
K_COH = 0.35
K_ALI = 0.30
K_SEP = 0.08
FLOCKING_ANGLE_DEGREES = 360

# Visualização
ROBOT_RADIUS = 0.04
COLOR_ROB = 'tab:blue'

# ===================== PARÂMETROS DA FILA (IN_LINE) =====================
# Espaçamento alvo do seguidor em relação ao predecessor, ao longo do eixo do corredor
D_STAR = 0.45
# Alinhamento leve com a velocidade do predecessor
K_ALIGN_INLINE = 0.25
# Flocking residual para IN_LINE (0.0 desliga; 0.1–0.2 suaviza sem empurrar demais)
ALPHA_INLINE = 0.15
# Histerese espacial simples para o reset pós-fenda (evita flicker no corte)
EPS_RESET = 0.05
# Raio extra para formar a fila INSTANTANEAMENTE no primeiro gatilho (sem append incremental)
R0_BOOTSTRAP_DELTA = 0.6