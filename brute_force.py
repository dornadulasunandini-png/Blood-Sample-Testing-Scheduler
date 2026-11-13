
from itertools import permutations
from sample_data import samples


def brute_force_scheduler(data=None):

    if data is None:
        data = samples

    best_order = None
    minimum_cost = float("inf")
    total_orders = 0

    # Check every possible testing order
    for order in permutations(data):

        total_orders += 1
        completion_time = 0
        total_cost = 0

        for sample in order:
            completion_time += sample["time"]
            total_cost += sample["weight"] * completion_time

        if total_cost < minimum_cost:
            minimum_cost = total_cost
            best_order = order

    # Prepare result
    completion_time = 0
    details = []

    for sample in best_order:
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

    result = {
        "algorithm": "Brute Force",
        "schedule": details,
        "total_cost": minimum_cost,
        "total_orders": total_orders,
        "time_complexity": "O(n! * n)",
        "space_complexity": "O(n)"
    }

    print("\n===== BRUTE FORCE SCHEDULER =====")
    print("Total possible orders:", total_orders)

    for item in details:
        print(
            item["id"], item["test"],
            "| Completion:", item["completion_time"],
            "| Cost:", item["cost"]
        )

    print("\nMinimum Weighted Completion Cost:", minimum_cost)

    return result


if __name__ == "__main__":
    brute_force_scheduler()
