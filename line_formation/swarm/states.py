#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Definição dos estados possíveis para um robô (FSM).
"""

from enum import Enum, auto

class RobotStatus(Enum):
    """Enumeração dos estados do robô."""
    GROUP = auto()
    LEADER = auto()
    IN_LINE = auto()
    FINISHED = auto()