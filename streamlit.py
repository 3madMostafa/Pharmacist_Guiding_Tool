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
st.title("Pharmacist Guiding Tool 💊")

# Flexible search options
search_options = ["Drug Name", "Insurance"]
search_by = st.radio("What do you want to search by?", search_options)

# Flexible search input
search_input = st.text_input(f"Search for a {search_by}:").strip().upper()

# Handle search logic
if search_by == "Drug Name":
    unique_values = df['Cleaned Up Drug Name'].dropna().unique()
elif search_by == "Insurance":
    unique_values = [col.split('_')[0] for col in df.columns if '_check' in col]

# Filter matching results
if search_input:
    matched_values = [value for value in unique_values if search_input in value.upper()]
    selected_value = st.selectbox(f"Matching {search_by}s:", options=matched_values) if matched_values else None
else:
    selected_value = None

# Display results based on selection
if selected_value:
    if search_by == "Drug Name":
        filtered_df = df[df['Cleaned Up Drug Name'].str.contains(selected_value, na=False, case=False)]
    elif search_by == "Insurance":
        insurance_cols = [f"{selected_value}_check",
                          f"{selected_value}_quantity",
                          f"{selected_value}_net",
                          f"{selected_value}_copay",
                          f"{selected_value}_covered"]
        filtered_df = df[['Cleaned Up Drug Name'] + insurance_cols] if all(col in df.columns for col in insurance_cols) else pd.DataFrame()

    if not filtered_df.empty:
        st.subheader(f"Results for **{selected_value}**:")

        # Display data in a stylish format
        for _, row in filtered_df.iterrows():
            st.markdown("---")
            st.markdown(f"### Drug Name: **{row['Cleaned Up Drug Name']}**")
            if search_by == "Insurance":
                st.markdown(f"- **Check**: {row.get(f'{selected_value}_check', 'Not Available')}")
                st.markdown(f"- **Quantity**: {row.get(f'{selected_value}_quantity', 'Not Available')}")
                st.markdown(f"- **Net**: {row.get(f'{selected_value}_net', 'Not Available')}")
                st.markdown(f"- **Copay**: {row.get(f'{selected_value}_copay', 'Not Available')}")
                st.markdown(f"- **Covered**: {row.get(f'{selected_value}_covered', 'Not Available')}")
            st.markdown("---")
    else:
        st.warning(f"No results found for {selected_value}.")
else:
    st.info(f"Start typing to search for a {search_by}.")
