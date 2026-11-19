
def merge_sort(samples):

    if len(samples) <= 1:
        return samples

    mid = len(samples) // 2

    left = merge_sort(samples[:mid])
    right = merge_sort(samples[mid:])

    return merge(left, right)


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


def divide_conquer_schedule(samples):

    sorted_samples = merge_sort(samples.copy())

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
