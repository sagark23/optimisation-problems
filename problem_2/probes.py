import matplotlib.pyplot as plt
import numpy as np
from leap_ec import context, Individual

from problem_2.utils import find_best_solution


class BestFitnessLoggerProbe:
    def __init__(self, total_generations: int):
        self.total_generations = total_generations
        self.min_fitness_plot_percentage = 0.9
        self.max_fitness_plot_percentile = 98

    def _is_last_gen(self, current_gen: int):
        return current_gen == self.total_generations - 1

    def _should_print_best_fitness(self, current_gen: int) -> bool:
        return self._is_nth_gen(current_gen, 100)

    def _should_plot_best_fitness(self, current_gen: int) -> bool:
        return self._is_nth_gen(current_gen, 10)

    def _is_nth_gen(self, current_gen, n: int):
        return self.total_generations > n and (
                current_gen % (self.total_generations / n) == 0 or
                self._is_last_gen(current_gen)
        )

    def __call__(self, population: list[Individual]) -> list[Individual]:
        current_gen_num = context['leap']['generation']
        if context.get('track') is None:
            default = Individual(None)
            default.fitness = float('inf')
            context['track'] = {'solutions': [], 'best_entry': {'best_individual': default, 'generation': 0}}

        fittest = find_best_solution(population)
        current_entry = {'generation': current_gen_num, 'best_individual': fittest}
        if fittest.fitness < context['track']['best_entry']['best_individual'].fitness:
            context['track']['best_entry'] = current_entry
        context['track']['solutions'] = context['track']['solutions'] + [current_entry]

        if self._should_print_best_fitness(current_gen_num):
            print(f'Best fitness from [{current_gen_num}]: {fittest.fitness} | Best fitness so far [{context["track"]["best_entry"]["generation"]}]: {context["track"]["best_entry"]["best_individual"].fitness}')

        if self._should_plot_best_fitness(current_gen_num):
            self.create_plot()

        return population

    def create_plot(self) -> None:
        all_fitness_values = [x['best_individual'].fitness for x in context['track']['solutions']]
        y_min = min(all_fitness_values) * self.min_fitness_plot_percentage
        y_max = np.percentile(all_fitness_values, self.max_fitness_plot_percentile)
        plt.plot(
            [x['generation'] for x in context['track']['solutions']],
            all_fitness_values
        )
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Fitness over generations')
        plt.ylim(y_min, y_max)
        plt.show()
