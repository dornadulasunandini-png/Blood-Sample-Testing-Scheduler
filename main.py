
from sample_data import samples

# Maximum available laboratory testing time
CAPACITY = 10


def dynamic_programming_scheduler():

    n = len(samples)

    # Create DP table
    dp = [[0 for _ in range(CAPACITY + 1)]
          for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):

        sample_time = samples[i - 1]["time"]
        sample_weight = samples[i - 1]["weight"]

        for w in range(CAPACITY + 1):

            # Option 1: Do not select the sample
            dp[i][w] = dp[i - 1][w]

            # Option 2: Select the sample if capacity allows
            if sample_time <= w:

                include = (
                    sample_weight +
                    dp[i - 1][w - sample_time]
                )

                exclude = dp[i - 1][w]

                dp[i][w] = max(include, exclude)

    # Find selected samples using backtracking
    selected_samples = []
    remaining_capacity = CAPACITY

    for i in range(n, 0, -1):

        if dp[i][remaining_capacity] != dp[i - 1][remaining_capacity]:

            selected_samples.append(samples[i - 1])

            remaining_capacity -= samples[i - 1]["time"]

    selected_samples.reverse()

    # Calculate total time and priority
    total_time = sum(
        sample["time"] for sample in selected_samples
    )

    total_priority = sum(
        sample["weight"] for sample in selected_samples
    )

    # Display results
    print("\n======================================")
    print(" DYNAMIC PROGRAMMING SCHEDULER")
    print("======================================")

    print("\nSelected Blood Samples:")

    for sample in selected_samples:
        print(
            sample["id"],
            "-",
            sample["test"],
            "| Time:",
            sample["time"],
            "minutes | Priority:",
            sample["weight"]
        )

    print("\nTotal Testing Time:", total_time, "minutes")
    print("Total Priority Score:", total_priority)

    print("\nMaximum Laboratory Capacity:", CAPACITY, "minutes")

    print("\nDynamic Programming completed successfully!")


if __name__ == "__main__":
    dynamic_programming_scheduler()
