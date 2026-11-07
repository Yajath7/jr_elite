import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="Maintenance Ledger App", layout="wide")
st.title("🏡 Plot Maintenance Ledger Dashboard")
st.markdown("Select or search for a person's name below to look up their site records instantly.")

# Safe validation check if file exists
if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")
    
    # Process text column formatting safely
    df['Name'] = df['Name'].fillna('Unknown').astype(str).str.strip()
    df['Plot'] = df['Plot'].fillna('-').astype(str).str.strip()
    
    # Process values accurately
    numeric_cols = ["2020-2021", "2022-2023", "2023-2024", "2024-2025", "2025-2026", "2026-2027", "Total"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Label assignment
    df['Select_Label'] = df['Name'] + " (Plot: " + df['Plot'] + ")"
    unique_options = sorted(df['Select_Label'].unique())

    selected_person = st.selectbox("🔍 Search or Select Person Name:", unique_options)

    if selected_person:
        selected_row = df[df['Select_Label'] == selected_person].iloc[0]
        
        st.subheader(f"👤 Record Details for: {selected_row['Name']}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="📍 Plot / Site No.", value=str(selected_row['Plot']))
        col2.metric(label="💰 Total Maintenance Paid", value=f"₹{int(selected_row['Total']):,}")
        col3.metric(label="📋 Status Ledger", value="Verified Record")
        
        years = ["2020-2021", "2022-2023", "2023-2024", "2024-2025", "2025-2026", "2026-2027"]
        amounts = [int(selected_row[yr]) for yr in years if yr in df.columns]
        
        breakdown_df = pd.DataFrame({"Financial Year": years[:len(amounts)], "Amount Paid (₹)": amounts})
        st.write("### 📅 Maintenance Payment Breakdown By Year")
        st.dataframe(breakdown_df, hide_index=True, use_container_width=True)

    with st.expander("🗂️ View Full Master Registry Table"):
        st.dataframe(df.drop(columns=['Select_Label']), use_container_width=True, hide_index=True)
else:
    st.error("Error: 'data.csv' file not found in your repository path. Please create it.")
