
import streamlit as st
import pandas as pd

from sample_data import samples
from brute_force import brute_force_schedule
from divide_conquer import divide_conquer_schedule
from dynamic_programming import dynamic_programming_schedule
from greedy import greedy_schedule


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

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
    "Add blood samples, select their urgency levels, "
    "and compare four scheduling algorithms."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "samples" not in st.session_state:
    st.session_state.samples = [s.copy() for s in samples]


# --------------------------------------------------
# ADD NEW BLOOD SAMPLE
# --------------------------------------------------

st.header("1. Add New Blood Sample")

with st.form("add_sample_form"):

    col1, col2 = st.columns(2)

    with col1:

        sample_id = st.text_input(
            "Blood Sample ID",
            placeholder="Example: S107"
        )

        sample_name = st.text_input(
            "Test Name",
            placeholder="Example: Vitamin D"
        )

    with col2:

        urgency = st.selectbox(
            "Urgency Level",
            ["Emergency", "Urgent", "Normal"]
        )

        testing_time = st.number_input(
            "Testing Time (minutes)",
            min_value=1,
            max_value=120,
            value=3
        )

    submitted = st.form_submit_button(
        "➕ Add Blood Sample",
        use_container_width=True
    )

    if submitted:

        sample_id = sample_id.strip()
        sample_name = sample_name.strip()

        if not sample_id or not sample_name:

            st.error(
                "Please enter both Blood Sample ID and Test Name."
            )

        elif any(
            s["id"].lower() == sample_id.lower()
            for s in st.session_state.samples
        ):

            st.error(
                "This Blood Sample ID already exists. "
                "Please enter a different ID."
            )

        else:

            urgency_weights = {
                "Emergency": 10,
                "Urgent": 5,
                "Normal": 1
            }

            new_sample = {
                "id": sample_id,
                "name": sample_name,
                "urgency": urgency,
                "time": int(testing_time),
                "weight": urgency_weights[urgency]
            }

            st.session_state.samples.append(new_sample)

            # Clear old algorithm results
            st.session_state.pop("results", None)

            st.success(
                f"Blood sample {sample_id} added successfully!"
            )

            st.rerun()


# --------------------------------------------------
# SAMPLE DETAILS
# --------------------------------------------------

st.header("2. Blood Sample Details")

data = st.session_state.samples

sample_df = pd.DataFrame(data)

st.dataframe(
    sample_df,
    use_container_width=True,
    hide_index=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Samples",
        len(data)
    )

with col2:

    st.metric(
        "Total Testing Time",
        f"{sum(s['time'] for s in data)} minutes"
    )

with col3:

    st.metric(
        "Emergency Samples",
        sum(
            1 for s in data
            if s["urgency"] == "Emergency"
        )
    )


# --------------------------------------------------
# REMOVE SAMPLE
# --------------------------------------------------

st.subheader("Remove a Blood Sample")

sample_ids = [s["id"] for s in data]

if sample_ids:

    selected_id = st.selectbox(
        "Select Sample ID to remove",
        sample_ids
    )

    if st.button("Remove Selected Sample"):

        st.session_state.samples = [
            s for s in st.session_state.samples
            if s["id"] != selected_id
        ]

        st.session_state.pop("results", None)

        st.success(
            f"Sample {selected_id} removed successfully."
        )

        st.rerun()


# --------------------------------------------------
# ALGORITHM DESCRIPTIONS
# --------------------------------------------------

st.header("3. Algorithm Approaches")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Brute Force")

    st.write(
        "Checks all possible sample arrangements and finds "
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
        "the sum of completion times without using "
        "urgency weights in the optimization."
    )

    st.subheader("Greedy")

    st.write(
        "Calculates urgency weight divided by testing time "
        "and schedules the highest ratio first."
    )


# --------------------------------------------------
# RUN ALL ALGORITHMS
# --------------------------------------------------

st.header("4. Algorithm Results")

if st.button(
    "▶ Run All Algorithms",
    type="primary",
    use_container_width=True
):

    if not data:

        st.error("Please add at least one blood sample.")

    else:

        try:

            with st.spinner("Running all four algorithms..."):

                results = {

                    "Brute Force":
                        brute_force_schedule(data),

                    "Divide and Conquer":
                        divide_conquer_schedule(data),

                    "Dynamic Programming":
                        dynamic_programming_schedule(data),

                    "Greedy":
                        greedy_schedule(data)

                }

                st.session_state.results = results

            st.success(
                "All four algorithms completed successfully!"
            )

        except Exception as e:

            st.error("An error occurred while running the algorithms.")

            st.exception(e)


# --------------------------------------------------
# DISPLAY ALGORITHM RESULTS
# --------------------------------------------------

if "results" in st.session_state:

    results = st.session_state.results

    st.subheader("Individual Algorithm Outputs")

    for name, result in results.items():

        with st.expander(name, expanded=True):

            schedule = result["schedule"]

            st.write("**Scheduling Order:**")

            order_text = " → ".join(
                sample["id"] for sample in schedule
            )

            st.write(order_text)

            # DP has two different values
            if name == "Dynamic Programming":

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Minimum Sum of Completion Times",
                        result["objective_value"]
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

            # Schedule table

            st.write("**Schedule Details:**")

            schedule_table = []

            for sample in schedule:

                schedule_table.append({

                    "Sample ID": sample["id"],

                    "Test Name": sample["name"],

                    "Urgency": sample["urgency"],

                    "Testing Time": sample["time"],

                    "Urgency Weight": sample["weight"],

                    "Completion Time": sample["completion_time"],

                    "Weighted Cost": sample["weighted_cost"]

                })

            st.dataframe(
                pd.DataFrame(schedule_table),
                use_container_width=True,
                hide_index=True
            )


    # --------------------------------------------------
    # COMPARISON TABLE
    # --------------------------------------------------

    st.header("5. Algorithm Comparison")

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
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------
    # COST COMPARISON CHART
    # --------------------------------------------------

    st.header("6. Weighted Completion Cost Comparison")

    chart_df = comparison_df[
        ["Algorithm", "Weighted Completion Cost"]
    ].set_index("Algorithm")

    st.bar_chart(chart_df)


    # --------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------

    st.warning(
        "Important: The four algorithms use different "
        "scheduling objectives and strategies. Their "
        "weighted completion costs are not a direct "
        "comparison of four solutions to the same "
        "optimization problem."
    )

    st.success(
        "Scheduling and algorithm comparison completed!"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Smart Blood Sample Testing Scheduler | "
    "Data Structures and Algorithms Project"
)
