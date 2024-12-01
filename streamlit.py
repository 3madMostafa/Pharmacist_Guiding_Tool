import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Load the dataset
@st.cache_data
def load_data():
    file_path = 'last_version.xlsx'
    return pd.read_excel(file_path, sheet_name='last_version')

@st.cache_data
def filter_data(drug_name, insurance, df):
    filtered_df = df[df['Cleaned Up Drug Name'].str.contains(drug_name, na=False, case=False)]
    insurance_cols = [f"{insurance}_check", f"{insurance}_quantity", f"{insurance}_net", f"{insurance}_copay", f"{insurance}_covered"]
    if all(col in df.columns for col in insurance_cols):
        filtered_df = filtered_df[['Cleaned Up Drug Name'] + insurance_cols]
        return filtered_df.rename(columns={
            f"{insurance}_check": "Check",
            f"{insurance}_quantity": "Quantity",
            f"{insurance}_net": "Net",
            f"{insurance}_copay": "Copay",
            f"{insurance}_covered": "Covered"
        }).fillna("Not Available")
    return None

# Load data
df = load_data()
st.title("Pharmacist Guiding Tool 💊")

# Get unique drug names for suggestions
drug_names = df['Cleaned Up Drug Name'].dropna().unique()

# Search bar for Drug Name
drug_name_input = st.text_input("Search for a Drug Name:").strip().upper()
suggested_drugs = [name for name in drug_names if drug_name_input in name.upper()] if drug_name_input else []

drug_name = st.selectbox("Matching Drug Names:", options=suggested_drugs) if suggested_drugs else None

# Get unique insurance names for suggestions
insurance_names = [col.split('_')[0] for col in df.columns if '_check' in col]
insurance_names = list(set(insurance_names))

# Search bar for Insurance
insurance_input = st.text_input("Search for Insurance:").strip().upper()
suggested_insurances = [name for name in insurance_names if insurance_input in name.upper()] if insurance_input else []

selected_insurance = st.selectbox("Matching Insurances:", sorted(suggested_insurances)) if suggested_insurances else None

# Filter and display data
if drug_name and selected_insurance:
    filtered_df = filter_data(drug_name, selected_insurance, df)
    if filtered_df is not None and not filtered_df.empty:
        st.subheader(f"Results for **{drug_name}** and **{selected_insurance}**:")
        gb = GridOptionsBuilder.from_dataframe(filtered_df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_default_column(editable=False, groupable=True)
        gb.configure_columns(["Net", "Copay"], type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2)
        gb.configure_grid_options(domLayout='autoHeight')
        grid_options = gb.build()

        AgGrid(
            filtered_df,
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            theme="balham",
            fit_columns_on_grid_load=True,
            height=400,
        )
    else:
        st.warning(f"No data available for insurance: {selected_insurance}")
else:
    if not drug_name:
        st.info("Start typing a drug name to see suggestions.")
    if not selected_insurance:
        st.info("Start typing an insurance name to see suggestions.")
