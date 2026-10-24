from dataclasses import dataclass

from model.Constructor import Constructor


@dataclass
class Arco:
    c1: Constructor
    c2: Constructor
    peso: int