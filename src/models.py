from dataclasses import dataclass

@dataclass
class Task:
    name: str
    hardness: str # 'жёсткое', 'твёрдое', 'мягкое'
    C: float
    D: float
    T: float