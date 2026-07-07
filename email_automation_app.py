import streamlit as st
from datetime import datetime
import json
import os
import urllib.parse

# 1. SET PAGE THEME, VIBRANT TAB TITLE, AND EMOTICON FAVICON
st.set_page_config(
    page_title="MailCraft Pro | Template Automation", 
    page_icon="🎨", 
    layout="wide"
)

# 2. INJECT VIBRANT MODERN UI STYLE CODES (CSS Customization)
st.markdown("""
    <style>
    /* Gradient line effect at the top of the app */
    .stAppHeader {
        border-top: 6px solid transparent;
        background-image: linear-gradient(to right, #FF4B4B, #FF8F00, #4A00E0);
        background-size: 100% 6px;
        background-repeat: no-repeat;
    }
    
    /* Make input text areas and input blocks rounded and sleek */
    div.stTextArea textarea, div.stTextInput input, div.stSelectbox div {
        border-radius: 10px !important;
        border: 1px solid #E0E0E0 !important;
        transition: all 0.3s ease;
    }
    
    /* Give input blocks a nice color highlight on click/focus */
    div.stTextArea textarea:focus, div.stTextInput input:focus {
        border-color: #4A00E0 !important;
        box-shadow: 0 0 8px rgba(74, 0, 224, 0.2) !important;
    }
    
    /* Styling for expander bars */
    div.団.st-emotion-cache-1h996g3 {
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. SILHOUETTE HEADER CONTAINER WITH EMOTICON GRAPHICS
st.markdown("""
    <div style="display: flex; align-items: center; background-color: #F8F9FA; padding: 20px; border-radius: 12px; border-left: 5px solid #4A00E0; margin-bottom: 25px;">
        <div style="font-size: 42px; margin-right: 20px; color: #4A00E0;">📬</div>
        <div>
            <h2 style="margin: 0; padding: 0; color: #1E1E24; font-family: 'Inter', sans-serif;">Smart Email Template & Recipient Automation Engine</h2>
            <p style="margin: 5px 0 0 0; color: #5F6368; font-size: 14px;">Configure projects, manage sticky distribution groups, and compile time-sensitive reporting emails dynamically.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

DB_FILE = "projects.json"

# Helper function to load data from the JSON file
def load_project_database():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
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

if 'project_database' not in st.session_state:
    st.session_state.project_database = load_project_database()

# 4. INTERFACE LAYOUT: CONFIGURATION VS OUTPUT
col_config, col_output = st.columns([1, 1.2], gap="large")

with col_config:
    st.markdown("<h3 style='color: #4A00E0;'>⚙️ Parameter Matrix</h3>", unsafe_allow_html=True)
    
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

    report_type = st.selectbox(
        "Reporting Frequency Interval:",
        ["Monthly Review Report", "Quarterly Report", "Half-Yearly Report", "Annual Report"]
    )
    
    current_month = datetime.now().strftime("%B")
    months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("Reporting Target Month:", months_list, index=months_list.index(current_month))
    selected_year = st.selectbox("Reporting Target Year:", [2025, 2026, 2027], index=1)

    st.markdown("---")
    st.markdown(f"<h3 style='color: #FF8F00;'>👥 Distribution Lists</h3>", unsafe_allow_html=True)
    st.caption(f"Editing records locked to: **{selected_project}**")
    
    proj_data = st.session_state.project_database[selected_project]
    
    to_input = st.text_area("TO Recipients (Comma Separated):", value=", ".join(proj_data["to"]), key=f"to_area_{selected_project}")
    cc_input = st.text_area("CC Recipients (Comma Separated):", value=", ".join(proj_data["cc"]), key=f"cc_area_{selected_project}")
    bcc_input = st.text_area("BCC Recipients (Comma Separated):", value=", ".join(proj_data["bcc"]), key=f"bcc_area_{selected_project}")
    
    if st.button("💾 Save Changes to Distribution List"):
        st.session_state.project_database[selected_project]["to"] = [e.strip() for e in to_input.split(",") if e.strip()]
        st.session_state.project_database[selected_project]["cc"] = [e.strip() for e in cc_input.split(",") if e.strip()]
        st.session_state.project_database[selected_project]["bcc"] = [e.strip() for e in bcc_input.split(",") if e.strip()]
        
        save_project_database(st.session_state.project_database)
        st.success(f"Changes saved permanently for {selected_project}!")
        st.rerun()

# 5. DYNAMIC TEMPLATE RENDERING ENGINE
with col_output:
    st.markdown("<h3 style='color: #FF4B4B;'>📄 Composition Preview</h3>", unsafe_allow_html=True)
    
    calculated_subject = f"[{selected_project}] - {report_type} | {selected_month} {selected_year}"
    
    if report_type == "Monthly Review Report":
        calculated_body = f"Hi Team,\n\nPlease find attached the performance metrics and milestone updates for {selected_project} covering the operational window of {selected_month} {selected_year}.\n\nKey focuses for this review session:\n- Core deliverables status for {selected_month}\n- Budget burn rate tracking\n- Next steps scheduled for the upcoming month\n\nBest regards,"
    elif report_type == "Quarterly Report":
        calculated_body = f"Dear Stakeholders,\n\nWe have finalized the operational evaluation parameters for {selected_project}. This dynamic data bundle reflects our cumulative metrics finalized around the {selected_month} evaluation mark.\n\nPlease review the attached sheets detailing financial variance reports and system deployment speeds.\n\nRegards,"
    elif report_type == "Half-Yearly Report":
        calculated_body = f"Executive Team,\n\nEnclosed is the comprehensive Mid-Year strategic tracking summary data for {selected_project}, synthesized through {selected_month} {selected_year}.\n\nThis high-level presentation covers strategic realignments, execution risks mitigated, and project health overviews.\n\nSincerely,"
    else:
        calculated_body = f"All Hands,\n\nIt is our privilege to broadcast the comprehensive Annual Operational and Financial Closures documentation for {selected_project} tracking back through our milestone evaluations in {year}.\n\nThank you for your continued dedication to tracking this initiative across all metrics.\n\nWarm regards,"

    state_fingerprint = f"{selected_project}_{report_type}_{selected_month}_{selected_year}"

    final_subject = st.text_input("📋 Subject Line:", value=calculated_subject, key=f"sub_{state_fingerprint}")
    final_to = st.text_input("👤 To:", value=", ".join(st.session_state.project_database[selected_project]["to"]), key=f"to_{state_fingerprint}")
    final_cc = st.text_input("👥 Cc:", value=", ".join(st.session_state.project_database[selected_project]["cc"]), key=f"cc_{state_fingerprint}")
    final_bcc = st.text_input("🕵️ Bcc:", value=", ".join(st.session_state.project_database[selected_project]["bcc"]), key=f"bcc_{state_fingerprint}")
    final_body = st.text_area("📝 Email Body Copy:", value=calculated_body, height=250, key=f"body_{state_fingerprint}")
    
    # URL Encoding extraction strings
    encoded_subject = urllib.parse.quote(final_subject)
    encoded_body = urllib.parse.quote(final_body)
    
    clean_to = urllib.parse.quote(final_to)
    clean_cc = urllib.parse.quote(final_cc)
    clean_bcc = urllib.parse.quote(final_bcc)
    
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={clean_to}&cc={clean_cc}&bcc={clean_bcc}&su={encoded_subject}&body={encoded_body}"
    
    st.markdown("---")
    
    # Custom modern button styling matching Google Material Design with rounded edges
    st.markdown(
        f'<a href="{gmail_url}" target="_blank" style="text-decoration:none;">'
        '<button style="background-image: linear-gradient(135deg, #EA4335 0%, #C5221F 100%); color:white; padding:14px 28px; '
        'border:none; border-radius:50px; cursor:pointer; font-size:16px; width:100%; font-weight:bold; '
        'box-shadow: 0 4px 15px rgba(234, 67, 53, 0.3); transition: all 0.3s ease;">'
        '🚀 Open Compose Window in Web Gmail</button></a>', 
        unsafe_allow_html=True
    )
