
from sample_data import samples


def merge(left, right):

    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i]["time"] >= right[j]["time"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def merge_sort(data):

    if len(data) <= 1:
        return data

    middle = len(data) // 2

    left = merge_sort(data[:middle])
    right = merge_sort(data[middle:])

    return merge(left, right)


def divide_conquer_scheduler(data=None):

    if data is None:
        data = samples

    sorted_samples = merge_sort(data.copy())

    completion_time = 0
    details = []

    for sample in sorted_samples:

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

    total_cost = sum(item["cost"] for item in details)

    result = {
        "algorithm": "Divide and Conquer (Longest Time First)",
        "schedule": details,
        "total_cost": total_cost,
        "objective": "Schedule longest testing times first",
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)"
    }

    print("\n===== DIVIDE AND CONQUER =====")

    for item in details:
        print(
            item["id"],
            "| Completion:", item["completion_time"],
            "| Cost:", item["cost"]
        )

    print("Total Weighted Completion Cost:", total_cost)

    return result


if __name__ == "__main__":
    divide_conquer_scheduler()
