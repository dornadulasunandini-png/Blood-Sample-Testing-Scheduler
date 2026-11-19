
from sample_data import samples


def dynamic_programming_scheduler(data=None):

    if data is None:
        data = samples

    n = len(data)

    total_time = [0] * (1 << n)

    for mask in range(1, 1 << n):
        bit = mask & -mask
        i = bit.bit_length() - 1

        total_time[mask] = (
            total_time[mask ^ bit] + data[i]["time"]
        )

    INF = float("inf")

    dp = [INF] * (1 << n)
    parent = [-1] * (1 << n)

    dp[0] = 0

    # Minimize the sum of completion times
    for mask in range(1 << n):

        if dp[mask] == INF:
            continue

        for i in range(n):

            if not (mask & (1 << i)):

                new_mask = mask | (1 << i)

                new_cost = dp[mask] + total_time[new_mask]

                if new_cost < dp[new_mask]:
                    dp[new_mask] = new_cost
                    parent[new_mask] = i

    # Reconstruct the schedule
    mask = (1 << n) - 1
    schedule = []

    while mask:
        i = parent[mask]
        schedule.append(data[i])
        mask ^= (1 << i)

    schedule.reverse()

    completion_time = 0
    details = []

    for sample in schedule:

        completion_time += sample["time"]

        details.append({
            "id": sample["id"],
            "test": sample["test"],
            "urgency": sample["urgency"],
            "time": sample["time"],
            "weight": sample["weight"],
            "completion_time": completion_time,
            "cost": sample["weight"] * completion_time
        })

    weighted_cost = sum(item["cost"] for item in details)

    result = {
        "algorithm": "Dynamic Programming (Minimum Completion Time)",
        "schedule": details,
        "total_cost": weighted_cost,
        "objective_value": dp[(1 << n) - 1],
        "objective": "Minimize the sum of completion times",
        "time_complexity": "O(n * 2^n)",
        "space_complexity": "O(2^n)"
    }

    print("\n===== DYNAMIC PROGRAMMING =====")

    for item in details:
        print(
            item["id"],
            "| Completion:", item["completion_time"],
            "| Weighted Cost:", item["cost"]
        )

    print("Minimum Sum of Completion Times:", dp[(1 << n) - 1])
    print("Weighted Cost for Comparison:", weighted_cost)

    return result


if __name__ == "__main__":
    dynamic_programming_scheduler()
