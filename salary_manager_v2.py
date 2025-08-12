from __future__ import annotations
# pyright: reportAttributeAccessIssue=false

# New, clean, styled Streamlit interface for salary exploration
# - Loads data from salary_statistics_streamlit.csv (UTF-8)
# - Sidebar filters: company, job, employee search, salary range, sorting
# - KPIs, beautiful charts (Altair), and tabbed layout
# - Download filtered data

import math
from pathlib import Path

import pandas as pd
import streamlit as st  # type: ignore
import altair as alt
from typing import Any, cast


CSV_PATH = Path(__file__).with_name("salary_statistics_streamlit.csv")
TITLE = "Salary Explorer"
SUBTITLE = "Analyze companies, roles, and employee compensation"

"""
Type hints: VS Code/Pylance may not recognize Streamlit's dynamic API.
Cast the module to Any to avoid spurious attribute errors while keeping runtime behavior.
"""
st = cast(Any, st)

@st.cache_data(show_spinner=False)
def load_data(csv_path: Path = CSV_PATH) -> pd.DataFrame:
    """Load the salary CSV with safe parsing.

    Returns a DataFrame with columns: Company, Employee, Job, Salary (float)
    """
    df = pd.read_csv(csv_path, encoding="utf-8")
    # Normalize column names just in case
    df.columns = [c.strip() for c in df.columns]
    # Ensure numeric Salary
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
    df = df.dropna(subset=["Salary"]).copy()
    # Strip spaces around text fields
    for col in ["Company", "Employee", "Job"]:
        df[col] = df[col].astype(str).str.strip()
    return df


def _inject_global_styles() -> None:
    """Add subtle global CSS + a hero header with gradient background."""
    st.markdown(
        """
        <style>
            /* Page tweaks */
            .block-container { padding-top: 1.5rem; padding-bottom: 4rem; }

            /* Card-like metric look */
            .metric-card { background: #ffffffcc; border: 1px solid #e8e8e8; border-radius: 14px;
                           padding: 16px 18px; box-shadow: 0 4px 14px rgba(0,0,0,.06); }
            .metric-title { font-size: .85rem; color: #57606a; margin-bottom: 6px; }
            .metric-value { font-size: 1.6rem; font-weight: 700; }

            /* Dataframe tweaks */
            .stDataFrame { border-radius: 12px; overflow: hidden; }

            /* Hero header */
            .hero {
                background: linear-gradient(135deg, #0ea5e9 0%, #7c3aed 50%, #ec4899 100%);
                color: white; border-radius: 16px; padding: 28px 28px; margin-bottom: 16px;
                box-shadow: 0 10px 24px rgba(0,0,0,.12);
            }
            .hero h1 { font-weight: 800; margin: 0; font-size: 2rem; }
            .hero p { margin: 6px 0 0 0; font-size: 1.05rem; opacity: .95; }

            /* Section title */
            .section-title { font-weight: 700; font-size: 1.05rem; color: #374151; margin: 4px 0 8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="hero">
            <h1>📊 {TITLE}</h1>
            <p>{SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("Filters")
    st.sidebar.caption("Refine by company, role, and employee name.")

    companies = sorted(df["Company"].unique().tolist())
    jobs = sorted(df["Job"].unique().tolist())

    selected_companies = st.sidebar.multiselect(
        "Company",
        options=companies,
        default=companies,
    )

    selected_jobs = st.sidebar.multiselect(
        "Role",
        options=jobs,
        default=jobs,
    )

    employee_query = st.sidebar.text_input("Search employee", placeholder="Type a name…")

    min_sal, max_sal = float(df["Salary"].min()), float(df["Salary"].max())
    step = max(50.0, round((max_sal - min_sal) / 100, 2))
    salary_range = st.sidebar.slider(
        "Salary range",
        min_value=math.floor(min_sal / 50) * 50.0,
        max_value=math.ceil(max_sal / 50) * 50.0,
        value=(min_sal, max_sal),
        step=step,
    )

    sort_by = st.sidebar.selectbox(
        "Sort",
        options=["Salary: High → Low", "Salary: Low → High", "Employee A→Z", "Employee Z→A"],
        index=0,
    )

    st.sidebar.divider()
    show_stats = st.sidebar.checkbox("Show dataset stats", value=True)

    return {
        "companies": selected_companies or companies,
        "jobs": selected_jobs or jobs,
        "employee_query": employee_query.strip(),
        "salary_range": salary_range,
        "sort_by": sort_by,
        "show_stats": show_stats,
    }


def _apply_filters(df: pd.DataFrame, f: dict) -> pd.DataFrame:
    q = df.copy()
    q = q[q["Company"].isin(f["companies"]) & q["Job"].isin(f["jobs"])]

    if f["employee_query"]:
        q = q[q["Employee"].str.contains(f["employee_query"], case=False, na=False)]

    low, high = f["salary_range"]
    q = q[(q["Salary"] >= low) & (q["Salary"] <= high)]

    if f["sort_by"] == "Salary: High → Low":
        q = q.sort_values("Salary", ascending=False)
    elif f["sort_by"] == "Salary: Low → High":
        q = q.sort_values("Salary", ascending=True)
    elif f["sort_by"] == "Employee A→Z":
        q = q.sort_values(["Employee", "Salary"], ascending=[True, False])
    else:  # Employee Z→A
        q = q.sort_values(["Employee", "Salary"], ascending=[False, False])

    return q.reset_index(drop=True)


def _metric_card(title: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _kpi_row(df: pd.DataFrame) -> None:
    total_records = len(df)
    unique_employees = df["Employee"].nunique()
    avg_salary = df["Salary"].mean() if total_records else 0.0
    max_salary = df["Salary"].max() if total_records else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _metric_card("Records", f"{total_records:,}")
    with c2:
        _metric_card("Unique employees", f"{unique_employees:,}")
    with c3:
        _metric_card("Average salary", f"€{avg_salary:,.0f}")
    with c4:
        _metric_card("Highest salary", f"€{max_salary:,.0f}")


def _overview_tab(df: pd.DataFrame) -> None:
    st.markdown("<div class=\"section-title\">Overview</div>", unsafe_allow_html=True)
    _kpi_row(df)

    # Charts: salary distribution by company (boxplot) and average by role
    left, right = st.columns(2)

    with left:
        st.caption("Salary distribution by company")
        box = (
            alt.Chart(df)
            .mark_boxplot(outliers=True)
            .encode(
                x=alt.X("Company:N", title="Company"),
                y=alt.Y("Salary:Q", title="Salary (€)", scale=alt.Scale(zero=False)),
                color=alt.Color("Company:N", legend=None),
            )
            .properties(height=300)
        )
        st.altair_chart(box, use_container_width=True)

    with right:
        st.caption("Average salary by role")
        avg_role = df.groupby("Job", as_index=False).agg(Salary=("Salary", "mean"))
        bar = (
            alt.Chart(avg_role)
            .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
            .encode(
                x=alt.X("Salary:Q", title="Average salary (€)", scale=alt.Scale(zero=False)),
                y=alt.Y("Job:N", sort="-x", title="Role"),
                color=alt.Color("Job:N", legend=None),
                tooltip=["Job", alt.Tooltip("Salary:Q", format=",.0f", title="Avg (€)")],
            )
            .properties(height=300)
        )
        st.altair_chart(bar, use_container_width=True)


def _company_tab(df: pd.DataFrame) -> None:
    st.markdown("<div class=\"section-title\">Company insights</div>", unsafe_allow_html=True)

    # Company-level KPIs
    agg = (
        df.groupby("Company")
        .agg(Employees=("Employee", "nunique"), Records=("Employee", "size"), Avg_Salary=("Salary", "mean"))
        .reset_index()
        .sort_values("Avg_Salary", ascending=False)
    )

    chart = (
        alt.Chart(agg)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("Company:N", title="Company"),
            y=alt.Y("Avg_Salary:Q", title="Average salary (€)", scale=alt.Scale(zero=False)),
            color=alt.Color("Company:N", legend=None),
            tooltip=["Company", alt.Tooltip("Avg_Salary:Q", format=",.0f", title="Avg (€)"), "Employees", "Records"],
        )
        .properties(height=360)
    )
    st.altair_chart(chart, use_container_width=True)

    with st.expander("Show company breakdown table"):
        st.dataframe(
            agg.rename(columns={"Avg_Salary": "Average Salary (€)"}),
            use_container_width=True,
            hide_index=True,
        )


def _role_tab(df: pd.DataFrame) -> None:
    st.markdown("<div class=\"section-title\">Role insights</div>", unsafe_allow_html=True)

    # Use named aggregations to get flat columns and avoid index/column mismatch
    role_company = (
        df.groupby(["Job", "Company"], as_index=False)
        .agg(
            Count=("Salary", "count"),
            Avg=("Salary", "mean"),
            Max=("Salary", "max"),
            Min=("Salary", "min"),
        )
    )

    heat = (
        alt.Chart(role_company)
        .mark_rect()
        .encode(
            x=alt.X("Company:N", title="Company"),
            y=alt.Y("Job:N", title="Role"),
            color=alt.Color("Avg:Q", title="Avg (€)", scale=alt.Scale(scheme="blues")),
            tooltip=["Job", "Company", alt.Tooltip("Avg:Q", format=",.0f", title="Avg (€)"), "Count", "Max", "Min"],
        )
        .properties(height=360)
    )
    st.altair_chart(heat, use_container_width=True)

    with st.expander("Show role breakdown table"):
        st.dataframe(
            role_company.assign(**{"Avg (€)": role_company["Avg"].round(0)}).drop(columns=["Avg"]).rename(columns={"Avg (€)": "Avg (€)"}),
            use_container_width=True,
            hide_index=True,
        )


def _employees_tab(df: pd.DataFrame) -> None:
    st.markdown("<div class=\"section-title\">Employee explorer</div>", unsafe_allow_html=True)

    # Top earners (by max salary per employee) within filtered set
    top = (
        df.groupby("Employee", as_index=False)
        .agg(Salary=("Salary", "max"))
        .sort_values("Salary", ascending=False)
        .head(10)
    )
    bar = (
        alt.Chart(top)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("Salary:Q", title="Top salaries (€)", scale=alt.Scale(zero=False)),
            y=alt.Y("Employee:N", sort="-x", title="Employee"),
            color=alt.Color("Employee:N", legend=None),
            tooltip=["Employee", alt.Tooltip("Salary:Q", format=",.0f", title="Max (€)")],
        )
        .properties(height=360)
    )
    st.altair_chart(bar, use_container_width=True)

    st.caption("Filtered records")
    st.dataframe(
        df[["Company", "Employee", "Job", "Salary"]].rename(columns={"Salary": "Salary (€)"}),
        use_container_width=True,
        hide_index=True,
    )

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download filtered data (CSV)",
        data=csv,
        file_name="filtered_salary_data.csv",
        mime="text/csv",
        use_container_width=True,
    )


def main() -> None:
    st.set_page_config(page_title=TITLE, page_icon="📊", layout="wide")

    df_all = load_data()

    _inject_global_styles()

    filters = _sidebar_filters(df_all)
    df = _apply_filters(df_all, filters)

    if filters["show_stats"]:
        with st.sidebar:
            st.caption("Dataset snapshot")
            st.write(f"Total rows: {len(df_all):,}")
            st.write(f"Companies: {df_all['Company'].nunique():,}")
            st.write(f"Employees: {df_all['Employee'].nunique():,}")
            st.write(f"Roles: {df_all['Job'].nunique():,}")

    # Empty state
    if df.empty:
        st.warning("No results match your filters. Try expanding your selection.")
        return

    tabs = st.tabs(["Overview", "Companies", "Roles", "Employees"])

    with tabs[0]:
        _overview_tab(df)
    with tabs[1]:
        _company_tab(df)
    with tabs[2]:
        _role_tab(df)
    with tabs[3]:
        _employees_tab(df)

    with st.expander("About this app"):
        st.markdown(
            """
            This Streamlit app demonstrates:
            - Cached CSV loading with `st.cache_data`
            - Sidebar filtering and sorting
            - KPIs and Altair charts (boxplot, bar chart, heatmap)
            - Tabbed layout and CSV download
            """
        )


if __name__ == "__main__":
    main()

