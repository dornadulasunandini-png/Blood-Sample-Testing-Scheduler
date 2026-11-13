
from sample_data import samples


def dynamic_programming_scheduler(data=None):

    if data is None:
        data = samples

    n = len(data)

    # Calculate total testing time for every subset
    total_time = [0] * (1 << n)

    for mask in range(1, 1 << n):
        bit = mask & -mask
        i = bit.bit_length() - 1
        total_time[mask] = total_time[mask ^ bit] + data[i]["time"]

    # DP table: minimum cost for each subset
    INF = float("inf")
    dp = [INF] * (1 << n)
    parent = [-1] * (1 << n)

    dp[0] = 0

    # Find the best order
    for mask in range(1 << n):

        if dp[mask] == INF:
            continue

        for i in range(n):

            if not (mask & (1 << i)):

                new_mask = mask | (1 << i)

                new_cost = (
                    dp[mask]
                    + data[i]["weight"] * total_time[new_mask]
                )

                if new_cost < dp[new_mask]:
                    dp[new_mask] = new_cost
                    parent[new_mask] = i

    # Reconstruct the best schedule
    mask = (1 << n) - 1
    schedule = []

    while mask:
        i = parent[mask]
        schedule.append(data[i])
        mask ^= (1 << i)

    schedule.reverse()

    # Calculate completion times
    current_time = 0
    details = []

    for sample in schedule:
        current_time += sample["time"]

        cost = current_time * sample["weight"]

        details.append({
            "id": sample["id"],
            "test": sample["test"],
            "urgency": sample["urgency"],
            "time": sample["time"],
            "weight": sample["weight"],
            "completion_time": current_time,
            "cost": cost
        })

    result = {
        "algorithm": "Dynamic Programming",
        "schedule": details,
        "total_cost": dp[(1 << n) - 1],
        "time_complexity": "O(n * 2^n)",
        "space_complexity": "O(2^n)"
    }

    print("\n===== DYNAMIC PROGRAMMING SCHEDULER =====")

    for item in details:
        print(
            item["id"],
            item["test"],
            "| Completion:",
            item["completion_time"],
            "| Cost:",
            item["cost"]
        )

    print("\nMinimum Total Weighted Cost:", result["total_cost"])

    return result


if __name__ == "__main__":
    dynamic_programming_scheduler()
