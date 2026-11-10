import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
from datetime import datetime

# Add database and styles directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'styles'))

import db_helper
from theme import (
    CUSTOM_CSS, BIORON_GREEN, BIORON_BROWN, BIORON_OLIVE, 
    BIORON_DARK, render_metric_card
)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Bioron Solutions | Operations & Work Portal",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Logo path
LOGO_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'bioron_logo.jpg')


# =============================================================================
# AUTHENTICATION SCREEN
# =============================================================================
def render_login_screen():
    col_spacer1, col_center, col_spacer2 = st.columns([1, 1.8, 1])
    
    with col_center:
        st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=320)
        else:
            st.markdown("<h1 style='color: #3B7A2F;'>BIORON SOLUTIONS</h1>", unsafe_allow_html=True)
            
        st.markdown("""
            <h2 style='color: #1E291E; margin-top: 10px; font-size: 24px;'>Executive Operations & Team Work Portal</h2>
            <p style='color: #64748B; font-size: 14px;'>GreenBuild Composite Facility — Naubatpur, Patna, Bihar</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='login-container'>", unsafe_allow_html=True)
            st.markdown("<span class='login-role-pill'>🔒 Secure Portal Access</span>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-bottom: 20px; font-size: 18px;'>Sign In to Your Workspace</h3>", unsafe_allow_html=True)

            login_mode = st.radio(
                "Choose Login Method:",
                ["Quick Executive Select", "Manual Email & Password"],
                horizontal=True,
                label_visibility="collapsed"
            )

            if login_mode == "Quick Executive Select":
                user_profiles = [
                    ("Admin (Master Control)", "bioronsolutions@gmail.com", "adminpassword123"),
                    ("Sudip Roy (CEO)", "sudroy809@gmail.com", "bioronceo2026"),
                    ("Raman Vishwakarma (CTO)", "Raman.vishwa1581@gmail.com", "bioroncto2026"),
                    ("Shashank Srivastav (COO)", "shashanksrivastav954@gmail.com", "bioroncoo2026"),
                ]
                
                selected_profile = st.selectbox(
                    "Select Team Profile:",
                    options=user_profiles,
                    format_func=lambda x: f"{x[0]} — {x[1]}"
                )
                
                entered_secret = st.text_input(
                    "Password or PIN (Default PIN: 1234):",
                    value=selected_profile[2],
                    type="password"
                )
                
                if st.button("Log In to Portal", use_container_width=True):
                    auth_result = db_helper.authenticate_user(selected_profile[1], entered_secret)
                    if auth_result:
                        st.session_state.authenticated = True
                        st.session_state.current_user = auth_result
                        st.success(f"Welcome back, {auth_result['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please verify password or PIN.")
            else:
                user_email = st.text_input("Work Email:", placeholder="e.g. sudroy809@gmail.com")
                user_pass = st.text_input("Password or PIN:", type="password", placeholder="Enter your password")
                
                if st.button("Sign In", use_container_width=True):
                    if user_email and user_pass:
                        auth_result = db_helper.authenticate_user(user_email, user_pass)
                        if auth_result:
                            st.session_state.authenticated = True
                            st.session_state.current_user = auth_result
                            st.success(f"Welcome back, {auth_result['name']}!")
                            st.rerun()
                        else:
                            st.error("Authentication failed. Please check your email and password.")
                    else:
                        st.warning("Please fill in both Email and Password.")

            st.markdown("</div>", unsafe_allow_html=True)
            
            # Credentials reference guide for team members
            with st.expander("ℹ️ Team Credentials Reference"):
                st.markdown("""
                | Role | Name | Email | Default Password | Default PIN |
                | :--- | :--- | :--- | :--- | :--- |
                | **Admin** | System Administrator | `bioronsolutions@gmail.com` | `adminpassword123` | `1234` |
                | **CEO** | Sudip Roy | `sudroy809@gmail.com` | `bioronceo2026` | `1234` |
                | **CTO** | Raman Vishwakarma | `Raman.vishwa1581@gmail.com` | `bioroncto2026` | `1234` |
                | **COO** | Shashank Srivastav | `shashanksrivastav954@gmail.com` | `bioroncoo2026` | `1234` |
                """)


# =============================================================================
# TOP HEADER BAR
# =============================================================================
def render_header():
    user = st.session_state.current_user
    role_color = {
        "Admin": "role-badge-admin",
        "CEO": "role-badge-ceo",
        "CTO": "role-badge-cto",
        "COO": "role-badge-coo"
    }.get(user.get("role", ""), "role-badge-ceo")

    col_title, col_user = st.columns([3, 1.2])
    with col_title:
        st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 15px;'>
            <div>
                <h2 style='margin: 0; font-size: 22px; color: #1E291E;'>Bioron Solutions Private Limited</h2>
                <p style='margin: 0; font-size: 13px; color: #64748B;'>GreenBuild Composite Manufacturing Hub • Naubatpur, Patna</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_user:
        st.markdown(f"""
        <div style='text-align: right;'>
            <span class='{role_color}' style='font-size: 12px;'>{user.get('role', 'Executive')}</span>
            <span style='font-size: 14px; font-weight: 700; color: #1E291E; margin-left: 6px;'>{user.get('name', 'User')}</span>
            <div style='font-size: 11px; color: #64748B;'>{user.get('email', '')}</div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# MODULE 1: OPERATIONS DASHBOARD
# =============================================================================
def render_operations_dashboard():
    st.markdown("### 📊 Executive Operations & Performance Dashboard")
    st.caption("Strategic metrics, plant commissioning status, pre-orders pipeline, and 5-year financials")

    # High-level Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(render_metric_card("Total Pre-Orders Pipeline", "₹1.30 Cr", "4 Strategic Key Accounts", "green"), unsafe_allow_html=True)
    with m2:
        st.markdown(render_metric_card("Phase 1 Production Target", "30,000 sq ft/mo", "Ramping to 1.2L sq ft in Phase 2", "olive"), unsafe_allow_html=True)
    with m3:
        st.markdown(render_metric_card("Total Project Capex", "₹87.03 Lakh", "₹77.71L SIDBI / Bank + ₹9.32L Promoter", "brown"), unsafe_allow_html=True)
    with m4:
        st.markdown(render_metric_card("GreenBuild Unit Margin", "₹8 / sq ft (35%)", "Price: ₹23/sq ft vs COGS: ₹15/sq ft", "green"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Secondary Metrics Row
    sm1, sm2, sm3, sm4 = st.columns(4)
    with sm1:
        st.markdown(render_metric_card("Thermal Energy Reduction", ">75% Saved", "<200°C curing vs 1,200°C kiln", "green"), unsafe_allow_html=True)
    with sm2:
        st.markdown(render_metric_card("Structural Benchmark", "M30 / M40", "Tested 34.2 – 41.8 MPa", "olive"), unsafe_allow_html=True)
    with sm3:
        st.markdown(render_metric_card("Water Absorption", "< 0.74%", "Impermeable (<1% Target)", "brown"), unsafe_allow_html=True)
    with sm4:
        st.markdown(render_metric_card("Cash Break-Even Buffer", "4.7x Cushion", "21,250 sq ft/mo operating BEP", "green"), unsafe_allow_html=True)

    st.markdown("---")

    # Charts Row 1: Financial Projections & Pre-Orders Pipeline
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown("#### 📈 5-Year Financial & EBITDA Trajectory (DPR Model)")
        fin_df = db_helper.get_financial_projections()
        if not fin_df.empty:
            fig_fin = go.Figure()
            fig_fin.add_trace(go.Bar(
                x=fin_df['fiscal_year'],
                y=fin_df['revenue_lakh'],
                name="Gross Revenue (₹ Lakh)",
                marker_color=BIORON_GREEN
            ))
            fig_fin.add_trace(go.Scatter(
                x=fin_df['fiscal_year'],
                y=fin_df['ebitda_lakh'],
                name="EBITDA (₹ Lakh)",
                line=dict(color=BIORON_BROWN, width=3),
                mode='lines+markers'
            ))
            fig_fin.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(title="Fiscal Year"),
                yaxis=dict(title="₹ Lakhs")
            )
            st.plotly_chart(fig_fin, use_container_width=True)
        else:
            st.info("No financial projection data found.")

    with c2:
        st.markdown("#### 🤝 Strategic Pre-Orders Pipeline")
        sales_df = db_helper.get_sales_pipeline()
        if not sales_df.empty:
            fig_sales = px.pie(
                sales_df,
                names='client_name',
                values='total_value',
                hole=0.45,
                color_discrete_sequence=[BIORON_GREEN, BIORON_BROWN, BIORON_OLIVE, "#0284C7"]
            )
            fig_sales.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=30, b=10),
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1)
            )
            st.plotly_chart(fig_sales, use_container_width=True)
        else:
            st.info("No sales pipeline data found.")

    # Charts Row 2: Feedstock Composition & Capital Structure
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### ♻️ GreenBuild Feedstock Formulation Ratio")
        feedstock_data = {
            "Material": ["Industrial Fly Ash / C&D Debris", "Recovered Polymers & Post-Consumer Plastics", "Agricultural Residues & Stubble", "Resins & Mineral Binders"],
            "Share (%)": [40, 35, 20, 5]
        }
        fig_feed = px.bar(
            feedstock_data,
            x="Share (%)",
            y="Material",
            orientation="h",
            text="Share (%)",
            color="Material",
            color_discrete_sequence=[BIORON_GREEN, BIORON_BROWN, BIORON_OLIVE, "#94A3B8"]
        )
        fig_feed.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_feed, use_container_width=True)

    with c4:
        st.markdown("#### 🏦 Capital Financing Distribution (₹87.03 Lakh Total)")
        capex_data = {
            "Source": ["SIDBI Term Loan (Machinery)", "SIDBI Working Capital (90-Day)", "Promoter Infrastructure Prep", "Promoter 5% Equity Margin"],
            "Amount (₹ Lakh)": [69.40, 8.31, 4.97, 4.35]
        }
        fig_capex = px.pie(
            capex_data,
            names="Source",
            values="Amount (₹ Lakh)",
            hole=0.4,
            color_discrete_sequence=[BIORON_GREEN, BIORON_OLIVE, BIORON_BROWN, "#D97706"]
        )
        fig_capex.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_capex, use_container_width=True)


# =============================================================================
# MODULE 2: CRM & LEAD PIPELINE
# =============================================================================
def render_crm():
    st.markdown("### 📇 Customer Relationship Management (CRM) & Leads")
    st.caption("Centralized repository of all 239+ ecosystem connections, institutional leads, municipal ULBs, and strategic partners")

    # Fetch contacts
    contacts_df = db_helper.get_crm_contacts()

    # Top KPI Metrics for CRM
    total_contacts = len(contacts_df)
    qualified_count = len(contacts_df[contacts_df['stage'] == 'Qualified'])
    contacted_count = len(contacts_df[contacts_df['stage'] == 'Contacted'])
    new_count = len(contacts_df[contacts_df['stage'] == 'New'])

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(render_metric_card("Total Contacts", f"{total_contacts}", "All Ecosystem Accounts", "green"), unsafe_allow_html=True)
    with k2:
        st.markdown(render_metric_card("Qualified / Hot", f"{qualified_count}", "High-Potential Leads", "olive"), unsafe_allow_html=True)
    with k3:
        st.markdown(render_metric_card("Contacted / Engaged", f"{contacted_count}", "Active Discussions", "brown"), unsafe_allow_html=True)
    with k4:
        st.markdown(render_metric_card("New Leads", f"{new_count}", "Awaiting Outreach", "green"), unsafe_allow_html=True)

    st.markdown("---")

    # Action Toolbar: Search, Filters & Add Contact
    col_search, col_stage, col_cat, col_btn = st.columns([2, 1.2, 1.5, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Search Contacts:", placeholder="Search by name, organization, phone, or notes...")
    
    with col_stage:
        stages = ["All"] + sorted(list(contacts_df['stage'].dropna().unique()))
        selected_stage = st.selectbox("Stage Filter:", stages)
        
    with col_cat:
        categories = ["All"] + sorted(list(contacts_df['category'].dropna().unique()))
        selected_category = st.selectbox("Category Filter:", categories)
        
    with col_btn:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        show_add_modal = st.button("➕ Add Contact", use_container_width=True)

    # Add Contact Expander
    if show_add_modal:
        st.session_state.show_add_contact_form = not st.session_state.get("show_add_contact_form", False)

    if st.session_state.get("show_add_contact_form", False):
        with st.form("new_contact_form", clear_on_submit=True):
            st.markdown("#### ➕ Add New CRM Lead / Contact")
            fc1, fc2 = st.columns(2)
            with fc1:
                new_name = st.text_input("Contact Name *")
                new_org = st.text_input("Organization / Company")
                new_phone = st.text_input("Phone Number")
                new_email = st.text_input("Email Address")
            with fc2:
                new_category = st.selectbox("Category", [
                    "Connection / Network", "Incubator / Accelerator", 
                    "Resource / Advisor / Process", "Govt Connect", 
                    "Key Contact", "Customer / Pre-Order", "Supplier / Waste Aggregator"
                ])
                new_stage = st.selectbox("Initial Stage", [
                    "New", "Contacted", "Qualified", "In Discussion", "Proposal Sent", "Won / Partnered", "Inactive"
                ])
                new_value = st.number_input("Estimated Value (₹ INR)", min_value=0.0, step=10000.0)
                new_assigned = st.selectbox("Assigned To", ["Sudip Roy", "Raman Vishwakarma", "Shashank Srivastav", "BSPL Team"])

            new_notes = st.text_area("Interaction Notes & Strategic Context")

            submitted = st.form_submit_button("Save Contact to Database")
            if submitted:
                if new_name.strip():
                    new_id = db_helper.add_crm_contact(
                        name=new_name.strip(),
                        category=new_category,
                        organization=new_org.strip(),
                        phone=new_phone.strip(),
                        email=new_email.strip(),
                        stage=new_stage,
                        notes=new_notes.strip(),
                        lead_value=new_value,
                        assigned_to=new_assigned,
                        updated_by=st.session_state.current_user["name"]
                    )
                    st.success(f"Contact '{new_name}' added successfully! (ID: {new_id})")
                    st.session_state.show_add_contact_form = False
                    st.rerun()
                else:
                    st.error("Contact name is required.")

    # Filtered Contacts Table
    filtered_df = db_helper.get_crm_contacts(
        search_term=search_query,
        stage_filter=selected_stage,
        category_filter=selected_category
    )

    st.markdown(f"**Showing {len(filtered_df)} of {total_contacts} Contacts**")

    # Display contacts dataframe with interactive features
    display_cols = ['id', 'name', 'category', 'organization', 'phone', 'email', 'stage', 'notes', 'assigned_to']
    st.dataframe(
        filtered_df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", width="small"),
            "name": st.column_config.TextColumn("Contact Name", width="medium"),
            "category": st.column_config.TextColumn("Category", width="medium"),
            "organization": st.column_config.TextColumn("Organization", width="medium"),
            "phone": st.column_config.TextColumn("Phone", width="small"),
            "email": st.column_config.TextColumn("Email", width="medium"),
            "stage": st.column_config.SelectboxColumn(
                "Stage",
                options=["New", "Contacted", "Qualified", "In Discussion", "Proposal Sent", "Won / Partnered", "Inactive"],
                width="small"
            ),
            "notes": st.column_config.TextColumn("Notes", width="large")
        }
    )

    # Quick Edit / Interaction logger
    with st.expander("✏️ Update Contact Stage or Log Interaction"):
        ue_col1, ue_col2 = st.columns([1, 2])
        with ue_col1:
            contact_options = filtered_df[['id', 'name', 'organization']].to_dict('records')
            if contact_options:
                target_contact = st.selectbox(
                    "Select Contact to Update:",
                    options=contact_options,
                    format_func=lambda x: f"ID #{x['id']}: {x['name']} ({x.get('organization', '')})"
                )
                
                updated_stage = st.selectbox(
                    "Update Stage:",
                    ["Contacted", "Qualified", "In Discussion", "Proposal Sent", "Won / Partnered", "Inactive"],
                    index=0
                )
        
        with ue_col2:
            if contact_options:
                additional_note = st.text_area("Add Interaction Notes / Update:", placeholder="Logged meeting notes, follow-up actions...")
                if st.button("Apply Contact Update"):
                    current_notes = filtered_df[filtered_df['id'] == target_contact['id']]['notes'].values[0] or ""
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    new_full_notes = f"{current_notes}\n[{timestamp} by {st.session_state.current_user['name']}]: {additional_note}".strip()
                    
                    db_helper.update_crm_contact(
                        target_contact['id'],
                        stage=updated_stage,
                        notes=new_full_notes,
                        updated_by=st.session_state.current_user['name']
                    )
                    st.success(f"Contact #{target_contact['id']} successfully updated!")
                    st.rerun()

    # CSV Export Button
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered CRM Contacts (CSV)",
        data=csv_bytes,
        file_name=f"bioron_crm_contacts_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )


# =============================================================================
# MODULE 3: PROJECT & TASK TRACKER (KANBAN BOARD)
# =============================================================================
def render_task_tracker():
    st.markdown("### 📋 Project & Task Tracker — Interactive Kanban Board")
    st.caption("Track site readiness, machinery procurement, SIDBI financing milestones, and operational deliverables")

    # Fetch tasks
    all_tasks = db_helper.get_work_tasks()

    # Filter Row
    f1, f2, f3, f4 = st.columns([1.5, 1.5, 1.5, 1.2])
    with f1:
        assignees = ["All"] + sorted(list(all_tasks['assigned_to_name'].dropna().unique()))
        sel_assignee = st.selectbox("Filter Assignee:", assignees)
    with f2:
        depts = ["All"] + sorted(list(all_tasks['department'].dropna().unique()))
        sel_dept = st.selectbox("Filter Department:", depts)
    with f3:
        priorities = ["All", "P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"]
        sel_priority = st.selectbox("Filter Priority:", priorities)
    with f4:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        open_task_modal = st.button("➕ New Task", use_container_width=True)

    # Create New Task Form
    if open_task_modal:
        st.session_state.show_create_task = not st.session_state.get("show_create_task", False)

    if st.session_state.get("show_create_task", False):
        with st.form("create_task_form", clear_on_submit=True):
            st.markdown("#### ➕ Create New Operational Task")
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                t_title = st.text_input("Task Title *", placeholder="e.g. Electrical earthing & generator installation")
                t_dept = st.selectbox("Department", ["Plant Operations", "BSPL Board", "Sales", "Marketing", "R&D", "Accounts"])
                t_cat = st.selectbox("Category", [
                    "Plant Setup & Civil Works", "Machinery & Procurement", 
                    "Raw Material & Sourcing", "R&D & Formulations", 
                    "Production & QC", "Sales & B2B Pipeline", 
                    "SIDBI & Banking Finance", "Governance & Legal"
                ])
                t_assigned = st.selectbox("Assignee", ["Sudip Roy", "Raman Vishwakarma", "Shashank Srivastav", "Uttam Kumar", "Naubatpur Plant Operations Head"])
            with t_col2:
                t_priority = st.selectbox("Priority", ["P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"], index=1)
                t_status = st.selectbox("Initial Status", ["To Do", "In Progress", "Under Review", "Completed", "Blocked"])
                t_due = st.date_input("Target Due Date")
                t_prog = st.slider("Initial Progress %", 0, 100, 0)
                
            t_desc = st.text_area("Detailed Scope & Description")
            
            task_submitted = st.form_submit_button("Add Task to Kanban")
            if task_submitted:
                if t_title.strip():
                    new_t_id = db_helper.add_work_task(
                        title=t_title.strip(),
                        description=t_desc.strip(),
                        department=t_dept,
                        category=t_cat,
                        assigned_to_name=t_assigned,
                        priority=t_priority,
                        status=t_status,
                        due_date=str(t_due),
                        progress=t_prog,
                        created_by=st.session_state.current_user['email']
                    )
                    st.success(f"Task created successfully! (ID: {new_t_id})")
                    st.session_state.show_create_task = False
                    st.rerun()
                else:
                    st.error("Task title is required.")

    # Apply filters
    filtered_tasks = db_helper.get_work_tasks(
        assignee_filter=sel_assignee,
        department_filter=sel_dept,
        priority_filter=sel_priority
    )

    # View Mode Switcher
    view_mode = st.radio("Display Mode:", ["Kanban Board", "Table Register"], horizontal=True)

    if view_mode == "Kanban Board":
        kanban_columns = [
            ("To Do", "📋", "#64748B"),
            ("In Progress", "⚡", "#0284C7"),
            ("Under Review", "🔍", "#D97706"),
            ("Completed", "✅", "#16A34A"),
            ("Blocked", "⛔", "#DC2626")
        ]

        cols = st.columns(len(kanban_columns))

        for idx, (col_name, icon, header_color) in enumerate(kanban_columns):
            with cols[idx]:
                column_tasks = filtered_tasks[filtered_tasks['status'] == col_name]
                
                # Column Header
                st.markdown(f"""
                <div class='kanban-column'>
                    <div class='kanban-col-header' style='color: {header_color};'>
                        <span>{icon} {col_name}</span>
                        <span style='background: #E2E8F0; color: #1E291E; padding: 2px 8px; border-radius: 10px; font-size: 11px;'>{len(column_tasks)}</span>
                    </div>
                """, unsafe_allow_html=True)

                if column_tasks.empty:
                    st.markdown("<p style='font-size: 12px; color: #94A3B8; text-align: center; margin-top: 30px;'>No tasks in this stage</p>", unsafe_allow_html=True)
                else:
                    for _, task in column_tasks.iterrows():
                        p_badge = {
                            "P0 - Critical": "badge-p0",
                            "P1 - High": "badge-p1",
                            "P2 - Medium": "badge-p2",
                            "P3 - Low": "badge-p3"
                        }.get(task['priority'], "badge-p2")

                        st.markdown(f"""
                        <div class='kanban-card'>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;'>
                                <span style='font-size: 11px; font-weight: 800; color: #3B7A2F;'>{task['task_code']}</span>
                                <span class='kanban-badge {p_badge}'>{task['priority'].split(' ')[0]}</span>
                            </div>
                            <div class='kanban-card-title'>{task['title']}</div>
                            <div class='kanban-card-desc'>{task.get('description', '')[:95]}...</div>
                            <div style='display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 8px;'>
                                <span class='kanban-badge badge-dept'>{task.get('department', '')}</span>
                                <span class='kanban-badge badge-assignee'>👤 {task.get('assigned_to_name', '')}</span>
                            </div>
                            <div style='font-size: 11px; color: #64748B; margin-bottom: 4px;'>
                                📅 Due: <b>{task.get('due_date', 'N/A')}</b> | Progress: <b>{task.get('progress_percentage', 0)}%</b>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Card action controls inside a tight expander
                        with st.expander(f"⚙️ Move: {task['task_code']}"):
                            next_stage_options = ["To Do", "In Progress", "Under Review", "Completed", "Blocked"]
                            new_st = st.selectbox(
                                "Move to:",
                                next_stage_options,
                                index=next_stage_options.index(col_name),
                                key=f"sel_stage_{task['id']}"
                            )
                            if st.button("Update Stage", key=f"btn_move_{task['id']}"):
                                db_helper.update_task_status(task['id'], new_st)
                                st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.dataframe(
            filtered_tasks[['task_code', 'title', 'department', 'category', 'assigned_to_name', 'priority', 'status', 'progress_percentage', 'due_date']],
            use_container_width=True,
            hide_index=True
        )


# =============================================================================
# MODULE 4: MACHINERY & CAPITAL ASSETS
# =============================================================================
def render_machinery_assets():
    st.markdown("### ⚙️ Machinery & Fixed Assets Capital Register")
    st.caption("Complete 21 Capital Machines + 11 Infrastructure assets (₹74.37 Lakhs) from DPR Section 6")

    mach_df = db_helper.get_machinery_assets()
    if mach_df.empty:
        st.info("No machinery records found.")
        return

    # High-level asset totals
    total_assets = len(mach_df)
    total_capex_lakh = mach_df['total_cost_lakh'].sum()
    installed_count = len(mach_df[mach_df['status'].isin(['Installed', 'Operational'])])
    pending_count = len(mach_df[mach_df['status'] == 'To Be Purchased'])

    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.markdown(render_metric_card("Total Registered Assets", f"{total_assets}", "Machines & Civil Infra", "green"), unsafe_allow_html=True)
    with a2:
        st.markdown(render_metric_card("Total Asset Value", f"₹{total_capex_lakh:.2f} Lakh", "DPR Cost Basis", "brown"), unsafe_allow_html=True)
    with a3:
        st.markdown(render_metric_card("Installed / Operational", f"{installed_count}", "Commissioned at Site", "olive"), unsafe_allow_html=True)
    with a4:
        st.markdown(render_metric_card("Procurement Queue", f"{pending_count}", "Awaiting PO / Quotation", "green"), unsafe_allow_html=True)

    st.markdown("---")

    # Status Breakdown Chart
    c_m1, c_m2 = st.columns([1.2, 1])
    with c_m1:
        status_counts = mach_df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_mach = px.bar(
            status_counts,
            x='Status',
            y='Count',
            color='Status',
            color_discrete_sequence=[BIORON_GREEN, BIORON_OLIVE, BIORON_BROWN, "#D97706", "#64748B"]
        )
        fig_mach.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_mach, use_container_width=True)

    with c_m2:
        st.markdown("#### 📑 Asset Funding Source")
        funding_counts = mach_df.groupby('funding_source')['total_cost_lakh'].sum().reset_index()
        fig_fund = px.pie(
            funding_counts,
            names='funding_source',
            values='total_cost_lakh',
            hole=0.45,
            color_discrete_sequence=[BIORON_GREEN, BIORON_BROWN, BIORON_OLIVE]
        )
        fig_fund.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fund, use_container_width=True)

    # Interactive Assets Table
    st.markdown("#### 📋 Capital Asset Inventory Table")
    st.dataframe(
        mach_df[['asset_code', 'asset_name', 'category', 'quantity', 'unit_cost_lakh', 'total_cost_lakh', 'funding_source', 'status', 'vendor_supplier']],
        use_container_width=True,
        hide_index=True
    )


# =============================================================================
# MODULE 5: DATABASE STUDIO & DATA CONTROL (USER ACCESS)
# =============================================================================
def render_database_studio():
    st.markdown("### 💾 Database Studio & Data Control Center")
    st.caption("Direct, unrestricted access to inspect, query, export, and backup the SQLite database (`bioron_operations.db`)")

    # Informational notice
    st.info("💡 You have full master control of the underlying SQLite database. You can inspect all 15 operational tables, run custom SQL queries, export data to CSV/Excel, and download full database backups.")

    tab_explore, tab_sql, tab_backup = st.tabs(["🗄️ Table Explorer", "⚡ SQL Query Runner", "📦 Backup & Export"])

    with tab_explore:
        tables = db_helper.get_all_tables()
        col_t1, col_t2 = st.columns([1.5, 1])
        with col_t1:
            selected_table = st.selectbox("Select Database Table to Inspect:", tables, index=tables.index('crm_contacts') if 'crm_contacts' in tables else 0)
        with col_t2:
            row_limit = st.selectbox("Max Rows to Load:", [50, 100, 250, 500, 1000, 5000], index=3)

        if selected_table:
            table_df = db_helper.get_table_data(selected_table, limit=row_limit)
            st.markdown(f"**Table: `{selected_table}` | Rows Loaded: {len(table_df)} | Total Columns: {len(table_df.columns)}**")
            
            # Search filter within table
            search_table = st.text_input(f"Filter records in `{selected_table}`:", placeholder="Type any text to filter rows...")
            if search_table:
                mask = table_df.astype(str).apply(lambda row: row.str.contains(search_table, case=False).any(), axis=1)
                display_df = table_df[mask]
            else:
                display_df = table_df
                
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Download table as CSV
            csv_data = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download `{selected_table}` as CSV",
                data=csv_data,
                file_name=f"{selected_table}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

    with tab_sql:
        st.markdown("#### ⚡ Execute Custom SQL Queries")
        st.caption("Execute standard SQL statements (`SELECT`, `PRAGMA`, etc.) directly on `bioron_operations.db`.")
        
        sample_queries = [
            "SELECT stage, COUNT(*) as total_contacts FROM crm_contacts GROUP BY stage;",
            "SELECT department, priority, COUNT(*) FROM work_portal_tasks GROUP BY department, priority;",
            "SELECT category, SUM(total_cost_lakh) as total_lakh FROM machinery_assets GROUP BY category;",
            "SELECT name, role, gmail_address, access_level FROM team_members;",
            "SELECT client_name, product_line, total_value, stage FROM sales_pipeline_orders;"
        ]
        
        chosen_sample = st.selectbox("Or choose a pre-built executive query:", ["-- Custom Query --"] + sample_queries)
        
        default_query = chosen_sample if chosen_sample != "-- Custom Query --" else "SELECT * FROM crm_contacts LIMIT 10;"
        sql_input = st.text_area("SQL Statement:", value=default_query, height=120)
        
        if st.button("Run SQL Query", type="primary"):
            if sql_input.strip():
                try:
                    res_df, msg = db_helper.execute_custom_sql(sql_input)
                    st.success(msg)
                    if res_df is not None:
                        st.dataframe(res_df, use_container_width=True, hide_index=True)
                        st.caption(f"Returned {len(res_df)} rows")
                except Exception as e:
                    st.error(f"SQL Execution Error: {str(e)}")
            else:
                st.warning("Please enter a SQL query.")

    with tab_backup:
        st.markdown("#### 📦 SQLite Database Backup & Connection Info")
        st.markdown(f"""
        - **Local Database Path**: `{db_helper.DB_PATH}`
        - **File Size**: `{os.path.getsize(db_helper.DB_PATH) / 1024:.1f} KB`
        - **Supported External Tools**: You can open this database with **DB Browser for SQLite**, **DBeaver**, or **VS Code SQLite Viewer**.
        """)
        
        db_bytes = db_helper.get_database_file_bytes()
        st.download_button(
            label="💾 Download Full SQLite Database Snapshot (`.db`)",
            data=db_bytes,
            file_name=f"bioron_operations_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.db",
            mime="application/x-sqlite3",
            help="Download a snapshot of the raw SQLite database for offline analysis or safe keeping."
        )


# =============================================================================
# MODULE 6: TEAM & PROFILE SETTINGS
# =============================================================================
def render_team_settings():
    st.markdown("### 👤 Team Profiles & Security Settings")
    st.caption("Manage team roles, credentials, access levels, and security settings")

    user = st.session_state.current_user

    c_prof1, c_prof2 = st.columns(2)
    with c_prof1:
        st.markdown("#### 🏷️ Current Active Session")
        st.markdown(f"""
        - **Name**: **{user['name']}**
        - **Role**: `{user['role']}` ({user['designation']})
        - **Work Email**: `{user['email']}`
        - **Department**: `{user.get('department', 'BSPL Board')}`
        - **Access Level**: `{user['access_level']}`
        """)

        with st.form("change_credentials_form"):
            st.markdown("##### 🔐 Update Your Password / PIN")
            new_pw = st.text_input("New Password", type="password")
            new_pin = st.text_input("New 4-digit PIN", max_chars=4, type="password")
            
            pw_submitted = st.form_submit_button("Save New Credentials")
            if pw_submitted:
                if new_pw or new_pin:
                    db_helper.update_user_credentials(user['id'], new_pw if new_pw else None, new_pin if new_pin else None)
                    st.success("Credentials updated successfully!")
                else:
                    st.warning("Please provide a new password or PIN.")

    with c_prof2:
        st.markdown("#### 👥 Active BSPL Team Roster")
        team_df = db_helper.get_all_team_members()
        st.dataframe(
            team_df[['name', 'role', 'designation', 'gmail_address', 'access_level', 'department']],
            use_container_width=True,
            hide_index=True
        )


# =============================================================================
# MAIN APP ROUTER
# =============================================================================
def main():
    if not st.session_state.authenticated or st.session_state.current_user is None:
        render_login_screen()
        return

    # Render Top Header
    render_header()
    st.markdown("---")

    # Sidebar Navigation
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
            
        st.markdown("### 🧭 Portal Navigation")
        selected_module = st.radio(
            "Go to Module:",
            [
                "📊 Operations Dashboard",
                "📇 CRM & Leads Pipeline",
                "📋 Task Tracker & Kanban",
                "⚙️ Machinery & Assets",
                "💾 Database Studio & Control",
                "👤 Team & Profile Settings"
            ]
        )

        st.markdown("---")
        st.markdown("#### 🏭 Facility Quick Stats")
        st.markdown("""
        - **Location**: Korra, Naubatpur
        - **Plot**: 7,000 sq ft
        - **Curing Platen**: <200°C
        - **M30/M40 Standard**: PASSED
        """)

        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()

    # Route to selected module
    if selected_module == "📊 Operations Dashboard":
        render_operations_dashboard()
    elif selected_module == "📇 CRM & Leads Pipeline":
        render_crm()
    elif selected_module == "📋 Task Tracker & Kanban":
        render_task_tracker()
    elif selected_module == "⚙️ Machinery & Assets":
        render_machinery_assets()
    elif selected_module == "💾 Database Studio & Control":
        render_database_studio()
    elif selected_module == "👤 Team & Profile Settings":
        render_team_settings()

if __name__ == '__main__':
    main()
