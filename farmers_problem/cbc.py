import multiprocessing

from pulp import COIN_CMD


def get_threads() -> int:
    return max(1, multiprocessing.cpu_count() - 1)


def coin_cmd_solver() -> COIN_CMD:
    return COIN_CMD(
        threads=get_threads(),
        path='cbc',
        presolve=True
    ) 