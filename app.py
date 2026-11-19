
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
    "An algorithm-based system that demonstrates different "
    "blood sample scheduling strategies."
)

st.info(
    "This project compares four scheduling approaches "
    "using different scheduling objectives."
)


# Add sample section
st.header("1. Add Blood Sample")

with st.form("sample_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        sample_id = st.text_input(
            "Sample ID",
            placeholder="S107"
        )

    with col2:
        test_name = st.text_input(
            "Test Name",
            placeholder="Blood Test"
        )

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
            st.error("Maximum 8 samples allowed.")

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

            # Remove old results after changing sample data
            st.session_state.pop("results", None)

            st.success("Blood sample added successfully!")
            st.rerun()


# Display samples
st.header("2. Blood Sample Details")

df = pd.DataFrame(st.session_state.samples)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Samples", len(df))

col2.metric(
    "Total Testing Time",
    f"{df['time'].sum()} min"
)

col3.metric(
    "Emergency Samples",
    len(df[df["urgency"] == "Emergency"])
)


# Algorithm descriptions
explanations = {

    "Brute Force": (
        "Checks every possible sample arrangement and selects "
        "the arrangement with the highest weighted completion cost. "
        "It demonstrates the worst-case scheduling arrangement."
    ),

    "Divide and Conquer": (
        "Divides the sample list into smaller groups, sorts them "
        "using Merge Sort, and combines them by arranging the "
        "longest testing time first."
    ),

    "Dynamic Programming": (
        "Uses bitmasking and a DP table to store previous results. "
        "It finds the schedule that minimizes the sum of completion "
        "times without using urgency weights in the optimization."
    ),

    "Greedy": (
        "Calculates urgency weight divided by testing time. "
        "It arranges samples from the highest ratio to the lowest "
        "ratio to minimize weighted completion cost."
    )
}


# Run algorithms
st.header("3. Algorithm Results")

data = st.session_state.samples

if st.button("Run All Four Algorithms", type="primary"):

    with st.spinner("Running all four algorithms..."):

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

    for tab, name in zip(tabs, results.keys()):

        with tab:

            result = results[name]

            st.subheader(name)

            st.write("**How it works:**")
            st.write(explanations[name])

            st.write("**Scheduling objective:**")
            st.write(result.get("objective", "Scheduling comparison"))

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Weighted Completion Cost",
                result["total_cost"]
            )

            c2.metric(
                "Time Complexity",
                result["time_complexity"]
            )

            c3.metric(
                "Space Complexity",
                result["space_complexity"]
            )

            if name == "Dynamic Programming":
                st.metric(
                    "Minimum Sum of Completion Times",
                    result["objective_value"]
                )

            st.write("**Testing Schedule:**")

            schedule_df = pd.DataFrame(result["schedule"])

            st.dataframe(
                schedule_df,
                use_container_width=True,
                hide_index=True
            )

            order = " → ".join(
                item["id"] for item in result["schedule"]
            )

            st.write("**Sample ID Order:**")
            st.code(order)

            if name == "Brute Force":

                st.info(
                    f"Total possible arrangements checked: "
                    f"{result['total_orders']}"
                )

            st.write("**Algorithm steps:**")

            if name == "Brute Force":

                steps = [
                    "Generate all possible sample arrangements.",
                    "Calculate completion time for every sample.",
                    "Calculate weighted completion cost.",
                    "Compare all possible arrangements.",
                    "Select the arrangement with maximum cost."
                ]

            elif name == "Divide and Conquer":

                steps = [
                    "Divide the sample list into two halves.",
                    "Sort each half recursively.",
                    "Compare testing times.",
                    "Merge the halves in descending testing-time order.",
                    "Calculate the weighted completion cost."
                ]

            elif name == "Dynamic Programming":

                steps = [
                    "Create a DP table for all sample subsets.",
                    "Use bitmasking to represent selected samples.",
                    "Calculate total processing time for each subset.",
                    "Store the minimum sum of completion times.",
                    "Reconstruct the final testing order."
                ]

            else:

                steps = [
                    "Calculate urgency weight divided by testing time.",
                    "Sort samples by descending ratio.",
                    "Select the highest-ratio sample first.",
                    "Calculate completion times.",
                    "Calculate total weighted completion cost."
                ]

            for i, step in enumerate(steps, 1):
                st.write(f"{i}. {step}")


    # Algorithm comparison
    st.header("4. Algorithm Comparison")

    comparison_rows = []

    for name, result in results.items():

        order = " → ".join(
            item["id"] for item in result["schedule"]
        )

        comparison_rows.append({
            "Algorithm": name,
            "Scheduling Objective": result.get("objective", ""),
            "Sample Order": order,
            "Weighted Cost": result["total_cost"],
            "Time Complexity": result["time_complexity"],
            "Space Complexity": result["space_complexity"]
        })

    comparison = pd.DataFrame(comparison_rows)

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Weighted Cost Comparison")

    chart_data = comparison[
        ["Algorithm", "Weighted Cost"]
    ].set_index("Algorithm")

    st.bar_chart(chart_data)

    st.warning(
        "The four algorithms use different scheduling objectives. "
        "Their weighted costs are shown for comparison, but the "
        "lowest cost is not a fair overall winner because the "
        "algorithms are not optimizing the same objective."
    )


# Footer
st.divider()

st.caption(
    "Smart Blood Sample Testing Scheduler | "
    "Academic Algorithm Explorer Project"
)
