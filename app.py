import streamlit as st
import pandas as pd

from calculations import (
    calculate_shear,
    calculate_delta_t,
    calculate_delta_t_per_height,
    classify_stability
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Thermal Stability Classifier",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ GAWC Renewables - Thermal Stability Classifier")

tab1, tab2 = st.tabs(["📝 Manual Input", "📂 File Upload"])

# =====================================================
# TAB 1 : MANUAL INPUT
# =====================================================

with tab1:

    st.header("Enter Atmospheric Data")

    col1, col2 = st.columns(2)

    with col1:
        speed_59 = st.number_input(
            "Wind Speed at 59m (m/s)",
            min_value=0.0,
            value=0.0,
            step=0.1
        )

        temp_59 = st.number_input(
            "Temperature at 59m (°C)",
            value=0.0,
            step=0.1
        )

    with col2:
        speed_22 = st.number_input(
            "Wind Speed at 22m (m/s)",
            min_value=0.0,
            value=0.0,
            step=0.1
        )

        temp_22 = st.number_input(
            "Temperature at 22m (°C)",
            value=0.0,
            step=0.1
        )

    if st.button("Calculate"):

        shear = calculate_shear(speed_59, speed_22, 59, 22)

        delta_t = calculate_delta_t(temp_59, temp_22)

        delta_t_h = calculate_delta_t_per_height(delta_t)

        stability = classify_stability(delta_t_h)

        st.divider()

        st.subheader("Results")

        c1, c2, c3 = st.columns(3)

        c1.metric("Shear", f"{shear:.4f}")
        c2.metric("Delta T", f"{delta_t:.2f} °C")
        c3.metric("Delta T/H", f"{delta_t_h:.4f}")

        st.write("### Stability Class")

        if stability.lower() == "unstable":
            st.success(f"🟢 {stability}")

        elif stability.lower() == "stable":
            st.error(f"🔴 {stability}")

        else:
            st.warning(f"🟡 {stability}")

# =====================================================
# TAB 2 : FILE UPLOAD
# =====================================================

with tab2:

    st.header("Upload Excel File")

    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=["xlsx"]
    )

    if uploaded_file is not None:

        df = pd.read_excel(uploaded_file)

        st.subheader("Input Data")

        st.dataframe(df)

        try:

        

            df["Shear"] = df.apply(
                lambda row: calculate_shear(
                    row["Speed59 m A [m/s]"],
                    row["Speed 22m [m/s]"],
                    59,
                    22
                ),
                axis=1
            )

            df["Delta T"] = df.apply(
                lambda row: calculate_delta_t(
                    row["Temperature 59 m [°C]"],
                  row["Temperature 22 m [°C]"]

                ),
                axis=1
            )

            df["Delta T/deltaH"] = df["Delta T"].apply(
                calculate_delta_t_per_height
            )

            df["Class"] = df["Delta T/deltaH"].apply(
                classify_stability
            )

            st.success("Processing Complete!")

            st.subheader("Processed Results")

            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Results",
                data=csv,
                file_name="processed_results.csv",
                mime="text/csv"
            )

        except KeyError as e:

            st.error(
                f"Column not found: {e}\n\n"
                "Please make sure the Excel column names match exactly."
            )

        except Exception as e:

            st.error(f"Error while processing file:\n{e}")

