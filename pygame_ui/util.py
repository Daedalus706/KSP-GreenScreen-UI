import math


def rotate_vector(x:float, y:float, a:float) -> tuple[float, float]:
    sin = math.sin(a)
    cos = math.cos(a)
    return (
        cos*x - sin*y,
        sin*x + cos*y
    )


def norm(x:float, y:float) -> float:
    return math.sqrt(x*x + y*y)
