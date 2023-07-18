"""
Compare the performance of algorithms for fair course allocation.

To run this file, you need
    pip install experiments_csv

Programmer: Erel Segal-Halevi
Since: 2023-07
"""
import fairpy.courses as crs
from typing import *
import numpy as np

agent_capacity_bounds =  [6,6]
item_capacity_bounds = [40,40]
max_value = 1000
normalized_sum_of_values = 1000


def course_allocation_with_random_instance(
    num_of_agents:int, num_of_items:int, 
    value_noise_ratio:float,
    algorithm:Callable,
    random_seed: int,):
    np.random.seed(random_seed)
    instance = crs.Instance.random(
        num_of_agents=num_of_agents, num_of_items=num_of_items, normalized_sum_of_values=normalized_sum_of_values,
        agent_capacity_bounds=agent_capacity_bounds, 
        item_capacity_bounds=item_capacity_bounds, 
        item_base_value_bounds=[1,max_value],
        item_subjective_ratio_bounds=[1-value_noise_ratio, 1+value_noise_ratio]
        )
    allocation = algorithm(instance)
    matrix = crs.AgentBundleValueMatrix(instance, allocation)
    matrix.use_normalized_values()
    return {
        "utilitarian_value": matrix.utilitarian_value(),
        "egalitarian_value": matrix.egalitarian_value(),
        "max_envy": matrix.max_envy(),
        "mean_envy": matrix.mean_envy(),
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "course_allocation_biased.csv", backup_folder="results/backup/")

    TIME_LIMIT = 100
    input_ranges = {
        "num_of_agents": [100,200,300],
        "num_of_items":  [10,20,30],
        "value_noise_ratio": [0, 0.1, 0.3, 0.5, 0.7, 1],
        "algorithm": [
            crs.utilitarian_matching, 
            crs.iterated_maximum_matching, 
            crs.serial_dictatorship, 
            # crs.course_allocation_by_proxy_auction,   # Very bad performance
            crs.round_robin, 
            crs.bidirectional_round_robin
            ],
        "random_seed": range(5),
    }
    experiment.run_with_time_limit(course_allocation_with_random_instance, input_ranges, time_limit=TIME_LIMIT)
