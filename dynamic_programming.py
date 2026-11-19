
def dynamic_programming_schedule(samples):

    n = len(samples)

    total_states = 1 << n

    dp = [float("inf")] * total_states
    parent = [None] * total_states

    dp[0] = 0

    # Dynamic Programming

    for mask in range(total_states):

        elapsed_time = sum(
            samples[i]["time"]
            for i in range(n)
            if mask & (1 << i)
        )

        for j in range(n):

            if not (mask & (1 << j)):

                new_mask = mask | (1 << j)

                new_cost = (
                    dp[mask]
                    + elapsed_time
                    + samples[j]["time"]
                )

                if new_cost < dp[new_mask]:

                    dp[new_mask] = new_cost
                    parent[new_mask] = (mask, j)

    # Reconstruct schedule

    mask = total_states - 1
    best_order = []

    while mask:

        previous_mask, sample_index = parent[mask]

        best_order.append(samples[sample_index])

        mask = previous_mask

    best_order.reverse()

    # Calculate weighted cost

    completion_time = 0
    weighted_total = 0

    schedule = []

    for sample in best_order:

        completion_time += sample["time"]

        cost = sample["weight"] * completion_time

        weighted_total += cost

        schedule.append({
            **sample,
            "completion_time": completion_time,
            "weighted_cost": cost
        })

    return {
        "schedule": schedule,
        "total_cost": weighted_total,
        "objective_value": dp[total_states - 1],
        "time_complexity": "O(n × 2^n)",
        "space_complexity": "O(2^n)"
    }
