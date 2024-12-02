import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    file_path = 'Matched_Data_Final2.csv'  # Updated file name
    return pd.read_csv(file_path).drop_duplicates()

# Load the data
df = load_data()

# Title of the app
st.title("CDI Medication Guiding Tool 💊")

# Search criteria
st.markdown("### Search Options")
st.info("Search is only allowed using both Drug Name and Insurance.")

# Fetch unique drug names and insurance names
drug_names = df['Cleaned Up Drug Name'].dropna().unique()
insurance_names = df['Insurance'].dropna().unique()

# Search fields with auto-complete
drug_name_input = st.selectbox("Search for a Drug Name:", options=[""] + [name for name in drug_names], format_func=lambda x: x if x else "Type to search...")
insurance_input = st.selectbox("Search for an Insurance:", options=[""] + [name for name in insurance_names], format_func=lambda x: x if x else "Type to search...")

# Filter data based on the selected criteria
if drug_name_input and insurance_input:
    # Filter by both Drug Name and Insurance
    filtered_df = df[(df['Cleaned Up Drug Name'].str.contains(drug_name_input, na=False, case=False)) & 
                     (df['Insurance'].str.contains(insurance_input, na=False, case=False))]
    if not filtered_df.empty:
        filtered_df = filtered_df[['Cleaned Up Drug Name', 'Quantity', 'Net', 'Copay']].drop_duplicates().fillna("Not Available")
    else:
        filtered_df = pd.DataFrame()
else:
    filtered_df = pd.DataFrame()

# Display results
if not filtered_df.empty:
    st.subheader(f"Results for your search:")
    for _, row in filtered_df.iterrows():
        st.markdown("---")
        st.markdown(f"### Drug Name: **{row['Cleaned Up Drug Name']}**")
        st.markdown(f"- **Quantity**: {row['Quantity']}")
        st.markdown(f"- **Net**: {row['Net']}")
        st.markdown(f"- **Copay**: {row['Copay']}")
        st.markdown("---")
else:
    if drug_name_input and insurance_input:
        st.warning(f"No results found for Drug: {drug_name_input} with Insurance: {insurance_input}.")
    else:
        st.info("Please enter both Drug Name and Insurance to get results.")
