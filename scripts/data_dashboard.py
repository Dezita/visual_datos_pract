import pandas as pd
import streamlit as st
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Mental Health Dashboard", layout="wide")

# Load data, use streamlit cache
@st.cache_data
def load_data():
    df = pd.read_csv("data/Mental_Health_clean.csv")
    return df

df = load_data()

# Title dashboard
st.title("Mental Health and Lifestyle Data Exploration Dashboard")
st.markdown("Explore patterns in mental health across countries, genders and age.")

# Define tabs
tab1, tab2 = st.tabs([
    "Mental Health Conditions by Country",
    "Analysis of Mental Health by Gender, Age and Country"
])

# Define color palette for mental health conditions (5 categories)
condition_colors = px.colors.qualitative.Set3[:5]

with tab1:
    st.header("Mental Health Conditions by Country")
    st.markdown("### Geographic Distribution and Prevalence of Mental Health Conditions")

    conditions_list = df["Mental Health Condition"].dropna().unique().tolist()
    conditions_list.sort()
    conditions_list.insert(0, "Total")

    selected_condition = st.selectbox("Select a Mental Health Condition to Display on the Map:", conditions_list)

    # Prepare map data based on mental health condition
    if selected_condition == "Total":
        map_data = df["Country"].value_counts().reset_index()
        map_data.columns = ["Country", "Count"]
    else:
        map_data = df[df["Mental Health Condition"] == selected_condition]["Country"].value_counts().reset_index()
        map_data.columns = ["Country", "Count"]

    fig_map = px.choropleth(
        map_data,
        locations="Country",
        locationmode="country names",
        color="Count",
        title=f"Number of Cases by Country for {selected_condition}",
        color_continuous_scale="YlOrRd",
        labels={"Count": "Number of Cases"}
    )
    fig_map.update_layout(
        height=500,
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Prepare data for stacked bar chart
    condition_country_counts = df.groupby(["Country", "Mental Health Condition"]).size().unstack().fillna(0)
    condition_country_props = condition_country_counts.div(condition_country_counts.sum(axis=1), axis=0)

    fig_bar = px.bar(
        condition_country_props,
        barmode="stack",
        title="Proportion of Mental Health Conditions per Country",
        labels={"value": "Proportion", "Country": "Country"},
        height=500,
        color_discrete_sequence=condition_colors
    )
    fig_bar.update_layout(
        xaxis={'categoryorder': 'category ascending'},
        yaxis_tickformat=".0%",
        legend_title_text="Mental Health Condition"
    )
    st.plotly_chart(fig_bar, use_container_width=True)


with tab2:
    st.header("Analysis of Mental Health by Gender, Age and Country")
    st.markdown("### Explore relationships between mental health conditions, gender, age and geography")

    # Gender color palette
    gender_color_map = {
        "Male": "#5DADE2",    # blue
        "Female": "#EE90DE",  # pink
        "Other": "#3DDB82"    # green
    }

    # Country selector with 'Total' option (affects all charts)
    country_list = ["Total"] + sorted(df["Country"].dropna().unique().tolist())
    selected_country = st.selectbox("Select a Country (or Total for all):", country_list)

    # Filter dataframe based on selected country for all charts
    if selected_country == "Total":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["Country"] == selected_country]

    # Group data for grouped bar chart: count by Mental Health Condition and Gender
    gender_condition_counts = filtered_df.groupby(["Mental Health Condition", "Gender"]).size().reset_index(name="Count")

    # Grouped bar chart: Mental Health Condition by Gender
    fig_bar_gender = px.bar(
        gender_condition_counts,
        x="Mental Health Condition",
        y="Count",
        color="Gender",
        barmode="group",
        color_discrete_map=gender_color_map,
        title=f"Counts of Mental Health Conditions by Gender in {selected_country}"
    )
    fig_bar_gender.update_layout(
        height=400,
        yaxis_title="Number of Cases",
        xaxis_title="Mental Health Condition",
        legend_title_text="Gender"
    )

    # Group data for pie chart: total counts by Gender (proportion)
    gender_counts = filtered_df["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]

    # Pie chart: Gender distribution proportion
    fig_pie = px.pie(
        gender_counts,
        names="Gender",
        values="Count",
        color="Gender",
        color_discrete_map=gender_color_map,
        title="Gender Distribution Proportion"
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')

    # Layout: two charts side by side (bar and pie)
    col1, col2 = st.columns([3, 1])
    col1.plotly_chart(fig_bar_gender, use_container_width=True)
    col2.plotly_chart(fig_pie, use_container_width=True)

    # Next row: line chart + disease selector
    col_line, col_select = st.columns([4,1])

    # Disease selector only for line chart
    condition_list_with_total = ["Total"] + sorted(df["Mental Health Condition"].dropna().unique().tolist())
    selected_condition_line = col_select.selectbox("Select a Mental Health Condition for Line Chart:", condition_list_with_total)

    # Filter data for line chart based on country AND selected_condition_line
    if selected_condition_line == "Total":
        line_df = filtered_df[filtered_df["Age"].notna() & filtered_df["Gender"].notna()]
    else:
        line_df = filtered_df[
            (filtered_df["Mental Health Condition"] == selected_condition_line) &
            filtered_df["Age"].notna() &
            filtered_df["Gender"].notna()
        ]

    # Group by Age and Gender to get counts for line chart
    line_grouped = line_df.groupby(["Age", "Gender"]).size().reset_index(name="Count")

    # Line chart: Number of cases by Age and Gender
    fig_line = px.line(
        line_grouped,
        x="Age",
        y="Count",
        color="Gender",
        color_discrete_map=gender_color_map,
        title=f"Number of Cases by Age and Gender for {selected_condition_line} in {selected_country}"
    )
    fig_line.update_layout(height=350, yaxis_title="Number of Cases", xaxis_title="Age")

    col_line.plotly_chart(fig_line, use_container_width=True)


# File Execution in Terminal:
# streamlit run data_dashboard.py





