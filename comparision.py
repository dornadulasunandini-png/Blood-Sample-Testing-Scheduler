
# ALGORITHM COMPARISON
# Smart Blood Sample Testing Scheduler

from itertools import permutations
from time import perf_counter

from sample_data import samples
from divide_conquer import merge_sort


# Calculate weighted completion cost
def calculate_cost(order):

    completion_time = 0
    total_cost = 0

    for sample in order:

        completion_time += sample["time"]

        total_cost += (
            sample["weight"] * completion_time
        )

    return total_cost


# 1. BRUTE FORCE
def brute_force():

    best_order = None
    minimum_cost = float("inf")

    for order in permutations(samples):

        cost = calculate_cost(order)

        if cost < minimum_cost:

            minimum_cost = cost
            best_order = order

    return best_order, minimum_cost


# 2. DIVIDE AND CONQUER
def divide_conquer():

    order = merge_sort(samples.copy())

    cost = calculate_cost(order)

    return order, cost


# 3. GREEDY
def greedy():

    order = sorted(
        samples,
        key=lambda s: s["weight"] / s["time"],
        reverse=True
    )

    cost = calculate_cost(order)

    return order, cost


# 4. DYNAMIC PROGRAMMING
def dynamic_programming():

    capacity = 10
    n = len(samples)

    dp = [
        [0] * (capacity + 1)
        for _ in range(n + 1)
    ]

    for i in range(1, n + 1):

        sample = samples[i - 1]

        time = sample["time"]
        weight = sample["weight"]

        for c in range(capacity + 1):

            dp[i][c] = dp[i - 1][c]

            if time <= c:

                include = (
                    weight + dp[i - 1][c - time]
                )

                dp[i][c] = max(
                    dp[i][c],
                    include
                )

    # Recover selected samples
    selected = []
    remaining = capacity

    for i in range(n, 0, -1):

        if dp[i][remaining] != dp[i - 1][remaining]:

            sample = samples[i - 1]

            selected.append(sample)

            remaining -= sample["time"]

    selected.reverse()

    return selected, dp[n][capacity]


# Measure execution time
def measure(function):

    start = perf_counter()

    result = function()

    end = perf_counter()

    execution_time = (end - start) * 1000

    return result, execution_time


# MAIN COMPARISON
def compare_algorithms():

    print("\n")
    print("=" * 75)
    print("       SMART BLOOD SAMPLE SCHEDULER")
    print("          ALGORITHM COMPARISON")
    print("=" * 75)

    results = []

    # Run Brute Force
    (bf_order, bf_cost), bf_time = measure(brute_force)

    results.append(
        ("Brute Force", "O(n x n!)", bf_cost, bf_time)
    )

    # Run Divide and Conquer
    (dc_order, dc_cost), dc_time = measure(divide_conquer)

    results.append(
        ("Divide and Conquer", "O(n log n)", dc_cost, dc_time)
    )

    # Run Greedy
    (g_order, g_cost), g_time = measure(greedy)

    results.append(
        ("Greedy", "O(n log n)", g_cost, g_time)
    )

    # Run Dynamic Programming
    (dp_order, dp_value), dp_time = measure(dynamic_programming)

    results.append(
        ("Dynamic Programming", "O(n x B)", dp_value, dp_time)
    )

    # Display results
    print("\nPERFORMANCE RESULTS")
    print("-" * 75)

    print(
        f"{'Algorithm':<23}"
        f"{'Complexity':<17}"
        f"{'Result':<12}"
        f"{'Time (ms)':<12}"
    )

    print("-" * 75)

    for name, complexity, result, execution in results:

        print(
            f"{name:<23}"
            f"{complexity:<17}"
            f"{result:<12}"
            f"{execution:<12.4f}"
        )

    print("-" * 75)

    print("\nRESULT EXPLANATION")

    print("Brute Force cost:", bf_cost)
    print("Divide and Conquer cost:", dc_cost)
    print("Greedy cost:", g_cost)

    print("Dynamic Programming maximum priority:", dp_value)

    print("\nDynamic Programming selected samples:")

    for sample in dp_order:

        print(
            sample["id"],
            "-",
            sample["test"]
        )

    print("\nCONCLUSION")

    if bf_cost == dc_cost == g_cost:

        print(
            "Brute Force, Divide and Conquer, "
            "and Greedy found the same optimal cost."
        )

    print(
        "Dynamic Programming maximized priority "
        "within the 10-minute testing limit."
    )

    print("=" * 75)


if __name__ == "__main__":
    compare_algorithms()
