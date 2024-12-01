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

# Search inputs
drug_name_input = st.text_input("Search for a Drug Name:").strip().upper()
insurance_input = st.text_input("Search for an Insurance:").strip().upper()

# Filter data based on both inputs
if drug_name_input and insurance_input:
    # Filter Drug Name
    filtered_df = df[df['Cleaned Up Drug Name'].str.contains(drug_name_input, na=False, case=False)]
    
    # Filter Insurance Columns
    insurance_cols = [f"{insurance_input}_check",
                      f"{insurance_input}_quantity",
                      f"{insurance_input}_net",
                      f"{insurance_input}_copay",
                      f"{insurance_input}_covered"]
    
    if not filtered_df.empty and all(col in df.columns for col in insurance_cols):
        # Filter relevant columns for Insurance
        filtered_df = filtered_df[['Cleaned Up Drug Name'] + insurance_cols]
        filtered_df = filtered_df.rename(columns={
            f"{insurance_input}_check": "Check",
            f"{insurance_input}_quantity": "Quantity",
            f"{insurance_input}_net": "Net",
            f"{insurance_input}_copay": "Copay",
            f"{insurance_input}_covered": "Covered"
        }).fillna("Not Available")
        
        # Display Results
        st.subheader(f"Results for **{drug_name_input}** with **{insurance_input}**:")
        for _, row in filtered_df.iterrows():
            st.markdown("---")
            st.markdown(f"### Drug Name: **{row['Cleaned Up Drug Name']}**")
            st.markdown(f"- **Check**: {row['Check']}")
            st.markdown(f"- **Quantity**: {row['Quantity']}")
            st.markdown(f"- **Net**: {row['Net']}")
            st.markdown(f"- **Copay**: {row['Copay']}")
            st.markdown(f"- **Covered**: {row['Covered']}")
            st.markdown("---")
    else:
        st.warning(f"No results found for Drug: {drug_name_input} with Insurance: {insurance_input}.")
else:
    st.info("Please enter both Drug Name and Insurance to search.")
