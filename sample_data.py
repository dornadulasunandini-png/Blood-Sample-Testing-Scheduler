
# SMART BLOOD SAMPLE TESTING SCHEDULER
# Sample Dataset

samples = [
    {
        "id": "S101",
        "test": "CBC",
        "urgency": "Emergency",
        "time": 2,
        "weight": 10
    },
    {
        "id": "S102",
        "test": "Blood Sugar",
        "urgency": "Normal",
        "time": 3,
        "weight": 1
    },
    {
        "id": "S103",
        "test": "Hemoglobin",
        "urgency": "Urgent",
        "time": 2,
        "weight": 5
    },
    {
        "id": "S104",
        "test": "Lipid Profile",
        "urgency": "Normal",
        "time": 4,
        "weight": 1
    },
    {
        "id": "S105",
        "test": "Platelet Count",
        "urgency": "Emergency",
        "time": 3,
        "weight": 10
    },
    {
        "id": "S106",
        "test": "Thyroid Test",
        "urgency": "Urgent",
        "time": 5,
        "weight": 5
    }
]


def display_samples():
    print("\n" + "=" * 75)
    print("       SMART BLOOD SAMPLE TESTING SCHEDULER")
    print("=" * 75)

    print(
        f"{'ID':<10}"
        f"{'TEST TYPE':<20}"
        f"{'URGENCY':<15}"
        f"{'TIME':<12}"
        f"{'WEIGHT':<10}"
    )

    print("-" * 75)

    for sample in samples:
        print(
            f"{sample['id']:<10}"
            f"{sample['test']:<20}"
            f"{sample['urgency']:<15}"
            f"{sample['time']:<12}"
            f"{sample['weight']:<10}"
        )

    print("=" * 75)


if __name__ == "__main__":
    display_samples()
