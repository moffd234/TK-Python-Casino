import random


def handle_heads_tails() -> str:
    flip_num: int = random.randint(0, 1)
    return "tails" if flip_num == 0 else "heads"
