const { initDb } = require('./db');

function seedDatabase() {
    const db = initDb();

    console.log('[Seed] Beginning data seeding with VALIDATED DATA ONLY...');

    // 1. Company Profile (DPR Section 1.2)
    db.prepare('DELETE FROM company_profile').run();
    db.prepare(`
        INSERT INTO company_profile (
            company_name, cin, pan, tan, dipp_number, udyam_reg_number, 
            gst_wb, gst_bihar, registered_office, plant_location, 
            site_area_sqft, workshed_sqft, roofing_shed_sqft, website, official_email
        ) VALUES (
            'Bioron Solutions Private Limited',
            'U74999BR2020PTC080854',
            'AAJCB4812F',
            'CALB21151E',
            'DIPP99938',
            'UDYAM-WB-15-0007940',
            '19AAJCB4812F1ZR',
            'Application In Process (Patna Circle)',
            'F-57/104/1397/B R Ahmedkar Road, Rathtala, Kalyani, Nadia, West Bengal 741235',
            'Korra, Naubatpur, Patna, Bihar 801109',
            7000, 1000, 2000,
            'www.bioronsolutions.com',
            'bioronsolutions@gmail.com'
        )
    `).run();
    console.log('[Seed] Validated company profile seeded.');

    // 2. Team Members (Admin + DPR Section 1.2 Promoters)
    db.prepare('DELETE FROM team_members').run();
    const team = [
        {
            name: 'BSPL Operations Admin',
            designation: 'Master Administrator & Operations Controller',
            role_category: 'Executive',
            department: 'BSPL Board',
            pin_code: '1234',
            avatar_color: '#10b981',
            access_level: 'SuperAdmin',
            phone: '+91 8981922296',
            gmail_address: 'bioronsolutions@gmail.com',
            aadhaar_number: 'N/A (Corporate Master)',
            pan_number: 'AAJCB4812F',
            residential_address: 'Registered Office, Kalyani, Nadia, WB',
            linkedin_url: 'https://www.linkedin.com/company/bioron-solutions',
            core_responsibilities: 'Master administrative oversight, board management, department communication, credentials and operations tracking.',
            gmail_sync_status: 'Connected',
            last_gmail_sync: new Date().toISOString().replace('T', ' ').substring(0, 19)
        },
        {
            name: 'Sudip Roy',
            designation: 'Chief Executive Officer (Promoter 1)',
            role_category: 'Executive',
            department: 'BSPL Board',
            pin_code: '1234',
            avatar_color: '#059669',
            access_level: 'SuperAdmin',
            phone: '8981922296',
            gmail_address: 'sudroy809@gmail.com',
            aadhaar_number: '419902724145',
            pan_number: 'BHKPR1464F',
            residential_address: 'F-57/104/1397/B R Ahmedkar Road, Rathtala, Kalyani, Nadia, 741235',
            linkedin_url: 'https://linkedin.com/in/sudip-roy-b50089104',
            core_responsibilities: 'Production, R&D & Tech Architecture, Strategic Partnerships, SIDBI Financing, Corporate Governance.',
            gmail_sync_status: 'Connected',
            last_gmail_sync: new Date().toISOString().replace('T', ' ').substring(0, 19)
        },
        {
            name: 'Raman Vishwakarma',
            designation: 'Chief Technical Officer / Co-Founder & COO (Promoter 2)',
            role_category: 'Technical',
            department: 'Sales',
            pin_code: '1234',
            avatar_color: '#06b6d4',
            access_level: 'Director',
            phone: '—',
            gmail_address: 'raman.bioron@gmail.com',
            aadhaar_number: '—',
            pan_number: '—',
            residential_address: 'Patna, Bihar',
            linkedin_url: 'http://www.linkedin.com/in/raman-vishwakarma-142873392',
            core_responsibilities: 'Business Expansion & Scaling, Operational Efficiency & Delivery, B2B Pre-orders & GTM Offtake MOUs.',
            gmail_sync_status: 'Connected',
            last_gmail_sync: new Date().toISOString().replace('T', ' ').substring(0, 19)
        },
        {
            name: 'Shashank Srivastav',
            designation: 'Chief Operating Officer (Promoter 3)',
            role_category: 'Operations',
            department: 'Marketing',
            pin_code: '1234',
            avatar_color: '#8b5cf6',
            access_level: 'Director',
            phone: '—',
            gmail_address: 'shashank.bioron@gmail.com',
            aadhaar_number: '—',
            pan_number: '—',
            residential_address: 'Patna, Bihar',
            linkedin_url: '',
            core_responsibilities: 'Feedstock Supply Chain, Waste Aggregators & Municipal Liaison, Marketing & Public Sector Alliances.',
            gmail_sync_status: 'Connected',
            last_gmail_sync: new Date().toISOString().replace('T', ' ').substring(0, 19)
        },
        {
            name: 'Uttam Kumar',
            designation: 'Investor & Shareholder (Promoter 4)',
            role_category: 'Board',
            department: 'Accounts',
            pin_code: '1234',
            avatar_color: '#f59e0b',
            access_level: 'Director',
            phone: '—',
            gmail_address: 'uttam.kumar.investor@gmail.com',
            aadhaar_number: '—',
            pan_number: '—',
            residential_address: 'Patna, Bihar',
            linkedin_url: '',
            core_responsibilities: 'Capital Allocation, Investor Relations, Treasury, Financial Governance & Accounting Controls.',
            gmail_sync_status: 'Connected',
            last_gmail_sync: new Date().toISOString().replace('T', ' ').substring(0, 19)
        },
        {
            name: 'Naubatpur Plant Operations Head',
            designation: 'Plant Engineer & Shift Supervisor',
            role_category: 'Plant',
            department: 'Plant Operations',
            pin_code: '1234',
            avatar_color: '#34d399',
            access_level: 'Lead',
            phone: '—',
            gmail_address: 'plant.naubatpur@gmail.com',
            aadhaar_number: '—',
            pan_number: '—',
            residential_address: 'Naubatpur, Patna, Bihar',
            linkedin_url: '',
            core_responsibilities: 'Plant readiness, machinery installation, trial batches, daily mass balance logs and operator safety.',
            gmail_sync_status: 'Connected',
            last_gmail_sync: new Date().toISOString().replace('T', ' ').substring(0, 19)
        }
    ];

    const stmtTeam = db.prepare(`
        INSERT INTO team_members (
            name, designation, role_category, department, pin_code, avatar_color, access_level,
            phone, gmail_address, aadhaar_number, pan_number, residential_address, linkedin_url, 
            core_responsibilities, gmail_sync_status, last_gmail_sync
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    team.forEach(t => {
        stmtTeam.run(
            t.name, t.designation, t.role_category, t.department, t.pin_code, t.avatar_color, t.access_level,
            t.phone, t.gmail_address, t.aadhaar_number, t.pan_number, t.residential_address, t.linkedin_url,
            t.core_responsibilities, t.gmail_sync_status, t.last_gmail_sync
        );
    });
    console.log('[Seed] Team members (including Admin bioronsolutions@gmail.com) seeded.');

    // 3. Department Channels (Exact Account Heads)
    db.prepare('DELETE FROM department_channels').run();
    const channels = [
        {
            slug: 'bspl-board',
            name: 'BSPL Board & Governance',
            icon: '🏛️',
            description: 'Board governance, SIDBI loan appraisal (₹77.71L), project cost reconciliation (₹87.03L), and statutory compliance.',
            account_head_name: 'Sudip Roy & Uttam Kumar',
            account_head_email: 'bioronsolutions@gmail.com'
        },
        {
            slug: 'sales',
            name: 'Sales & Commercial Offtake',
            icon: '💼',
            description: 'B2B commercial construction developers, B2G infrastructure tenders, pre-order pipeline (₹1.5 Cr / 500k sq ft).',
            account_head_name: 'Raman Vishwakarma',
            account_head_email: 'raman.bioron@gmail.com'
        },
        {
            slug: 'marketing',
            name: 'Marketing & Strategic Alliances',
            icon: '📣',
            description: 'CleanTech branding, Greenr cohort (IKEA Foundation/Visa/TechnoServe), MSME Champion showcase, EPR partnerships.',
            account_head_name: 'Shashank Srivastav',
            account_head_email: 'shashank.bioron@gmail.com'
        },
        {
            slug: 'rd',
            name: 'R&D & Technical Validation',
            icon: '🔬',
            description: 'GreenBuild composite formulation, curing trials (<200°C), NIT & IIT Patna standards, M30/M40 load resistance.',
            account_head_name: 'Sudip Roy',
            account_head_email: 'sudroy809@gmail.com'
        },
        {
            slug: 'accounts',
            name: 'Accounts & Financial Control',
            icon: '💰',
            description: '90-day working capital cycle (₹12.66L), GST compliance (WB 19AAJCB4812F1ZR & Bihar), fixed asset register, banking audit.',
            account_head_name: 'Uttam Kumar',
            account_head_email: 'uttam.kumar.investor@gmail.com'
        },
        {
            slug: 'plant-ops',
            name: 'Naubatpur Plant Operations',
            icon: '🏭',
            description: 'Site readiness, civil preparation, machinery procurement and installation stages, power connection, operator safety.',
            account_head_name: 'Naubatpur Plant Operations Head',
            account_head_email: 'plant.naubatpur@gmail.com'
        }
    ];

    const stmtChan = db.prepare(`
        INSERT INTO department_channels (
            slug, name, icon, description, account_head_name, account_head_email
        ) VALUES (?, ?, ?, ?, ?, ?)
    `);

    channels.forEach(c => {
        stmtChan.run(c.slug, c.name, c.icon, c.description, c.account_head_name, c.account_head_email);
    });
    console.log('[Seed] Department channels seeded.');

    // 4. Clean Channel Messages (Validated Directives from Admin)
    db.prepare('DELETE FROM channel_messages').run();
    const messages = [
        {
            channel_slug: 'bspl-board',
            author_id: 1,
            author_name: 'BSPL Operations Admin',
            author_email: 'bioronsolutions@gmail.com',
            author_role: 'Master Administrator',
            message_text: 'Official Board Channel initialized. DPR for Korra, Naubatpur facility (₹87.03 Lakh total project cost) submitted for SIDBI financing appraisal. All board members and account heads can log their operational updates directly here.',
            linked_entity_type: 'SIDBI Loan',
            linked_entity_id: 'Financing Proposal (₹77.71L)',
            is_gmail_notified: 1
        },
        {
            channel_slug: 'sales',
            author_id: 1,
            author_name: 'BSPL Operations Admin',
            author_email: 'bioronsolutions@gmail.com',
            author_role: 'Master Administrator',
            message_text: 'Sales & Offtake channel active. Tracking 500,000 sq ft pre-order pipeline interest (PepsiCo, Kalyani Municipality PPP, Youth Aid Foundation, and Eastern Promoters). Maintain discussion logs here.',
            linked_entity_type: 'Sales Pipeline',
            linked_entity_id: '500,000 sq ft Demand',
            is_gmail_notified: 1
        },
        {
            channel_slug: 'plant-ops',
            author_id: 1,
            author_name: 'BSPL Operations Admin',
            author_email: 'bioronsolutions@gmail.com',
            author_role: 'Master Administrator',
            message_text: 'Machinery master register set to "To Be Purchased". As vendor quotations are finalized and loan disbursements commence, update each asset status through RFQ -> PO Issued -> Delivered -> Installed.',
            linked_entity_type: 'Machinery Register',
            linked_entity_id: '21 Capital Assets (₹69.40L)',
            is_gmail_notified: 1
        }
    ];

    const stmtMsg = db.prepare(`
        INSERT INTO channel_messages (
            channel_slug, author_id, author_name, author_email, author_role,
            message_text, linked_entity_type, linked_entity_id, is_gmail_notified
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    messages.forEach(m => {
        stmtMsg.run(m.channel_slug, m.author_id, m.author_name, m.author_email, m.author_role, m.message_text, m.linked_entity_type, m.linked_entity_id, m.is_gmail_notified);
    });
    console.log('[Seed] Channel initialization messages seeded.');

    // 5. Machinery & Capital Assets (DPR Section 6.1.1 & 6.4.1)
    // ALL MACHINERY STATUS SET TO "To Be Purchased" AS INSTRUCTED!
    db.prepare('DELETE FROM machinery_assets').run();
    const assets = [
        // 21 Machinery Items (₹69.40 Lakhs Total) - Status: 'To Be Purchased'
        ['MCH-01', 'Concrete Mixer (Main Chamber)', 'Machinery', 3, 6.00, 18.00, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-15', 'Primary heavy-duty mixing chamber for polymer & aggregate homogenisation.'],
        ['MCH-02', 'Hydraulic Press Mechanism + Conveyors', 'Machinery', 2, 7.00, 14.00, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-20', 'High tonnage press with precision automated heating platen (<200°C).'],
        ['MCH-03', 'Mixer Secondary Chamber', 'Machinery', 3, 5.00, 15.00, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-15', 'Secondary blending & coloring compounding chamber.'],
        ['MCH-04', 'Molds (Lock & Unlock)', 'Machinery', 2, 1.20, 2.40, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-10', 'Hardened precision molds for 300x300mm tiles and pavers.'],
        ['MCH-05', 'Containers', 'Auxiliary', 6, 0.05, 0.30, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-05', 'Batch transfer intermediate bins.'],
        ['MCH-06', 'Agricultural Shredding Module', 'Machinery', 1, 1.50, 1.50, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-10', 'High-speed rotary chopper for straw, stubble, and agro residues.'],
        ['MCH-07', 'Crusher Module', 'Machinery', 1, 2.25, 2.25, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-10', 'Size reduction for C&D mineral fractions and ceramic waste.'],
        ['MCH-08', 'Plastic Shredding Module', 'Machinery', 1, 0.75, 0.75, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-10', 'Dual-shaft plastic shredder for LDPE/HDPE/MLP.'],
        ['MCH-09', 'Plastic Washing Module', 'Machinery', 1, 0.75, 0.75, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-12', 'Friction washer to clean dirt and film from plastic.'],
        ['MCH-10', 'Drying Module', 'Machinery', 1, 0.80, 0.80, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-12', 'Centrifugal dryer and thermal de-moisturizer.'],
        ['MCH-11', 'Sieve Sections', 'Machinery', 1, 0.40, 0.40, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-08', 'Vibratory particle grader for 0mm to 25mm aggregate bands.'],
        ['MCH-12', 'Container for Water Boiling', 'Auxiliary', 1, 0.50, 0.50, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-08', 'Sanitization and de-greasing chamber.'],
        ['MCH-13', 'Carriers', 'Auxiliary', 4, 0.20, 0.80, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-05', 'Material transport pallets and carriers.'],
        ['MCH-14', 'Sucker', 'Auxiliary', 3, 0.20, 0.60, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-05', 'Pneumatic powder and flake transfer suction systems.'],
        ['MCH-15', 'Condenser / Cooling Tower', 'Machinery', 1, 0.80, 0.80, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-15', 'Closed-loop cooling water circuit for press hydraulics.'],
        ['MCH-16', 'Plastic Containers', 'Auxiliary', 10, 0.03, 0.30, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-05', 'Finished batch holding crates.'],
        ['MCH-17', 'Conveyors + Cooling Spray + Coating Segment 1st', 'Machinery', 2, 0.50, 1.00, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-20', 'Post-cure tile cooling conveyor with surface coating spray.'],
        ['MCH-18', 'Storage Racks', 'Auxiliary', 6, 0.50, 3.00, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-05', 'Heavy-duty multi-tier curing and warehouse racking.'],
        ['MCH-19', 'Miscellaneous Tooling & Spares', 'Auxiliary', 1, 1.50, 1.50, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-15', 'Maintenance kits, pressure sensors, thermocouples.'],
        ['MCH-20', 'Liquid Collection & Fuel Extraction', 'Machinery', 1, 0.75, 0.75, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-20', 'Byproduct condensate and pyrolytic fuel recovery system.'],
        ['MCH-21', 'Within-Unit Transport Trolleys', 'Vehicle', 2, 0.50, 1.00, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-05', 'Heavy manual and hydraulic pallet trolleys.'],
        ['MCH-22', 'EV for Local Transportation', 'Vehicle', 1, 3.00, 3.00, 'SIDBI Term Loan', 'To Be Finalized', 'To Be Purchased', 'SIDBI Bank', '2026-12-20', 'Cargo 3-wheeler for local feedstock pickup and deliveries.'],

        // Promoter Funded Infrastructure (₹4.97 Lakhs) - Status: 'Budgeted'
        ['INF-01', 'Workshed Preparation (1,000 sq ft)', 'Infrastructure', 1, 0.80, 0.80, 'Promoter Contribution', 'Civil Contractor', 'Budgeted', 'Promoter Property', '2026-11-30', 'Enclosed manufacturing shed with concrete flooring.'],
        ['INF-02', 'Additional Roofing Shed (2,000 sq ft)', 'Infrastructure', 1, 0.60, 0.60, 'Promoter Contribution', 'Prefab Contractor', 'Budgeted', 'Promoter Property', '2026-11-30', 'Covered shed for feedstock storage and segregation.'],
        ['INF-03', 'Land Preparation & Leveling', 'Infrastructure', 1, 0.75, 0.75, 'Promoter Contribution', 'Earthmovers', 'Budgeted', 'Promoter Property', '2026-11-20', 'Site grading, compaction and drainage channels.'],
        ['INF-04', 'Boundary Fencing & Security Gate', 'Infrastructure', 1, 0.75, 0.75, 'Promoter Contribution', 'Fabrication Works', 'Budgeted', 'Promoter Property', '2026-11-25', 'Site perimeter boundary and secure entrance.'],
        ['INF-05', 'Electrical Connection & Metering', 'Infrastructure', 1, 0.30, 0.30, 'Promoter Contribution', 'BSPHCL Contractor', 'Budgeted', 'Promoter Property', '2026-12-05', '3-phase industrial power load installation.'],
        ['INF-06', 'Wiring, Switchgear & Distribution Board', 'Infrastructure', 1, 0.35, 0.35, 'Promoter Contribution', 'Electrical Contractor', 'Budgeted', 'Promoter Property', '2026-12-05', 'Industrial cabling, circuit breakers, emergency stop relays.'],
        ['INF-07', 'Machine Foundation Grouting', 'Infrastructure', 1, 0.40, 0.40, 'Promoter Contribution', 'Civil Contractor', 'Budgeted', 'Promoter Property', '2026-12-10', 'Vibration-damped machine base grouting.'],
        ['INF-08', 'Storage Tanks (Water & Chemical Additives)', 'Infrastructure', 1, 0.25, 0.25, 'Promoter Contribution', 'Tank Suppliers', 'Budgeted', 'Promoter Property', '2026-11-25', 'Water storage and polymer additive tank.'],
        ['INF-09', 'Safety Gear, PPE & Boots', 'Infrastructure', 1, 0.12, 0.12, 'Promoter Contribution', 'Safety Supplies', 'Budgeted', 'Promoter Property', '2026-11-30', 'Helmets, heat-resistant gloves, boots, eye protection.'],
        ['INF-10', 'Tools, Calibration Equipment & Process Line', 'Infrastructure', 1, 0.50, 0.50, 'Promoter Contribution', 'Instrument Suppliers', 'Budgeted', 'Promoter Property', '2026-12-10', 'Precision calipers, digital scales, digital temperature sensors.'],
        ['INF-11', 'Legal, Pollution Clearance & Compliance', 'Infrastructure', 1, 0.15, 0.15, 'Promoter Contribution', 'Legal Advisors', 'Budgeted', 'Promoter Property', '2026-11-20', 'MSME, SPCB Consent, factory inspector filings.']
    ];

    const stmtAsset = db.prepare(`
        INSERT INTO machinery_assets (
            asset_code, asset_name, category, quantity, unit_cost_lakh, 
            total_cost_lakh, funding_source, vendor_supplier, status, 
            hypothecated_to, installation_target_date, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    assets.forEach(a => {
        stmtAsset.run(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11]);
    });
    console.log('[Seed] Machinery Assets seeded with status "To Be Purchased" (₹69.40L) & Infrastructure (₹4.97L).');

    // 6. Feedstock Inventory: ZERO SAMPLE DATA!
    db.prepare('DELETE FROM feedstock_intake').run();
    console.log('[Seed] Feedstock intake cleared of sample data (ready for real weighbridge entries).');

    // 7. Manufacturing Batches: ZERO SAMPLE DATA!
    db.prepare('DELETE FROM manufacturing_batches').run();
    console.log('[Seed] Manufacturing batches cleared of sample data (ready for real production runs).');

    // 8. Quality Inspections: Validated Historical Benchmarks (DPR Section 3 & Pitch Deck)
    db.prepare('DELETE FROM quality_inspections').run();
    db.prepare(`
        INSERT INTO quality_inspections (
            inspection_id, batch_id, test_date, product_sku,
            compressive_strength_mpa, water_absorption_pct, thickness_variance_mm,
            warpage_mm, surface_finish_rating, defect_classification,
            testing_agency, lab_report_ref, inspection_outcome, certified_by
        ) VALUES (
            'QC-BENCHMARK-01',
            NULL,
            '2026-10-20',
            'GreenBuild Composite Tiles (M30/M40 Baseline Validation)',
            34.2,
            0.74,
            0.18,
            0.10,
            'A-Grade Smooth',
            'None',
            'Technical Validation Cell (AIC-JKLU / NIT & IIT Patna Guidance)',
            'VAL-BSPL-2026-M30',
            'Certified Pass',
            'Sudip Roy'
        )
    `).run();
    console.log('[Seed] Validated technical benchmark recorded in QC register.');

    // 9. Commercial Pipeline Orders: Validated Demand (Pitch Deck Slide 10: 500,000 sq ft / ₹1.5 Cr Pipeline)
    db.prepare('DELETE FROM sales_pipeline_orders').run();
    const pipeline = [
        [
            'PIPE-PEP-01',
            'PepsiCo India Holdings Pvt Ltd',
            'Industrial Circular Partner',
            'Sustainability Offtake Division',
            'info@bioronsolutions.com',
            '—',
            'Regional Warehouses',
            'GreenBuild Industrial Composite Pavers',
            80000,
            28.0,
            2240000,
            'Pre-Order Discussion',
            '2027-02-28',
            null,
            null,
            'Partnership dialogue for sustainable waste & boiler fly ash off-take',
            0,
            2240000,
            'Unpaid',
            'Raman Vishwakarma'
        ],
        [
            'PIPE-KAL-02',
            'Kalyani Municipality / Nadia DM Office (PPP Model)',
            'Govt ULB / Municipality',
            'District Magistrate / Municipal Executive',
            'info@bioronsolutions.com',
            '—',
            'Public Walkways & Civic Spaces',
            'GreenBuild Public Footpath Interlocking Tiles',
            120000,
            25.0,
            3000000,
            'Proposal Submitted',
            '2027-03-31',
            null,
            null,
            'PPP Model Proposal submitted to Nadia District Magistrate',
            0,
            3000000,
            'Unpaid',
            'Sudip Roy'
        ],
        [
            'PIPE-YAF-03',
            'Youth Aid Foundation (RDF Stream)',
            'CSR & Institutional',
            'Circular Projects Team',
            'info@bioronsolutions.com',
            '—',
            'Community Infrastructure Projects',
            'GreenBuild Composite Tiles - Base M30',
            60000,
            24.0,
            1440000,
            'Pre-Order Discussion',
            '2027-01-31',
            null,
            null,
            'Collaboration dialogue to create value from RDF managing plastic & waste',
            0,
            1440000,
            'Unpaid',
            'Shashank Srivastav'
        ],
        [
            'PIPE-EST-04',
            'Commercial Construction Promoters & Contractors Consortium',
            'Commercial Developer',
            'Procurement & Architecture Firms',
            'info@bioronsolutions.com',
            '—',
            'Eastern India Commercial Projects',
            'GreenBuild Composite Tiles & Exterior Panels',
            240000,
            26.5,
            6360000,
            'Pre-Order Discussion',
            '2027-04-30',
            null,
            null,
            'Active discussions with promoters and architectural firms for deployment',
            0,
            6360000,
            'Unpaid',
            'Raman Vishwakarma'
        ]
    ];

    const stmtPipe = db.prepare(`
        INSERT INTO sales_pipeline_orders (
            order_code, customer_name, customer_segment, contact_person,
            contact_email, contact_phone, project_location, product_sku,
            quantity_sqft, unit_price_per_sqft, total_order_value,
            deal_stage, delivery_deadline, dispatched_date, invoice_number,
            payment_terms, amount_paid, balance_due, payment_status, assigned_account_manager
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    pipeline.forEach(p => {
        stmtPipe.run(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15], p[16], p[17], p[18], p[19]);
    });
    console.log('[Seed] Validated pre-order pipeline (500,000 sq ft / ₹1.304 Cr) seeded.');

    // 10. Financial Projections Ledger (Exact DPR Tables 1 & 2)
    db.prepare('DELETE FROM financial_mis_ledger').run();
    const projections = [
        ['FY 2026-27 (Ramp)', 'Nov 2026 - Mar 2027 (Ramp Cumulative)', 1, 210000, 147000, 23.0, 33.81, 22.05, 11.76, 8.50, 3.26, 9.64, 2.89, 7.74, -7.37, 0.00, -7.37, 3.26, 10.27, 0.32],
        ['FY 2027-28', 'Full Year 2', 1, 2800000, 1960000, 23.0, 450.80, 294.00, 156.80, 9.35, 147.45, 32.71, 6.65, 7.30, 133.50, 33.60, 99.90, 113.85, 12.74, 8.94],
        ['FY 2028-29', 'Full Year 3', 1, 3360000, 2352000, 23.0, 540.96, 352.80, 188.16, 10.29, 177.88, 32.88, 5.99, 6.73, 165.16, 41.57, 123.59, 136.31, 12.74, 10.70],
        ['FY 2029-30', 'Full Year 4', 1, 4032000, 2822400, 23.0, 649.15, 423.36, 225.79, 11.31, 214.48, 33.04, 5.39, 6.10, 202.99, 51.09, 151.90, 163.39, 12.74, 12.82],
        ['FY 2030-31', 'Full Year 5', 1, 4838400, 3386880, 23.0, 778.98, 508.03, 270.95, 12.44, 258.51, 33.19, 4.85, 5.40, 248.26, 62.49, 185.77, 196.02, 12.74, 15.39]
    ];

    const stmtFin = db.prepare(`
        INSERT INTO financial_mis_ledger (
            fiscal_year, month_year, is_projection, production_sqft, sales_volume_sqft,
            selling_price_per_sqft, revenue_lakh, cogs_lakh, gross_profit_lakh,
            fixed_operating_costs_lakh, ebitda_lakh, ebitda_margin_pct,
            depreciation_lakh, interest_expense_lakh, profit_before_tax_lakh,
            tax_lakh, profit_after_tax_lakh, cash_available_debt_service_lakh,
            total_debt_service_lakh, dscr_ratio
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    projections.forEach(p => {
        stmtFin.run(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15], p[16], p[17], p[18], p[19]);
    });
    console.log('[Seed] DPR financial projections seeded.');

    // 11. 10-Year SIDBI Loan Amortization Schedule (DPR Section 9.3 Table 3)
    db.prepare('DELETE FROM loan_amortization_schedule').run();
    const schedule = [
        [1, 'Year 1 (6 Mo Moratorium + 6 Mo EMI)', 77.96, 7.74, 2.53, 10.27, 75.43, 1.062, 'Upcoming'],
        [2, 'Year 2 (Full 12 Mo EMI)', 75.43, 7.30, 5.45, 12.74, 69.99, 1.062, 'Upcoming'],
        [3, 'Year 3 (Full 12 Mo EMI)', 69.99, 6.73, 6.02, 12.74, 63.97, 1.062, 'Upcoming'],
        [4, 'Year 4 (Full 12 Mo EMI)', 63.97, 6.10, 6.65, 12.74, 57.33, 1.062, 'Upcoming'],
        [5, 'Year 5 (Full 12 Mo EMI)', 57.33, 5.40, 7.34, 12.74, 49.98, 1.062, 'Upcoming'],
        [6, 'Year 6 (Full 12 Mo EMI)', 49.98, 4.63, 8.11, 12.74, 41.87, 1.062, 'Upcoming'],
        [7, 'Year 7 (Full 12 Mo EMI)', 41.87, 3.78, 8.96, 12.74, 32.91, 1.062, 'Upcoming'],
        [8, 'Year 8 (Full 12 Mo EMI)', 32.91, 2.85, 9.90, 12.74, 23.01, 1.062, 'Upcoming'],
        [9, 'Year 9 (Full 12 Mo EMI)', 23.01, 1.81, 10.93, 12.74, 12.08, 1.062, 'Upcoming'],
        [10, 'Year 10 (Full 12 Mo EMI)', 12.08, 0.66, 12.08, 12.74, 0.00, 1.062, 'Upcoming']
    ];

    const stmtAmort = db.prepare(`
        INSERT INTO loan_amortization_schedule (
            loan_year, calendar_period, opening_balance_lakh, interest_expense_lakh,
            principal_repaid_lakh, total_debt_service_lakh, closing_loan_balance_lakh,
            monthly_emi_lakh, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    schedule.forEach(s => {
        stmtAmort.run(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8]);
    });
    console.log('[Seed] SIDBI loan amortization schedule seeded.');

    // 12. ESG Metrics (Target Baseline from DPR Section 12)
    db.prepare('DELETE FROM esg_environmental_metrics').run();
    db.prepare(`
        INSERT INTO esg_environmental_metrics (
            record_date, period_label, solid_waste_diverted_kg, plastic_waste_recycled_kg,
            fly_ash_recycled_kg, agro_residue_recycled_kg, cd_debris_recycled_kg,
            co2_emissions_avoided_kg, thermal_energy_saved_kwh, water_recycled_liters,
            epr_credits_units_generated, certified_auditor
        ) VALUES (
            '2026-10-31',
            'Pre-Commissioning Baseline (Ramp Stage)',
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            'Pending Third-Party Baseline Certification (DPR Section 12 Requirement)'
        )
    `).run();
    console.log('[Seed] ESG metrics baseline seeded.');

    // 13. Work Portal Tasks (DPR Section 5: Implementation Stages 1 to 6)
    db.prepare('DELETE FROM work_portal_tasks').run();
    const tasks = [
        {
            task_code: 'TSK-STG-01',
            title: 'Implementation Stage 1: Site Readiness & Lease Formalities',
            description: 'Finalize registered lease deed for 7,000 sq ft Korra Naubatpur site, prepare scaled layout for 1,000 sq ft workshed and 2,000 sq ft roofing shed, complete civil compaction and drainage.',
            department: 'Plant Operations',
            category: 'Plant Setup & Civil Works',
            assigned_to_id: 2,
            assigned_to_name: 'Sudip Roy',
            priority: 'P0 - Critical',
            status: 'In Progress',
            progress_percentage: 60,
            due_date: '2026-11-20',
            created_by: 'bioronsolutions@gmail.com'
        },
        {
            task_code: 'TSK-STG-02',
            title: 'Implementation Stage 2: Procurement & Final Vendor Quotations',
            description: 'Obtain final binding vendor quotations for all 21 machinery assets (₹69.40 Lakhs). Confirm taxes, freight, installation scope, warranties and commissioning timelines.',
            department: 'Plant Operations',
            category: 'Machinery & Procurement',
            assigned_to_id: 3,
            assigned_to_name: 'Raman Vishwakarma',
            priority: 'P0 - Critical',
            status: 'In Progress',
            progress_percentage: 45,
            due_date: '2026-11-25',
            created_by: 'bioronsolutions@gmail.com'
        },
        {
            task_code: 'TSK-FIN-03',
            title: 'SIDBI Financing Final Appraisal & CA Review',
            description: 'Reconcile project cost (₹87.03L) and loan ask (₹77.71L). Submit CA-certified 5-year DSCR schedule, promoter contribution proof (₹9.32L) and obtain sanction letter.',
            department: 'BSPL Board',
            category: 'SIDBI & Banking Finance',
            assigned_to_id: 2,
            assigned_to_name: 'Sudip Roy',
            priority: 'P0 - Critical',
            status: 'In Progress',
            progress_percentage: 75,
            due_date: '2026-11-15',
            created_by: 'bioronsolutions@gmail.com'
        },
        {
            task_code: 'TSK-SAL-04',
            title: 'Formalize PepsiCo & Kalyani Municipality Offtake Agreements',
            description: 'Advance discussions from preliminary dialogues into signed MOUs/trial agreements for industrial paver deployment and municipal footpath pilot.',
            department: 'Sales',
            category: 'Sales & B2B Pipeline',
            assigned_to_id: 3,
            assigned_to_name: 'Raman Vishwakarma',
            priority: 'P1 - High',
            status: 'In Progress',
            progress_percentage: 50,
            due_date: '2026-12-05',
            created_by: 'bioronsolutions@gmail.com'
        },
        {
            task_code: 'TSK-ACC-05',
            title: 'Establish Governance & Accounting Controls',
            description: 'Setup dedicated company bank account, cashbook, fixed-asset register, and board-approved limits for purchases as per DPR Section 13.',
            department: 'Accounts',
            category: 'Governance & Legal',
            assigned_to_id: 5,
            assigned_to_name: 'Uttam Kumar',
            priority: 'P1 - High',
            status: 'To Do',
            progress_percentage: 20,
            due_date: '2026-11-30',
            created_by: 'bioronsolutions@gmail.com'
        },
        {
            task_code: 'TSK-STG-03',
            title: 'Implementation Stage 3: Installation & Operator Training',
            description: 'Install mixers, hydraulic press, shredder lines, test electrical interlocks and safety switches, train operators for <200°C curing cycle.',
            department: 'Plant Operations',
            category: 'Machinery & Procurement',
            assigned_to_id: 6,
            assigned_to_name: 'Naubatpur Plant Operations Head',
            priority: 'P1 - High',
            status: 'To Do',
            progress_percentage: 0,
            due_date: '2026-12-25',
            created_by: 'bioronsolutions@gmail.com'
        },
        {
            task_code: 'TSK-STG-04',
            title: 'Implementation Stage 4: Trial Production & Yield Verification',
            description: 'Run controlled trial batches; record actual output, rejects, cycle time and unit COGS to validate the budgeted ₹15/sq ft assumption.',
            department: 'R&D',
            category: 'Production & QC',
            assigned_to_id: 2,
            assigned_to_name: 'Sudip Roy',
            priority: 'P2 - Medium',
            status: 'To Do',
            progress_percentage: 0,
            due_date: '2027-01-15',
            created_by: 'bioronsolutions@gmail.com'
        }
    ];

    const stmtTask = db.prepare(`
        INSERT INTO work_portal_tasks (
            task_code, title, description, department, category,
            assigned_to_id, assigned_to_name, priority, status,
            progress_percentage, due_date, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    tasks.forEach(t => {
        stmtTask.run(
            t.task_code, t.title, t.description, t.department, t.category,
            t.assigned_to_id, t.assigned_to_name, t.priority, t.status,
            t.progress_percentage, t.due_date, t.created_by
        );
    });
    console.log('[Seed] Validated roadmap tasks seeded.');

    // 14. Gmail Messages Log: Cleaned of fake emails!
    db.prepare('DELETE FROM gmail_messages_log').run();
    db.prepare(`
        INSERT INTO gmail_messages_log (
            gmail_message_id, thread_id, team_member_email, sender_name,
            sender_email, recipient_email, subject, snippet, body_content,
            email_date, category, linked_module, is_starred, is_read, action_required
        ) VALUES (
            'MSG-SYS-001',
            'TH-SYS-ADMIN',
            'bioronsolutions@gmail.com',
            'Bioron System Hub',
            'bioronsolutions@gmail.com',
            'bioronsolutions@gmail.com',
            'Bioron Operations Work Portal Live - Ready for Team Gmail Sync',
            'Admin account initialized. Ready to connect and sync official communications for Sudip Roy, Raman Vishwakarma, Shashank Srivastav, and Uttam Kumar.',
            'Bioron Solutions Operations Portal is ready for real communications syncing. When members communicate regarding SIDBI appraisals, supplier machinery quotes, or customer pre-orders, sync them directly into this ledger.',
            '${new Date().toISOString().replace('T', ' ').substring(0, 19)}',
            'Operations & General',
            'Admin Setup',
            1,
            1,
            0
        )
    `).run();
    console.log('[Seed] Gmail log cleared and initialized for bioronsolutions@gmail.com.');

    console.log('[Seed] Data seeding completed successfully with 100% VALIDATED DATA!');
}

if (require.main === module) {
    seedDatabase();
}

module.exports = { seedDatabase };
