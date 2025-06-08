# %%
# Imports and settings
import pandas as pd
import numpy as np

# %%
# Load the CSV file (adjust path accordingly)
csv_path = "../data/Mental_Health_Lifestyle_Dataset.csv"
df = pd.read_csv(csv_path)

# %%
# Check the first few rows to understand the data
print(df.head())

# %%
# Get basic info about columns, data types, and nulls
print(df.info())

# %%
# Summary statistics for numerical columns
print(df.describe())

# %%
# Check for missing values per column
print(df.isnull().sum())

# We obwerve that only Mental Health Condition contains NULL values.
# Next, we will evaluate the relationship between this nulls and the rest
# of the variables to decide if we impute them or just eliminate them.

# %%
# Evaluate missing values in Mental Health Condition with other variables

# Create a new column to indicate if the value is missing
df["MH_Missing"] = df["Mental Health Condition"].isnull()

# Define numerical and categorical columns
numerical_cols = [
    "Age", "Sleep Hours", "Work Hours per Week",
    "Screen Time per Day (Hours)", "Social Interaction Score", "Happiness Score"
]

categorical_cols = [
    "Gender", "Country", "Exercise Level", "Diet Type", "Stress Level"
]

# Analysis of numerical variables
print("=== Numerical Variables Analysis by Missing Mental Health Condition ===")
for col in numerical_cols:
    print(f"\n>> {col}")
    print(df.groupby("MH_Missing")[col].describe())

# Analysis of categorical variables
print("\n=== Categorical Variables Analysis by Missing Mental Health Condition ===")
for col in categorical_cols:
    print(f"\n>> {col}")
    print(df.groupby("MH_Missing")[col].value_counts(normalize=True))


# %% 
# Visualize dsitribution of nulls in all the other variables

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


# Set seaborn theme
# sns.set(style="whitegrid")

# VIOLIN PLOTS for numerical variables
for col in numerical_cols:
    plt.figure(figsize=(8, 5))
    sns.violinplot(x="MH_Missing", y=col, data=df, palette="Set2")
    plt.title(f"{col} by Missing Mental Health Condition")
    plt.xlabel("Mental Health Condition is Missing")
    plt.ylabel(col)
    plt.tight_layout()
    plt.show()

# COUNT PLOTS for categorical variables
for col in categorical_cols:
    plt.figure(figsize=(8, 5))
    sns.countplot(x=col, hue="MH_Missing", data=df, palette="Set1")
    plt.title(f"{col} vs Missing Mental Health Condition")
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.legend(title="MH Condition Missing")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# %% Since the missed values does not show any pattern in all the different 
# variables, we delete them and prepare the visualization using the 
# rest 2405 rows

# Drop the rows with NA and the column MH_Missing
df_clean = df.dropna(subset=["Mental Health Condition"])
df_clean = df_clean.drop(columns=["MH_Missing"])


# %% 
# Statistics numerical variables
df_clean.describe()

# %% 
# Statistics categorical variables

for col in categorical_cols:
    print(f"\n=== Category counts for: {col} ===")
    print(df_clean[col].value_counts(dropna=False))

# %%
# Export clean dataset to a new csv to be used for visualization
df_clean.to_csv("../data/Mental_Health_clean.csv", index=False)
