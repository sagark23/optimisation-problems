import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
from imageio import v2 as imageio
from matplotlib import pyplot as plt
from pulp import LpProblem, LpStatus, value


@dataclass
class ImageItems:
    warehouse_name: str
    x_name: str
    y_name: str
    stage_name: str
    ax: plt.Axes
    line_writer: list[Callable[[], None]]
    feasible_solution_writer: Callable[[], None]

    def create(self, warehouse_upper_bound: int) -> str:
        self._plot_setup(warehouse_upper_bound)
        self.ax.clear()
        for line in self.line_writer:
            line()
        self.feasible_solution_writer()

        with_fs = f"problem_1/outputs/{self.warehouse_name}_{self.x_name}_{self.y_name}/{self.stage_name}.png"
        ImageItems._write(with_fs)

        return with_fs

    def _plot_setup(self, warehouse_upper_bound: int) -> None:
        self.ax.set_xlim(0, warehouse_upper_bound)
        self.ax.set_ylim(0, warehouse_upper_bound)
        self.ax.set_xlabel(self.x_name)
        self.ax.set_ylabel(self.y_name)
        self.ax.set_title(f"Feasible Region Evolution from {self.warehouse_name} to {self.x_name} and {self.y_name}")

    @staticmethod
    def _write(file_name: str):
        plt.legend()
        Path(os.path.dirname(file_name)).mkdir(parents=True, exist_ok=True)
        plt.savefig(file_name)
        print(f"Image created: {file_name}")


def print_box(title: str) -> None:
    print('╭', '─' * (len(title) + 2), '╮', sep='')
    print('│', title, '│')
    print('╰', '─' * (len(title) + 2), '╯', sep='')


def print_solution(problem: LpProblem) -> None:
    print_box('Solution')
    print('Status:', LpStatus[problem.status])
    units_delivered = 0
    for variable in problem.variables():
        if variable.varValue > 0:
            print(variable.name, '=', variable.varValue)
            units_delivered += variable.varValue
    print(f'Total Cost = {value(problem.objective)}')


def create_gif(warehouse_upper_bound: int, x_store_upper_bound: int, y_store_upper_bound: int, warehouse_name: str,
               x_name: str, y_name: str) -> None:
    _, ax = plt.subplots()
    constraint_colors = {
        warehouse_name: "red",
        x_name: "green",
        y_name: "purple"
    }

    def warehouse_line() -> None:
        warehouse_constraint = [[warehouse_upper_bound, 0], [0, warehouse_upper_bound]]
        ax.plot(*warehouse_constraint, color=constraint_colors[warehouse_name], linestyle='-', marker='o',
                label=f"{x_name} + {y_name} ≤ {warehouse_upper_bound}")

    def x_line() -> None:
        s1_constraint = [[x_store_upper_bound, x_store_upper_bound], [0, warehouse_upper_bound]]
        ax.plot(*s1_constraint, color=constraint_colors[x_name], linestyle='-', marker='o',
                label=f"{x_name} ≤ {x_store_upper_bound}")

    def y_line() -> None:
        s2_constraint = [[0, warehouse_upper_bound], [y_store_upper_bound, y_store_upper_bound]]
        ax.plot(*s2_constraint, color=constraint_colors[y_name], linestyle='-', marker='o',
                label=f"{y_name} ≤ {y_store_upper_bound}")

    def warehouse_feasible_region() -> None:
        x = np.linspace(0, 1000, 100)
        ax.fill_between(x, 0, warehouse_upper_bound - x, color='green', alpha=0.5)

    def warehouse_x_feasible_region() -> None:
        x = np.linspace(0, x_store_upper_bound, 100)
        y1 = warehouse_upper_bound - x
        ax.fill_between(x, 0, y1, color='green', alpha=0.5)

    def warehouse_x_y_feasible_region() -> None:
        x = np.linspace(0, x_store_upper_bound, 100)
        y1 = warehouse_upper_bound - x
        y2 = np.full_like(x, y_store_upper_bound)
        ax.fill_between(x, 0, np.minimum(y1, y2), color='green', alpha=0.5)

    items = [
        ImageItems(
            warehouse_name, x_name, y_name, 'warehouse', ax,
            line_writer=[warehouse_line], feasible_solution_writer=warehouse_feasible_region
        ),
        ImageItems(
            warehouse_name, x_name, y_name, 'warehouse_x', ax,
            line_writer=[warehouse_line, x_line], feasible_solution_writer=warehouse_x_feasible_region
        ),
        ImageItems(
            warehouse_name, x_name, y_name, 'warehouse_x_y', ax,
            line_writer=[warehouse_line, x_line, y_line], feasible_solution_writer=warehouse_x_y_feasible_region
        )
    ]

    images = [imageio.imread(item.create(warehouse_upper_bound)) for item in items]
    gif_file_name = f"problem_1/outputs/{warehouse_name}_{x_name}_{y_name}.gif"
    imageio.mimsave(gif_file_name, images, duration=1750, loop=0)
    print(f"GIF created: {gif_file_name}")
