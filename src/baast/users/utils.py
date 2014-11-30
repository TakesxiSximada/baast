# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class Sex(Enum):
    unknown = 0
    male = 1
    female = 2
