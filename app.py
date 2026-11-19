import streamlit as st
import pandas as pd

from sample_data import samples

from brute_force import brute_force_schedule
from divide_conquer import divide_conquer_schedule
from dynamic_programming import dynamic_programming_schedule
from greedy import greedy_schedule


# PAGE CONFIGURATION

st.set_page_config(
    page_title="Blood Sample Testing Scheduler",
    page_icon="🩸",
    layout="wide"
)

st.title("🩸 Smart Blood Sample Testing Scheduler")

st.write(
    "An algorithm-based system to schedule blood samples "
    "using four different approaches."
)

st.info(
    "This project compares Brute Force, Divide and Conquer, "
    "Dynamic Programming, and Greedy algorithms."
)


# SAMPLE DETAILS

st.header("1. Blood Sample Details")

if "samples" not in st.session_state:

    st.session_state.samples = [s.copy() for s in samples]

data = st.session_state.samples

st.dataframe(
    pd.DataFrame(data),
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Samples",
        len(data)
    )

with col2:

    st.metric(
        "Total Testing Time",
        sum(s["time"] for s in data),
        "Minutes"
    )


# ALGORITHM DESCRIPTIONS

st.header("2. Algorithm Approaches")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Brute Force")

    st.write(
        "Checks all possible arrangements and finds "
        "the maximum weighted completion cost."
    )

    st.subheader("Divide and Conquer")

    st.write(
        "Uses Merge Sort to arrange samples from "
        "longest testing time to shortest testing time."
    )

with col2:

    st.subheader("Dynamic Programming")

    st.write(
        "Uses bitmasking and a DP table to minimize "
        "the sum of completion times."
    )

    st.subheader("Greedy")

    st.write(
        "Uses urgency weight divided by testing time "
        "to arrange samples from highest ratio to lowest."
    )


# RUN ALGORITHMS

st.header("3. Algorithm Results")

if st.button("Run All Algorithms", type="primary"):

    with st.spinner("Running all algorithms..."):

        results = {

            "Brute Force": brute_force_schedule(data),

            "Divide and Conquer": divide_conquer_schedule(data),

            "Dynamic Programming": dynamic_programming_schedule(data),

            "Greedy": greedy_schedule(data)

        }

        st.session_state.results = results

    st.success("All four algorithms completed successfully!")


# DISPLAY RESULTS

if "results" in st.session_state:

    results = st.session_state.results

    st.subheader("Individual Algorithm Outputs")

    for name, result in results.items():

        with st.expander(name, expanded=True):

            st.write("**Scheduling Order:**")

            order = result["schedule"]

            order_text = " → ".join(
                sample["id"] for sample in order
            )

            st.write(order_text)

            if name == "Dynamic Programming":

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Minimum Sum of Completion Times",
                        result.get("objective_value", result.get("total_cost", 0))
                    )

                with col2:

                    st.metric(
                        "Weighted Completion Cost",
                        result["total_cost"]
                    )

            else:

                st.metric(
                    "Weighted Completion Cost",
                    result["total_cost"]
                )

            st.write(
                "**Time Complexity:**",
                result["time_complexity"]
            )

            st.write(
                "**Space Complexity:**",
                result["space_complexity"]
            )

            if name == "Brute Force":

                st.write(
                    "**Permutations Checked:**",
                    result["permutations_checked"]
                )

            st.write("**Schedule Details:**")

            schedule_table = []

            for sample in order:

                schedule_table.append({

                    "Sample ID": sample["id"],

                    "Test Name": sample["name"],

                    "Urgency": sample["urgency"],

                    "Testing Time": sample["time"],

                    "Weight": sample["weight"],

                    "Completion Time": sample["completion_time"],

                    "Weighted Cost": sample["weighted_cost"]

                })

            st.dataframe(
                pd.DataFrame(schedule_table),
                use_container_width=True
            )


    # COMPARISON TABLE

    st.header("4. Algorithm Comparison")

    comparison = []

    for name, result in results.items():

        order_text = " → ".join(
            sample["id"]
            for sample in result["schedule"]
        )

        comparison.append({

            "Algorithm": name,

            "Scheduling Order": order_text,

            "Weighted Completion Cost": result["total_cost"],

            "Time Complexity": result["time_complexity"],

            "Space Complexity": result["space_complexity"]

        })

    comparison_df = pd.DataFrame(comparison)

    st.dataframe(
        comparison_df,
        use_container_width=True
    )


    # CHART

    st.header("5. Cost Comparison Chart")

    chart_df = comparison_df[
        ["Algorithm", "Weighted Completion Cost"]
    ].set_index("Algorithm")

    st.bar_chart(chart_df)


    # EXPLANATION

    st.warning(
        "Important: These four approaches use different "
        "scheduling objectives. Their weighted completion "
        "costs are not a direct comparison of four algorithms "
        "solving the same optimization problem."
    )

    st.success("Scheduling comparison completed!")


# FOOTER

st.divider()

st.caption(
    "Smart Blood Sample Testing Scheduler | "
    "Data Structures and Algorithms Project"
)