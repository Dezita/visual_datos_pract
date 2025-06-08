import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("../data/Mental_Health_clean.csv")
    return df

df = load_data()

# Add an "All" option for the diseases select list
diseases = df["Mental Health Condition"].dropna().unique().tolist()
diseases = ["All"] + diseases

st.title("Mental Health Dashboard")

# Select disease
selected_disease = st.selectbox("Select Mental Health Condition:", diseases)

# Filter data based on selection
if selected_disease != "All":
    df_filtered = df[df["Mental Health Condition"] == selected_disease]
else:
    df_filtered = df.copy()

st.markdown(f"### Dataset filtered by: **{selected_disease}**")
st.write(f"Number of records: {len(df_filtered)}")

# 1. Bar chart: Gender distribution
gender_counts = df_filtered["Gender"].value_counts().reset_index()
gender_counts.columns = ["Gender", "Count"]

fig_gender = px.bar(gender_counts, x="Gender", y="Count", color="Gender",
                    title="Gender Distribution",
                    labels={"Count": "Number of Records"})

st.plotly_chart(fig_gender, use_container_width=True)

# 2. Violin plot: Work Hours per Week by Gender
fig_work_hours = px.violin(df_filtered, y="Work Hours per Week", x="Gender", color="Gender",
                          box=True, points="all",
                          title="Work Hours per Week by Gender")
st.plotly_chart(fig_work_hours, use_container_width=True)

# 3. Boxplot: Happiness Score by Gender
fig_happiness = px.box(df_filtered, y="Happiness Score", x="Gender", color="Gender",
                      title="Happiness Score by Gender")
st.plotly_chart(fig_happiness, use_container_width=True)

# 4. Choropleth Map: Count of records by Country
country_counts = df_filtered["Country"].value_counts().reset_index()
country_counts.columns = ["Country", "Count"]

fig_map = px.choropleth(country_counts, locations="Country", locationmode="country names",
                        color="Count", color_continuous_scale="Viridis",
                        title="Records Count by Country")
st.plotly_chart(fig_map, use_container_width=True)

# File Execution in Terminal:
# streamlit run data_dashboard.py
