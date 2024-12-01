import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

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

# Get unique drug names for suggestions
drug_names = df['Cleaned Up Drug Name'].dropna().unique()

# Search bar with suggestions for Drug Name
drug_name_input = st.text_input("Search for a Drug Name:").strip().upper()
suggested_drugs = [name for name in drug_names if drug_name_input in name.upper()]
drug_name = st.selectbox("Matching Drug Names:", options=suggested_drugs) if suggested_drugs else None

# Get unique insurance names for suggestions
insurance_names = [col.split('_')[0] for col in df.columns if '_check' in col]
insurance_names = list(set(insurance_names))

# Search bar with suggestions for Insurance
insurance_input = st.text_input("Search for Insurance:").strip().upper()
suggested_insurances = [name for name in insurance_names if insurance_input in name.upper()]
selected_insurance = st.selectbox("Matching Insurances:", sorted(suggested_insurances)) if suggested_insurances else None

# Filter data based on selected drug name and insurance
if drug_name and selected_insurance:
    filtered_df = df[df['Cleaned Up Drug Name'].str.contains(drug_name, na=False, case=False)]
    if not filtered_df.empty:
        st.subheader(f"Results for **{drug_name}** and **{selected_insurance}**:")
        
        # Display relevant insurance details
        insurance_cols = [f"{selected_insurance}_check",
                          f"{selected_insurance}_quantity",
                          f"{selected_insurance}_net",
                          f"{selected_insurance}_copay",
                          f"{selected_insurance}_covered"]

        if all(col in df.columns for col in insurance_cols):
            filtered_df = filtered_df[['Cleaned Up Drug Name'] + insurance_cols]
            filtered_df = filtered_df.rename(columns={
                f"{selected_insurance}_check": "Check",
                f"{selected_insurance}_quantity": "Quantity",
                f"{selected_insurance}_net": "Net",
                f"{selected_insurance}_copay": "Copay",
                f"{selected_insurance}_covered": "Covered"
            })
            
            # إعداد خيارات عرض الجدول
            gb = GridOptionsBuilder.from_dataframe(filtered_df)
            gb.configure_pagination(paginationAutoPageSize=True)  # تفعيل التصفح الصفحات
            gb.configure_default_column(editable=False, groupable=True)
            gb.configure_columns(["Net", "Copay"], type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2)
            gb.configure_selection('single')
            grid_options = gb.build()

            # عرض الجدول باستخدام AgGrid
            AgGrid(
                filtered_df,
                gridOptions=grid_options,
                enable_enterprise_modules=True,
                theme="balham",  # يمكنك تجربة "streamlit", "material", "balham-dark"
                fit_columns_on_grid_load=True,
                height=400,
            )
        else:
            st.warning(f"No data available for insurance: {selected_insurance}")
    else:
        st.warning(f"No results found for drug: {drug_name}")
elif not drug_name:
    st.info("Start typing a drug name to see suggestions.")
elif not selected_insurance:
    st.info("Start typing an insurance name to see suggestions.")
