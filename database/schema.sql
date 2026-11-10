-- =============================================================================
-- BIORON SOLUTIONS PRIVATE LIMITED (BSPL)
-- Operational Database Schema & Enterprise Board Management System
-- Facility: Korra, Naubatpur, Patna, Bihar
-- =============================================================================

PRAGMA foreign_keys = ON;

-- 1. Company Information & Legal Registry
CREATE TABLE IF NOT EXISTS company_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    cin TEXT NOT NULL,
    pan TEXT NOT NULL,
    tan TEXT NOT NULL,
    dipp_number TEXT,
    udyam_reg_number TEXT,
    gst_wb TEXT,
    gst_bihar TEXT,
    registered_office TEXT,
    plant_location TEXT,
    site_area_sqft REAL DEFAULT 7000,
    workshed_sqft REAL DEFAULT 1000,
    roofing_shed_sqft REAL DEFAULT 2000,
    website TEXT,
    official_email TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Promoters & Key Team Personnel (With Auth & Department Affiliation)
CREATE TABLE IF NOT EXISTS team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    designation TEXT NOT NULL,
    role_category TEXT CHECK(role_category IN ('Executive', 'Technical', 'Operations', 'Finance', 'Board', 'Plant')),
    department TEXT DEFAULT 'BSPL Board', -- 'BSPL Board', 'Sales', 'Marketing', 'R&D', 'Accounts', 'Plant Operations'
    pin_code TEXT DEFAULT '1234',
    avatar_color TEXT DEFAULT '#10b981',
    access_level TEXT CHECK(access_level IN ('SuperAdmin', 'Director', 'Lead', 'Staff')) DEFAULT 'Director',
    phone TEXT,
    gmail_address TEXT UNIQUE NOT NULL,
    aadhaar_number TEXT,
    pan_number TEXT,
    residential_address TEXT,
    linkedin_url TEXT,
    core_responsibilities TEXT,
    gmail_sync_status TEXT DEFAULT 'Connected',
    last_gmail_sync TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Capital Assets & Machinery Register (From DPR Section 6.1.1 & 6.4.1)
CREATE TABLE IF NOT EXISTS machinery_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_code TEXT UNIQUE NOT NULL,
    asset_name TEXT NOT NULL,
    category TEXT CHECK(category IN ('Machinery', 'Infrastructure', 'Vehicle', 'Auxiliary', 'Laboratory')),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_cost_lakh REAL NOT NULL,
    total_cost_lakh REAL NOT NULL,
    funding_source TEXT CHECK(funding_source IN ('SIDBI Term Loan', 'Promoter Contribution', 'Internal Accrual')),
    vendor_supplier TEXT,
    status TEXT CHECK(status IN ('To Be Purchased', 'Budgeted', 'RFQ Issued', 'PO Issued', 'Fabrication', 'Delivered', 'Installed', 'Operational', 'Under Maintenance')) DEFAULT 'To Be Purchased',
    hypothecated_to TEXT DEFAULT 'SIDBI Bank',
    depreciation_rate_wdv REAL DEFAULT 10.0,
    installation_target_date DATE,
    maintenance_interval_days INTEGER DEFAULT 30,
    last_serviced_date DATE,
    notes TEXT
);

-- 4. Feedstock Sourcing & Raw Material Intake (Stages 1 & 2)
CREATE TABLE IF NOT EXISTS feedstock_intake (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intake_lot_number TEXT UNIQUE NOT NULL,
    intake_date DATE NOT NULL,
    supplier_name TEXT NOT NULL,
    supplier_category TEXT CHECK(supplier_category IN ('Municipal ULB', 'Corporate Generator', 'MRF Aggregator', 'Agricultural Producer', 'Industrial Fly Ash', 'Other')),
    material_category TEXT CHECK(material_category IN ('Recovered Plastics', 'Agricultural Residues', 'Mineral Materials (Fly Ash/C&D)', 'Livestock Residues (Cow Dung)', 'Process Additives & Resins')),
    specific_material TEXT NOT NULL,
    gross_weight_kg REAL NOT NULL,
    tare_weight_kg REAL DEFAULT 0,
    net_weight_kg REAL NOT NULL,
    moisture_percentage REAL DEFAULT 0.0,
    contamination_percentage REAL DEFAULT 0.0,
    accepted_net_kg REAL NOT NULL,
    rejected_kg REAL DEFAULT 0.0,
    cost_per_kg REAL DEFAULT 0.0,
    total_cost REAL DEFAULT 0.0,
    weighbridge_slip_no TEXT,
    storage_bin_location TEXT,
    inspection_status TEXT CHECK(inspection_status IN ('Pending QC', 'Accepted', 'Rejected', 'Blended')) DEFAULT 'Pending QC',
    assigned_technician TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. 10-Stage Manufacturing Batches (Stages 1-10)
CREATE TABLE IF NOT EXISTS manufacturing_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_number TEXT UNIQUE NOT NULL,
    production_date DATE NOT NULL,
    product_sku TEXT NOT NULL,
    shift TEXT CHECK(shift IN ('Shift 1 (Day)', 'Shift 2 (Evening)', 'Night Shift')) DEFAULT 'Shift 1 (Day)',
    recipe_code TEXT NOT NULL,
    planned_sqft REAL NOT NULL,
    produced_sqft REAL DEFAULT 0,
    rejected_sqft REAL DEFAULT 0,
    good_sqft REAL DEFAULT 0,
    
    plastic_feedstock_kg REAL DEFAULT 0,
    flyash_mineral_kg REAL DEFAULT 0,
    agro_residue_kg REAL DEFAULT 0,
    additives_pigment_kg REAL DEFAULT 0,
    total_feedstock_kg REAL DEFAULT 0,
    
    curing_temperature_celsius REAL DEFAULT 180.0,
    hydraulic_press_tonnage REAL DEFAULT 150.0,
    pressing_cycle_seconds INTEGER DEFAULT 45,
    power_consumed_kwh REAL DEFAULT 0.0,
    water_consumed_liters REAL DEFAULT 0.0,
    
    current_stage INTEGER CHECK(current_stage BETWEEN 1 AND 10) DEFAULT 1,
    stage_name TEXT DEFAULT 'Stage 1: Raw Material Procurement',
    batch_status TEXT CHECK(batch_status IN ('Scheduled', 'In Progress', 'Cooling', 'QC Pending', 'Approved', 'Rejected', 'Packaged & Stocked')) DEFAULT 'Scheduled',
    
    plant_operator TEXT,
    shift_incharge TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Quality Control & Testing Register (Stage 9)
CREATE TABLE IF NOT EXISTS quality_inspections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inspection_id TEXT UNIQUE NOT NULL,
    batch_id INTEGER REFERENCES manufacturing_batches(id),
    test_date DATE NOT NULL,
    product_sku TEXT NOT NULL,
    compressive_strength_mpa REAL NOT NULL,
    water_absorption_pct REAL NOT NULL,
    thickness_variance_mm REAL NOT NULL,
    warpage_mm REAL DEFAULT 0.0,
    surface_finish_rating TEXT CHECK(surface_finish_rating IN ('A-Grade Smooth', 'B-Grade Commercial', 'Textured / R-Grade', 'Defective')),
    defect_classification TEXT,
    testing_agency TEXT DEFAULT 'In-House QC Lab (Validated with NIT/IIT Patna)',
    lab_report_ref TEXT,
    inspection_outcome TEXT CHECK(inspection_outcome IN ('Certified Pass', 'Conditional Pass', 'Rejected for Downcycling')) DEFAULT 'Certified Pass',
    certified_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Sales, Commercial Pre-Orders & Pipeline (Traction)
CREATE TABLE IF NOT EXISTS sales_pipeline_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_code TEXT UNIQUE NOT NULL,
    customer_name TEXT NOT NULL,
    customer_segment TEXT CHECK(customer_segment IN ('Commercial Developer', 'Infrastructure Contractor', 'Govt ULB / Municipality', 'Smart Cities Initiative', 'CSR & Institutional', 'Distributor / Dealer', 'Industrial Circular Partner')),
    contact_person TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    project_location TEXT,
    product_sku TEXT NOT NULL,
    quantity_sqft REAL NOT NULL,
    unit_price_per_sqft REAL NOT NULL,
    total_order_value REAL NOT NULL,
    deal_stage TEXT CHECK(deal_stage IN ('Pre-Order Discussion', 'Proposal Submitted', 'Lead / Inquiry', 'Sample Approved', 'LOI Signed', 'PO Issued', 'Under Production', 'Ready for Dispatch', 'Dispatched / In Transit', 'Delivered & Invoiced', 'Payment Completed')) DEFAULT 'Pre-Order Discussion',
    delivery_deadline DATE,
    dispatched_date DATE,
    invoice_number TEXT,
    payment_terms TEXT DEFAULT '30 Days Net',
    amount_paid REAL DEFAULT 0.0,
    balance_due REAL DEFAULT 0.0,
    payment_status TEXT CHECK(payment_status IN ('Unpaid', 'Advance Paid', 'Fully Paid', 'Overdue')) DEFAULT 'Unpaid',
    assigned_account_manager TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Financial Projections & Actual Monthly MIS (From DPR Tables 1 & 2)
CREATE TABLE IF NOT EXISTS financial_mis_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fiscal_year TEXT NOT NULL,
    month_year TEXT NOT NULL,
    is_projection INTEGER DEFAULT 0,
    production_sqft REAL NOT NULL,
    sales_volume_sqft REAL NOT NULL,
    selling_price_per_sqft REAL DEFAULT 23.0,
    revenue_lakh REAL NOT NULL,
    cogs_lakh REAL NOT NULL,
    gross_profit_lakh REAL NOT NULL,
    fixed_operating_costs_lakh REAL NOT NULL,
    ebitda_lakh REAL NOT NULL,
    ebitda_margin_pct REAL,
    depreciation_lakh REAL DEFAULT 0.0,
    interest_expense_lakh REAL DEFAULT 0.0,
    profit_before_tax_lakh REAL,
    tax_lakh REAL DEFAULT 0.0,
    profit_after_tax_lakh REAL,
    cash_available_debt_service_lakh REAL,
    total_debt_service_lakh REAL,
    dscr_ratio REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. SIDBI Loan Amortization Schedule (DPR Section 9.3 Table 3)
CREATE TABLE IF NOT EXISTS loan_amortization_schedule (
    loan_year INTEGER PRIMARY KEY,
    calendar_period TEXT NOT NULL,
    opening_balance_lakh REAL NOT NULL,
    interest_expense_lakh REAL NOT NULL,
    principal_repaid_lakh REAL NOT NULL,
    total_debt_service_lakh REAL NOT NULL,
    closing_loan_balance_lakh REAL NOT NULL,
    monthly_emi_lakh REAL DEFAULT 1.062,
    status TEXT CHECK(status IN ('Upcoming', 'Current', 'Paid in Full')) DEFAULT 'Upcoming'
);

-- 10. Environmental, ESG & Mass Balance Impact Tracker
CREATE TABLE IF NOT EXISTS esg_environmental_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_date DATE NOT NULL,
    period_label TEXT NOT NULL,
    solid_waste_diverted_kg REAL NOT NULL,
    plastic_waste_recycled_kg REAL NOT NULL,
    fly_ash_recycled_kg REAL NOT NULL,
    agro_residue_recycled_kg REAL NOT NULL,
    cd_debris_recycled_kg REAL NOT NULL,
    co2_emissions_avoided_kg REAL NOT NULL,
    thermal_energy_saved_kwh REAL NOT NULL,
    water_recycled_liters REAL NOT NULL,
    epr_credits_units_generated REAL DEFAULT 0.0,
    certified_auditor TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Work Portal: Enhanced Task Tracker (With Department / Account Head Tagging)
CREATE TABLE IF NOT EXISTS work_portal_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    department TEXT CHECK(department IN ('BSPL Board', 'Sales', 'Marketing', 'R&D', 'Accounts', 'Plant Operations')) DEFAULT 'Plant Operations',
    category TEXT CHECK(category IN ('Plant Setup & Civil Works', 'Machinery & Procurement', 'Raw Material & Sourcing', 'R&D & Formulations', 'Production & QC', 'Sales & B2B Pipeline', 'SIDBI & Banking Finance', 'Governance & Legal')),
    assigned_to_id INTEGER REFERENCES team_members(id),
    assigned_to_name TEXT NOT NULL,
    priority TEXT CHECK(priority IN ('P0 - Critical', 'P1 - High', 'P2 - Medium', 'P3 - Low')) DEFAULT 'P2 - Medium',
    status TEXT CHECK(status IN ('To Do', 'In Progress', 'Under Review', 'Completed', 'Blocked')) DEFAULT 'To Do',
    progress_percentage INTEGER DEFAULT 0,
    due_date DATE,
    completed_at DATE,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Department Communication Channels (Sales, Marketing, R&D, Accounts, BSPL Board, Plant Ops)
CREATE TABLE IF NOT EXISTS department_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    icon TEXT NOT NULL,
    description TEXT,
    account_head_name TEXT NOT NULL,
    account_head_email TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. Channel Messages & Operational Communication Thread
CREATE TABLE IF NOT EXISTS channel_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_slug TEXT NOT NULL REFERENCES department_channels(slug),
    author_id INTEGER REFERENCES team_members(id),
    author_name TEXT NOT NULL,
    author_email TEXT NOT NULL,
    author_role TEXT,
    message_text TEXT NOT NULL,
    linked_entity_type TEXT, -- 'Batch', 'Sales Order', 'Machinery Asset', 'SIDBI Loan', 'Task'
    linked_entity_id TEXT,
    is_gmail_notified INTEGER DEFAULT 1,
    gmail_sync_status TEXT DEFAULT 'Delivered',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. Work Portal: Gmail Integration & Synced Communications Log
CREATE TABLE IF NOT EXISTS gmail_messages_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gmail_message_id TEXT UNIQUE NOT NULL,
    thread_id TEXT,
    team_member_email TEXT NOT NULL,
    sender_name TEXT,
    sender_email TEXT NOT NULL,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    snippet TEXT,
    body_content TEXT,
    email_date TIMESTAMP NOT NULL,
    category TEXT CHECK(category IN ('Investor & Board', 'SIDBI & Bank', 'Supplier & Machinery', 'Raw Material Sourcing', 'Customer & Pre-Orders', 'Incubation & Grants', 'Operations & General')),
    linked_module TEXT,
    is_starred INTEGER DEFAULT 0,
    is_read INTEGER DEFAULT 0,
    action_required INTEGER DEFAULT 0,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lightning fast lookups
CREATE INDEX IF NOT EXISTS idx_feedstock_date ON feedstock_intake(intake_date);
CREATE INDEX IF NOT EXISTS idx_batches_date ON manufacturing_batches(production_date);
CREATE INDEX IF NOT EXISTS idx_tasks_dept ON work_portal_tasks(department);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON work_portal_tasks(status);
CREATE INDEX IF NOT EXISTS idx_channel_slug ON channel_messages(channel_slug);
CREATE INDEX IF NOT EXISTS idx_gmail_date ON gmail_messages_log(email_date);
