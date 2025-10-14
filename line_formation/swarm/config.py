"""
Configurações globais para o ambiente e algoritmos de enxame.
"""

import numpy as np # Importa a biblioteca NumPy, usada para operações com vetores e matrizes (posições, velocidades, etc.).

# ===================== CONFIGURAÇÃO DO AMBIENTE =====================
WORLDX, WORLDY = 12.0, 8.0 # Define a largura (X) e a altura (Y) do mundo da simulação.
DT = 0.08 # Define o passo de tempo da simulação. Valores menores tornam a simulação mais precisa, porém mais lenta.

# Fenda/paredes
GAP_X = 6.0 # Posição horizontal (eixo X) do centro da fenda. Mudar isso move toda a estrutura da parede para a esquerda ou direita.
GAP_CENTER_Y = 4.0 # Posição vertical (eixo Y) do centro da fenda. Mudar isso move a abertura para cima ou para baixo.
GAP_HEIGHT = 1.6 # Altura da abertura na parede. Aumentar isso torna a passagem mais fácil; diminuir aumenta o congestionamento.
WALL_WIDTH = 1.0 # Espessura da parede. Aumentar isso cria um "corredor" mais longo para os robôs atravessarem.
WALL_XMIN = GAP_X - WALL_WIDTH / 2.0 # Coordenada X inicial da parede (borda esquerda). É calculada automaticamente.
WALL_XMAX = GAP_X + WALL_WIDTH / 2.0 # Coordenada X final da parede (borda direita). É calculada automaticamente.
WALL_BOTTOM = (WALL_XMIN, 0.0, WALL_XMAX, GAP_CENTER_Y - GAP_HEIGHT / 2.0) # Define o retângulo da parte de baixo da parede.
WALL_TOP = (WALL_XMIN, GAP_CENTER_Y + GAP_HEIGHT / 2.0, WALL_XMAX, WORLDY) # Define o retângulo da parte de cima da parede.


# Círculos para arredondar as bordas da fenda
CIRCLE_RADIUS = WALL_WIDTH / 2.0
CIRCLE_BOTTOM_CENTER = np.array([GAP_X, GAP_CENTER_Y - GAP_HEIGHT / 2.0])
CIRCLE_TOP_CENTER = np.array([GAP_X, GAP_CENTER_Y + GAP_HEIGHT / 2.0])

GOAL = np.array([10.0, GAP_CENTER_Y]) # Posição final do alvo que os robôs devem alcançar, localizado após a fenda.
FENDA_CENTER = np.array([GAP_X, GAP_CENTER_Y]) # Coordenada exata do centro da fenda, usada como referência para as regiões da FSM.

# Linhas imaginárias (R0, R1)
RADII = [2.5, 1.2] # Define os raios das regiões da FSM. O primeiro (R₀) ativa a formação de linha, o segundo (R₁) ativa o rearranjo.

# ===================== PARÂMETROS DO ALGORITMO =====================
K_ATT = 1.5 # Constante de ganho da força de atração. Controla quão fortemente os robôs são puxados para o alvo.
K_REP_ROB = 0.65 # Constante de ganho da força de repulsão entre robôs. Controla quão forte eles se repelem.
K_REP_WALL = 0.9 # Constante de ganho da força de repulsão das paredes. Controla quão forte as paredes empurram os robôs.
DELTA_ROB = 0.6 # Distância de influência da repulsão entre robôs. A repulsão começa quando a distância é menor que este valor.
DELTA_WALL = 0.4 # Distância de influência da repulsão das paredes. A repulsão da parede começa quando a distância é menor que este valor.

# Parâmetros do Flocking (Boids)
K_COH = 0.08 # Ganho da força de Coesão. Controla a tendência do robô de se mover para o centro de massa dos seus vizinhos.
K_ALI = 0.10 # Ganho da força de Alinhamento. Controla a tendência do robô de alinhar sua velocidade com a dos seus vizinhos.
K_SEP = 0.14 # Ganho da força de Separação. Controla a tendência do robô de evitar se aproximar demais dos vizinhos imediatos.
R_NEI = 2.2 # Raio de vizinhança. Um robô considera outros dentro desta distância para os cálculos de coesão e alinhamento.
R_SEP = 0.55 # Raio de separação. Um robô ativará a força de separação de vizinhos que estiverem dentro desta distância menor.

# Parâmetros dos Robôs
VMAX = 0.25 # Velocidade máxima que um robô pode atingir.
VMIN = 0.03 # Velocidade mínima. Garante que os robôs não parem completamente, ajudando a evitar que fiquem presos.
ROBOT_RADIUS = 0.10 # Raio do robô, usado para a sua representação visual na simulação.
COLOR_ROB = "#1f77b4" # Cor dos robôs na visualização.