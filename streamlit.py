import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    file_path = 'last_version.xlsx'
    return pd.read_excel(file_path, sheet_name='last_version')

# Load the data
df = load_data()

# Title of the app
st.title("Pharmacist Guiding Tool 💊")

# Search criteria
st.markdown("### Search Options")
search_option = st.radio("Choose search criteria:", ["Drug Name + Insurance", "Drug Name Only", "Insurance Only"], horizontal=True)

# Fetch unique drug names and insurance names
drug_names = df['Cleaned Up Drug Name'].dropna().unique()
insurance_names = list(set([col.split('_')[0] for col in df.columns if '_check' in col]))

# Search fields with auto-complete
if search_option in ["Drug Name + Insurance", "Drug Name Only"]:
    drug_name_input = st.selectbox("Search for a Drug Name:", options=[""] + [name for name in drug_names], format_func=lambda x: x if x else "Type to search...")
else:
    drug_name_input = None

if search_option in ["Drug Name + Insurance", "Insurance Only"]:
    insurance_input = st.selectbox("Search for an Insurance:", options=[""] + [name for name in insurance_names], format_func=lambda x: x if x else "Type to search...")
else:
    insurance_input = None

# Filter data based on the selected criteria
if search_option == "Drug Name + Insurance" and drug_name_input and insurance_input:
    # Filter by both Drug Name and Insurance
    filtered_df = df[df['Cleaned Up Drug Name'].str.contains(drug_name_input, na=False, case=False)]
    insurance_cols = [f"{insurance_input}_check",
                      f"{insurance_input}_quantity",
                      f"{insurance_input}_net",
                      f"{insurance_input}_copay",
                      f"{insurance_input}_covered"]
    if not filtered_df.empty and all(col in df.columns for col in insurance_cols):
        filtered_df = filtered_df[['Cleaned Up Drug Name'] + insurance_cols]
        filtered_df = filtered_df.rename(columns={
            f"{insurance_input}_check": "Check",
            f"{insurance_input}_quantity": "Quantity",
            f"{insurance_input}_net": "Net",
            f"{insurance_input}_copay": "Copay",
            f"{insurance_input}_covered": "Covered"
        }).fillna("Not Available")
    else:
        filtered_df = pd.DataFrame()
elif search_option == "Drug Name Only" and drug_name_input:
    # Filter by Drug Name only
    filtered_df = df[df['Cleaned Up Drug Name'].str.contains(drug_name_input, na=False, case=False)]
elif search_option == "Insurance Only" and insurance_input:
    # Filter by Insurance only
    insurance_cols = [f"{insurance_input}_check",
                      f"{insurance_input}_quantity",
                      f"{insurance_input}_net",
                      f"{insurance_input}_copay",
                      f"{insurance_input}_covered"]
    if all(col in df.columns for col in insurance_cols):
        filtered_df = df[['Cleaned Up Drug Name'] + insurance_cols]
        filtered_df = filtered_df.rename(columns={
            f"{insurance_input}_check": "Check",
            f"{insurance_input}_quantity": "Quantity",
            f"{insurance_input}_net": "Net",
            f"{insurance_input}_copay": "Copay",
            f"{insurance_input}_covered": "Covered"
        }).fillna("Not Available")
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
        if "Check" in row:
            st.markdown(f"- **Check**: {row['Check']}")
            st.markdown(f"- **Quantity**: {row['Quantity']}")
            st.markdown(f"- **Net**: {row['Net']}")
            st.markdown(f"- **Copay**: {row['Copay']}")
            st.markdown(f"- **Covered**: {row['Covered']}")
        st.markdown("---")
else:
    if search_option == "Drug Name + Insurance" and drug_name_input and insurance_input:
        st.warning(f"No results found for Drug: {drug_name_input} with Insurance: {insurance_input}.")
    elif search_option == "Drug Name Only" and drug_name_input:
        st.warning(f"No results found for Drug: {drug_name_input}.")
    elif search_option == "Insurance Only" and insurance_input:
        st.warning(f"No results found for Insurance: {insurance_input}.")
    else:
        st.info("Please enter search criteria above to get results.")
