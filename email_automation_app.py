import streamlit as st
from datetime import datetime
import json
import os
import urllib.parse

st.set_page_config(page_title="Dynamic Email Generator", layout="wide")
st.title("✉️ Smart Email Template & Recipient Automation Engine")
st.write("Configure projects, manage sticky distribution groups, and compile time-sensitive reporting emails dynamically.")

DB_FILE = "projects.json"

# Helper function to load data from the JSON file
def load_project_database():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    # Default initial data if the file doesn't exist yet
    return {
        "Project Alpha": {
            "to": ["alpha.lead@company.com", "alpha.pm@company.com"],
            "cc": ["director.operations@company.com"],
            "bcc": ["archive.audit@company.com"]
        },
        "Project Beta": {
            "to": ["beta.team@company.com"],
            "cc": ["vp.engineering@company.com", "finance.track@company.com"],
            "bcc": []
        }
    }

# Helper function to save data to the JSON file
def save_project_database(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load the database into session state once upon startup
if 'project_database' not in st.session_state:
    st.session_state.project_database = load_project_database()

# 2. INTERFACE LAYOUT: CONFIGURATION VS OUTPUT
col_config, col_output = st.columns([1, 1.2])

with col_config:
    st.subheader("⚙️ Parameter Matrix")
    
    # Project Picker & Addition Zone
    available_projects = list(st.session_state.project_database.keys())
    selected_project = st.selectbox("Select Project Matrix:", available_projects)
    
    with st.expander("➕ Add New Project Profile"):
        new_proj_name = st.text_input("New Project Name:", key="new_proj_input")
        if st.button("Save New Project") and new_proj_name:
            clean_name = new_proj_name.strip()
            if clean_name and clean_name not in st.session_state.project_database:
                st.session_state.project_database[clean_name] = {"to": [], "cc": [], "bcc": []}
                save_project_database(st.session_state.project_database)
                st.success(f"Project '{clean_name}' saved permanently to file!")
                st.rerun()

    # Time & Report Frequency Drivers
    report_type = st.selectbox(
        "Reporting Frequency Interval:",
        ["Monthly Review Report", "Quarterly Report", "Half-Yearly Report", "Annual Report"]
    )
    
    current_month = datetime.now().strftime("%B")
    months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("Reporting Target Month:", months_list, index=months_list.index(current_month))
    selected_year = st.selectbox("Reporting Target Year:", [2025, 2026, 2027], index=1) # Defaults to 2026

    st.markdown("---")
    st.subheader("👥 Dynamic Distribution Lists")
    st.caption(f"Editing records locked to: **{selected_project}**")
    
    proj_data = st.session_state.project_database[selected_project]
    
    to_input = st.text_area("TO Recipients (Comma Separated):", value=", ".join(proj_data["to"]), key="to_area")
    cc_input = st.text_area("CC Recipients (Comma Separated):", value=", ".join(proj_data["cc"]), key="cc_area")
    bcc_input = st.text_area("BCC Recipients (Comma Separated):", value=", ".join(proj_data["bcc"]), key="bcc_area")
    
    # Save edits back to state AND write to JSON file
    if st.button("💾 Save Changes to Distribution List"):
        st.session_state.project_database[selected_project]["to"] = [e.strip() for e in to_input.split(",") if e.strip()]
        st.session_state.project_database[selected_project]["cc"] = [e.strip() for e in cc_input.split(",") if e.strip()]
        st.session_state.project_database[selected_project]["bcc"] = [e.strip() for e in bcc_input.split(",") if e.strip()]
        
        save_project_database(st.session_state.project_database)
        st.success(f"Changes saved permanently for {selected_project}!")
        st.rerun()

# 3. DYNAMIC TEMPLATE RENDERING ENGINE
with col_output:
    st.subheader("📄 Generated Mail Composition Output")
    
    subject_line = f"[{selected_project}] - {report_type} | {selected_month} {selected_year}"
    
    if report_type == "Monthly Review Report":
        body_template = f"Hi Team,\n\nPlease find attached the performance metrics and milestone updates for {selected_project} covering the operational window of {selected_month} {selected_year}.\n\nKey focuses for this review session:\n- Core deliverables status for {selected_month}\n- Budget burn rate tracking\n- Next steps scheduled for the upcoming month\n\nBest regards,"
    elif report_type == "Quarterly Report":
        body_template = f"Dear Stakeholders,\n\nWe have finalized the operational evaluation parameters for {selected_project}. This dynamic data bundle reflects our cumulative metrics finalized around the {selected_month} evaluation mark.\n\nPlease review the attached sheets detailing financial variance reports and system deployment speeds.\n\nRegards,"
    elif report_type == "Half-Yearly Report":
        body_template = f"Executive Team,\n\nEnclosed is the comprehensive Mid-Year strategic tracking summary data for {selected_project}, synthesized through {selected_month} {selected_year}.\n\nThis high-level presentation covers strategic realignments, execution risks mitigated, and project health overviews.\n\nSincerely,"
    else:
        body_template = f"All Hands,\n\nIt is our privilege to broadcast the comprehensive Annual Operational and Financial Closures documentation for {selected_project} tracking back through our milestone evaluations in {selected_year}.\n\nThank you for your continued dedication to tracking this initiative across all metrics.\n\nWarm regards,"

    # Output Interactive Widgets
    final_subject = st.text_input("📋 Subject Line:", value=subject_line, key="out_subject")
    final_to = st.text_input("👤 To:", value=", ".join(st.session_state.project_database[selected_project]["to"]), key="out_to")
    final_cc = st.text_input("👥 Cc:", value=", ".join(st.session_state.project_database[selected_project]["cc"]), key="out_cc")
    final_bcc = st.text_input("🕵️ Bcc:", value=", ".join(st.session_state.project_database[selected_project]["bcc"]), key="out_bcc")
    final_body = st.text_area("📝 Email Body Copy:", value=body_template, height=250, key="out_body")
    
    # URL Encoding strings for the mailto trigger
    to_str = ",".join(st.session_state.project_database[selected_project]["to"])
    cc_str = ",".join(st.session_state.project_database[selected_project]["cc"])
    bcc_str = ",".join(st.session_state.project_database[selected_project]["bcc"])
    
    encoded_subject = urllib.parse.quote(final_subject)
    encoded_body = urllib.parse.quote(final_body)
    
    mailto_url = f"mailto:{to_str}?cc={cc_str}&bcc={bcc_str}&subject={encoded_subject}&body={encoded_body}"
    
    st.markdown("---")
    # Clean Action Button launcher linked straight to desktop mail clients
    st.markdown(
        f'<a href="{mailto_url}" target="_blank" style="text-decoration:none;">'
        '<button style="background-color:#4CAF50; color:white; padding:12px 24px; '
        'border:none; border-radius:4px; cursor:pointer; font-size:16px; width:100%; font-weight:bold;">'
        '🚀 Open in Outlook / Mail Client</button></a>', 
        unsafe_allow_html=True
    )
