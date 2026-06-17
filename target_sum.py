"""Core logic for Target Sum."""
import random

DIFFICULTY_CONFIG = {
    "easy": {"count": 5, "pick": 2, "rounds": 6, "min": 1, "max": 12, "bonus": 1},
    "normal": {"count": 6, "pick": 3, "rounds": 7, "min": 1, "max": 20, "bonus": 2},
    "hard": {"count": 7, "pick": 3, "rounds": 8, "min": -5, "max": 30, "bonus": 3},
}


def config(difficulty):
    return DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["normal"])


def make_puzzle(difficulty, rng=None):
    rng = rng or random
    cfg = config(difficulty)
    numbers = [rng.randint(cfg["min"], cfg["max"]) for _ in range(cfg["count"])]
    solution_indices = sorted(rng.sample(range(cfg["count"]), cfg["pick"]))
    target = sum(numbers[i] for i in solution_indices)
    return {"numbers": numbers, "target": target, "pick": cfg["pick"], "solution": solution_indices}


def parse_indices(text, count):
    parts = text.replace(",", " ").split()
    indices = []
    for part in parts:
        if not part.isdigit():
            return None
        value = int(part)
        if not 1 <= value <= count:
            return None
        idx = value - 1
        if idx in indices:
            return None
        indices.append(idx)
    return indices


def choice_sum(numbers, indices):
    return sum(numbers[i] for i in indices)


def is_correct(puzzle, indices):
    if indices is None or len(indices) != puzzle["pick"]:
        return False
    return choice_sum(puzzle["numbers"], indices) == puzzle["target"]


def hint_text(puzzle):
    return " ".join(str(i + 1) for i in puzzle["solution"][:1])


def numbers_text(numbers):
    return " ".join(f"{idx + 1}:{num}" for idx, num in enumerate(numbers))


def score_for(difficulty, tries_left, used_hint=False, correct=True):
    if not correct:
        return 0
    base = 25 + tries_left * 10
    if used_hint:
        base //= 2
    return base * config(difficulty)["bonus"]


def final_rating(correct, rounds):
    if correct == rounds:
        return "perfect"
    if correct >= max(1, rounds * 2 // 3):
        return "solver"
    if correct >= max(1, rounds // 3):
        return "learner"
    return "lost"
