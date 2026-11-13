
from sample_data import samples


def greedy_scheduler(data=None):

    if data is None:
        data = samples

    # Sort samples by highest priority/time ratio
    sorted_samples = sorted(
        data,
        key=lambda sample: sample["weight"] / sample["time"],
        reverse=True
    )

    completion_time = 0
    details = []

    for sample in sorted_samples:

        completion_time += sample["time"]

        ratio = sample["weight"] / sample["time"]

        details.append({
            "id": sample["id"],
            "test": sample["test"],
            "urgency": sample["urgency"],
            "time": sample["time"],
            "weight": sample["weight"],
            "ratio": round(ratio, 2),
            "completion_time": completion_time,
            "cost": sample["weight"] * completion_time
        })

    total_cost = sum(item["cost"] for item in details)

    result = {
        "algorithm": "Greedy",
        "schedule": details,
        "total_cost": total_cost,
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)"
    }

    print("\n===== GREEDY SCHEDULER =====")

    for item in details:
        print(
            item["id"], item["test"],
            "| Ratio:", item["ratio"],
            "| Completion:", item["completion_time"],
            "| Cost:", item["cost"]
        )

    print("\nMinimum Weighted Completion Cost:", total_cost)

    return result


if __name__ == "__main__":
    greedy_scheduler()
