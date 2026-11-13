
import streamlit as st
import pandas as pd

from sample_data import samples
from brute_force import brute_force_scheduler
from divide_conquer import divide_conquer_scheduler
from dynamic_programming import dynamic_programming_scheduler
from greedy import greedy_scheduler


st.set_page_config(
    page_title="Blood Sample Testing Scheduler",
    page_icon="🧪",
    layout="wide"
)

# Initialize sample data
if "samples" not in st.session_state:
    st.session_state.samples = [dict(s) for s in samples]


# Header
st.title("🧪 Smart Blood Sample Testing Scheduler")
st.write(
    "An algorithm-based system that schedules blood tests "
    "according to urgency and testing time."
)

st.info(
    "Objective: Minimize the total weighted completion time "
    "of all blood samples."
)

# Add sample section
st.header("1. Add Blood Sample")

with st.form("sample_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        sample_id = st.text_input("Sample ID", placeholder="S107")

    with col2:
        test_name = st.text_input("Test Name", placeholder="Blood Test")

    with col3:
        urgency = st.selectbox(
            "Urgency",
            ["Emergency", "Urgent", "Normal"]
        )

    testing_time = st.number_input(
        "Testing Time (minutes)",
        min_value=1,
        max_value=120,
        value=3
    )

    submitted = st.form_submit_button("Add Sample")

    if submitted:
        if not sample_id.strip() or not test_name.strip():
            st.error("Please enter both Sample ID and Test Name.")

        elif any(
            s["id"].lower() == sample_id.strip().lower()
            for s in st.session_state.samples
        ):
            st.error("Sample ID already exists.")

        elif len(st.session_state.samples) >= 8:
            st.error("Maximum 8 samples allowed for this demonstration.")

        else:
            weights = {
                "Emergency": 10,
                "Urgent": 5,
                "Normal": 1
            }

            st.session_state.samples.append({
                "id": sample_id.strip(),
                "test": test_name.strip(),
                "urgency": urgency,
                "time": int(testing_time),
                "weight": weights[urgency]
            })

            st.success("Blood sample added successfully!")
            st.rerun()


# Display samples
st.header("2. Blood Sample Details")

df = pd.DataFrame(st.session_state.samples)

st.dataframe(df, use_container_width=True, hide_index=True)

col1, col2, col3 = st.columns(3)

col1.metric("Total Samples", len(df))
col2.metric("Total Testing Time", f"{df['time'].sum()} min")
col3.metric("Emergency Samples", len(
    df[df["urgency"] == "Emergency"]
))


# Run algorithms
st.header("3. Algorithm Results")

data = st.session_state.samples

if st.button("Run All Four Algorithms", type="primary"):

    with st.spinner("Running algorithms..."):

        results = {
            "Brute Force": brute_force_scheduler(data),
            "Divide and Conquer": divide_conquer_scheduler(data),
            "Dynamic Programming": dynamic_programming_scheduler(data),
            "Greedy": greedy_scheduler(data)
        }

        st.session_state.results = results

    st.success("All four algorithms completed successfully!")


# Display results
if "results" in st.session_state:

    results = st.session_state.results

    tabs = st.tabs([
        "Brute Force",
        "Divide and Conquer",
        "Dynamic Programming",
        "Greedy"
    ])

    explanations = {
        "Brute Force": (
            "Checks every possible arrangement of blood samples. "
            "It calculates the cost of each arrangement and selects "
            "the one with the lowest cost."
        ),
        "Divide and Conquer": (
            "Divides the sample list into smaller parts, sorts each "
            "part using Merge Sort, and combines them according to "
            "the priority-to-time ratio."
        ),
        "Dynamic Programming": (
            "Uses a bitmask DP table to calculate the minimum cost "
            "for every subset of samples. It builds the optimal "
            "schedule by adding one sample at a time."
        ),
        "Greedy": (
            "Selects the sample with the highest priority-to-time "
            "ratio first and continues in that order."
        )
    }

    complexities = {
        "Brute Force": ("O(n! × n)", "O(n)"),
        "Divide and Conquer": ("O(n log n)", "O(n)"),
        "Dynamic Programming": ("O(n × 2ⁿ)", "O(2ⁿ)"),
        "Greedy": ("O(n log n)", "O(n)")
    }

    for tab, name in zip(tabs, results.keys()):

        with tab:

            result = results[name]

            st.subheader(name)

            st.write("**How it works:**")
            st.write(explanations[name])

            time_c, space_c = complexities[name]

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Minimum Weighted Cost",
                result["total_cost"]
            )

            c2.metric("Time Complexity", time_c)

            c3.metric("Space Complexity", space_c)

            st.write("**Testing Schedule:**")

            schedule_df = pd.DataFrame(result["schedule"])

            st.dataframe(
                schedule_df,
                use_container_width=True,
                hide_index=True
            )

            if name == "Brute Force":
                st.info(
                    f"Total possible arrangements checked: "
                    f"{result['total_orders']}"
                )

            st.write("**Algorithm steps:**")

            if name == "Brute Force":
                steps = [
                    "Generate all possible sample arrangements.",
                    "Calculate completion time for each sample.",
                    "Calculate weighted completion cost.",
                    "Compare all arrangements.",
                    "Select the arrangement with minimum cost."
                ]

            elif name == "Divide and Conquer":
                steps = [
                    "Divide the sample list into two halves.",
                    "Sort each half recursively.",
                    "Compare priority-to-time ratios.",
                    "Merge the sorted halves.",
                    "Calculate the final scheduling cost."
                ]

            elif name == "Dynamic Programming":
                steps = [
                    "Create a DP table for all sample subsets.",
                    "Calculate total processing time for each subset.",
                    "Try adding each remaining sample.",
                    "Store the minimum cost for every subset.",
                    "Reconstruct the optimal testing order."
                ]

            else:
                steps = [
                    "Calculate the priority-to-time ratio.",
                    "Sort samples in descending ratio order.",
                    "Schedule the highest ratio sample first.",
                    "Calculate completion times.",
                    "Calculate the total weighted cost."
                ]

            for i, step in enumerate(steps, 1):
                st.write(f"{i}. {step}")


    # Comparison
    st.header("4. Algorithm Comparison")

    comparison = pd.DataFrame([
        {
            "Algorithm": name,
            "Total Cost": result["total_cost"]
        }
        for name, result in results.items()
    ])

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Cost Comparison Chart")

    st.bar_chart(
        comparison.set_index("Algorithm")
    )

    best_cost = min(
        result["total_cost"] for result in results.values()
    )

    st.success(
        f"Lowest weighted completion cost: {best_cost}"
    )


st.divider()

st.caption(
    "Smart Blood Sample Testing Scheduler | "
    "Academic Algorithm Explorer Project"
)
