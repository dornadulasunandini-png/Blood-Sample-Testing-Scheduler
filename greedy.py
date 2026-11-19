
def greedy_schedule(samples):

    sorted_samples = sorted(
        samples,
        key=lambda sample: (
            sample["weight"] / sample["time"]
        ),
        reverse=True
    )

    completion_time = 0
    total_cost = 0

    schedule = []

    for sample in sorted_samples:

        completion_time += sample["time"]

        cost = sample["weight"] * completion_time

        total_cost += cost

        schedule.append({
            **sample,
            "completion_time": completion_time,
            "weighted_cost": cost
        })

    return {
        "schedule": schedule,
        "total_cost": total_cost,
        "objective_value": total_cost,
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)"
    }
