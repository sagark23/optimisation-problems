import matplotlib.pyplot as plt
import numpy as np
from leap_ec import context, Individual


def find_best_solution(population: list[Individual], n) -> list[Individual]:
    return sorted(population, key=lambda x: x.fitness)[:n]


class BestFitnessLoggerProbe:
    def __init__(self, total_generations: int, elite_retention_count: int):
        self.total_generations = total_generations
        self.min_fitness_plot_percentage = 0.9
        self.max_fitness_plot_percentile = 98
        self.elite_retention_count = elite_retention_count

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
            context['track'] = {'solutions': [], 'best_entry': {'best_individual_in_gen': default, 'generation': -1}}

        fittest_n = find_best_solution(population, self.elite_retention_count)
        fittest_in_gen = fittest_n[0]
        current_entry = {
            'generation': current_gen_num,
            'best_individual_in_gen': fittest_in_gen,
            'best_individual': context['track']['best_entry']['best_individual_in_gen'],
            'avg_top_n_fitness': sum([x.fitness for x in fittest_n]) / len(fittest_n)
        }
        if fittest_in_gen.fitness < context['track']['best_entry']['best_individual_in_gen'].fitness:
            current_entry['best_individual_in_gen'] = fittest_in_gen
            context['track']['best_entry'] = current_entry
        context['track']['solutions'] = context['track']['solutions'] + [current_entry]

        if self._should_print_best_fitness(current_gen_num):
            print(f'Best fitness from [{current_gen_num}]: {fittest_in_gen.fitness} '
                  f'(avg top n fitness: {current_entry["avg_top_n_fitness"]}) | '
                  f'Best fitness so far[{context["track"]["best_entry"]["generation"]}]: '
                  f'{context["track"]["best_entry"]["best_individual_in_gen"].fitness}')

        if self._should_plot_best_fitness(current_gen_num):
            self.create_plot()

        return population

    def create_plot(self) -> None:
        all_generations = [x['generation'] for x in context['track']['solutions']]
        all_avg_top_n_fitness = [x['avg_top_n_fitness'] for x in context['track']['solutions']]
        all_fittest_of_gen = [x['best_individual_in_gen'].fitness for x in context['track']['solutions']]
        fittest_of_all_time = [x['best_individual'].fitness for x in context['track']['solutions']]
        y_min = min(all_fittest_of_gen) * self.min_fitness_plot_percentage
        y_max = np.percentile(all_fittest_of_gen, self.max_fitness_plot_percentile)

        plt.plot(all_generations, all_avg_top_n_fitness, label='Average Top N Fitness')
        plt.plot(all_generations, all_fittest_of_gen, label='Best Fitness in Gen', alpha=0.8)
        plt.plot(all_generations, fittest_of_all_time, label='Fittest of all time', color='black', alpha=0.5)

        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Fitness over generations')
        plt.gcf().set_size_inches(19.20, 10.80)
        plt.ylim(y_min, y_max)
        plt.legend()
        plt.show()
