
from itertools import permutations


def brute_force_schedule(samples):

    best_cost = -1
    best_order = []

    permutations_checked = 0

    for order in permutations(samples):

        permutations_checked += 1

        completion_time = 0
        total_cost = 0

        for sample in order:
            completion_time += sample["time"]
            total_cost += sample["weight"] * completion_time

        if total_cost > best_cost:
            best_cost = total_cost
            best_order = list(order)

    schedule = []
    completion_time = 0

    for sample in best_order:

        completion_time += sample["time"]

        schedule.append({
            **sample,
            "completion_time": completion_time,
            "weighted_cost": sample["weight"] * completion_time
        })

    return {
        "schedule": schedule,
        "total_cost": best_cost,
        "objective_value": best_cost,
        "permutations_checked": permutations_checked,
        "time_complexity": "O(n! × n)",
        "space_complexity": "O(n)"
    }
