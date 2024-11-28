import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    # Replace this with the path to your Excel file
    file_path = 'last_version.xlsx'
    return pd.read_excel(file_path, sheet_name='last_version')

# Load the data
df = load_data()

# Title of the app
st.title("Pharmacist Guiding Tool")

# Get unique drug names for suggestions
drug_names = df['Cleaned Up Drug Name'].dropna().unique()

# Search bar with suggestions
drug_name_input = st.text_input("Search for a Drug Name:").strip().upper()

# Suggestion logic: Display dropdown if input matches partial names
suggested_drugs = [name for name in drug_names if drug_name_input in name.upper()]
drug_name = st.selectbox("Matching Drug Names:", options=suggested_drugs) if suggested_drugs else None

# Dropdown for insurance selection
insurance_names = [col.split('_')[0] for col in df.columns if '_check' in col]
insurance_names = list(set(insurance_names))
selected_insurance = st.selectbox("Select an Insurance:", sorted(insurance_names))

# Filter data based on selected drug name
if drug_name:
    filtered_df = df[df['Cleaned Up Drug Name'].str.contains(drug_name, na=False, case=False)]
    if not filtered_df.empty:
        st.write(f"Results for **{drug_name}**:")

        # Display relevant insurance details
        insurance_cols = [f"{selected_insurance}_check",
                          f"{selected_insurance}_quantity",
                          f"{selected_insurance}_net",
                          f"{selected_insurance}_copay",
                          f"{selected_insurance}_covered"]

        if all(col in df.columns for col in insurance_cols):
            filtered_df = filtered_df[['Cleaned Up Drug Name'] + insurance_cols]
            st.dataframe(filtered_df.rename(columns={
                f"{selected_insurance}_check": "Check",
                f"{selected_insurance}_quantity": "Quantity",
                f"{selected_insurance}_net": "Net",
                f"{selected_insurance}_copay": "Copay",
                f"{selected_insurance}_covered": "Covered"
            }))
        else:
            st.warning(f"No data available for insurance: {selected_insurance}")
    else:
        st.warning(f"No results found for drug: {drug_name}")
else:
    st.info("Start typing a drug name to see suggestions.")
