"""
Interactive Facility Intelligence Dashboard.

Run locally:
    streamlit run app.py

Render:
    streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "dataset" / "cleaned_facility_data.csv"


st.set_page_config(
    page_title="Facility Intelligence Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load cleaned data with validated date and numeric types."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Clean dataset not found. Run the data generation and cleaning "
            "pipelines before starting the dashboard."
        )

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["inspection_date"],
    )

    return df


def style_page() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .dashboard-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .dashboard-subtitle {
            color: #6b7280;
            margin-bottom: 1.5rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid rgba(128,128,128,0.20);
            border-radius: 12px;
            padding: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def calculate_risk_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create location-level operational risk score."""
    summary = (
        df.groupby("location")
        .agg(
            average_footfall=("footfall", "mean"),
            average_cleanliness=("cleanliness_score", "mean"),
            average_complaints=("complaints", "mean"),
        )
        .reset_index()
    )

    footfall_range = max(
        summary["average_footfall"].max()
        - summary["average_footfall"].min(),
        1,
    )
    cleanliness_range = max(
        summary["average_cleanliness"].max()
        - summary["average_cleanliness"].min(),
        1,
    )

    summary["footfall_risk"] = (
        summary["average_footfall"]
        - summary["average_footfall"].min()
    ) / footfall_range

    summary["cleanliness_risk"] = (
        summary["average_cleanliness"].max()
        - summary["average_cleanliness"]
    ) / cleanliness_range

    summary["risk_score"] = (
        0.60 * summary["footfall_risk"]
        + 0.40 * summary["cleanliness_risk"]
    )

    return summary.sort_values("risk_score", ascending=False)


def main() -> None:
    style_page()

    try:
        df = load_data()
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    st.markdown(
        '<div class="dashboard-title">🏢 Facility Intelligence Dashboard</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="dashboard-subtitle">'
        "Data quality, hygiene performance and operational risk intelligence"
        "</div>",
        unsafe_allow_html=True,
    )

    # Sidebar filters
    st.sidebar.header("🔎 Dashboard Filters")

    locations = sorted(df["location"].dropna().unique())
    waste_levels = ["Low", "Medium", "High", "Critical"]

    selected_locations = st.sidebar.multiselect(
        "Location",
        options=locations,
        default=locations,
    )

    selected_waste = st.sidebar.multiselect(
        "Waste Level",
        options=waste_levels,
        default=waste_levels,
    )

    min_date = df["inspection_date"].min().date()
    max_date = df["inspection_date"].max().date()

    selected_dates = st.sidebar.date_input(
        "Inspection Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date, end_date = min_date, max_date

    filtered = df[
        df["location"].isin(selected_locations)
        & df["waste_level"].isin(selected_waste)
        & df["inspection_date"].dt.date.between(start_date, end_date)
    ].copy()

    if filtered.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    # KPI calculations
    total_facilities = filtered["facility_id"].nunique()
    average_cleanliness = filtered["cleanliness_score"].mean()
    total_complaints = filtered["complaints"].sum()
    water_uptime = (
        (filtered["water_availability"] == "Yes").mean() * 100
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "Facilities Inspected",
        f"{total_facilities:,}",
    )
    kpi2.metric(
        "Avg. Cleanliness",
        f"{average_cleanliness:.2f}/10",
    )
    kpi3.metric(
        "System Complaints",
        f"{total_complaints:,}",
    )
    kpi4.metric(
        "Water Availability",
        f"{water_uptime:.1f}%",
    )

    st.divider()

    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        location_summary = (
            filtered.groupby("location", as_index=False)
            .agg(
                mean_cleanliness=("cleanliness_score", "mean"),
                std_cleanliness=("cleanliness_score", "std"),
            )
            .sort_values("mean_cleanliness")
        )

        fig = px.bar(
            location_summary,
            x="location",
            y="mean_cleanliness",
            error_y="std_cleanliness",
            title="Mean Cleanliness by Location",
            labels={
                "location": "Location",
                "mean_cleanliness": "Mean Cleanliness",
            },
        )
        fig.update_yaxes(range=[0, 10])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        water_summary = (
            filtered.groupby("water_availability", as_index=False)
            .agg(total_complaints=("complaints", "sum"))
        )

        fig = px.bar(
            water_summary,
            x="water_availability",
            y="total_complaints",
            title="Total Complaints by Water Availability",
            labels={
                "water_availability": "Water Availability",
                "total_complaints": "Total Complaints",
            },
            text_auto=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Charts row 2
    col3, col4 = st.columns(2)

    with col3:
        fig = px.histogram(
            filtered,
            x="footfall",
            nbins=25,
            marginal="box",
            title="Daily Footfall Distribution",
            labels={"footfall": "Daily Visitors"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.scatter(
            filtered,
            x="odor_score",
            y="cleanliness_score",
            color="waste_level",
            hover_data=[
                "facility_id",
                "location",
                "complaints",
                "footfall",
            ],
            trendline="ols",
            title="Odor vs. Cleanliness",
            labels={
                "odor_score": "Odor Score",
                "cleanliness_score": "Cleanliness Score",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap
    st.subheader("📊 Correlation Matrix")

    numeric_columns = [
        "cleanliness_score",
        "odor_score",
        "footfall",
        "complaints",
    ]

    correlation = filtered[numeric_columns].corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.columns,
            zmin=-1,
            zmax=1,
            colorscale="RdBu",
            text=np.round(correlation.values, 2),
            texttemplate="%{text}",
            colorbar_title="Pearson r",
        )
    )

    fig.update_layout(
        title="Pearson Correlation Matrix",
        height=550,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Risk analysis
    st.subheader("⚠️ Operational Risk by Location")

    risk_table = calculate_risk_table(filtered)

    st.dataframe(
        risk_table.style.format(
            {
                "average_footfall": "{:,.0f}",
                "average_cleanliness": "{:.2f}",
                "average_complaints": "{:.2f}",
                "footfall_risk": "{:.2f}",
                "cleanliness_risk": "{:.2f}",
                "risk_score": "{:.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    highest_risk = risk_table.iloc[0]

    st.info(
        f"Highest operational risk location: **{highest_risk['location']}** "
        f"with a risk score of **{highest_risk['risk_score']:.2f}**."
    )

    # Data explorer
    st.subheader("📋 Cleaned Dataset Explorer")

    display_columns = [
        "facility_id",
        "location",
        "cleanliness_score",
        "odor_score",
        "waste_level",
        "water_availability",
        "footfall",
        "complaints",
        "inspection_date",
    ]

    st.dataframe(
        filtered[display_columns].sort_values(
            "inspection_date",
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )

    csv_data = filtered[display_columns].to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Dataset",
        data=csv_data,
        file_name="filtered_facility_data.csv",
        mime="text/csv",
    )

    st.caption(
        "PugArch Technology — Day 3 | Data & AI/ML | "
        "NumPy • Pandas • Matplotlib • Seaborn • Streamlit • Plotly"
    )


if __name__ == "__main__":
    main()
