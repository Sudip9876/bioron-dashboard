# Bioron Solutions: Operations Database, Executive Board Dashboard & Work Portal

Comprehensive enterprise management system, operational database, and board dashboard built from scratch for **Bioron Solutions Private Limited (BSPL)**, tailored to the **GreenBuild Composite Manufacturing Facility at Korra, Naubatpur, Patna, Bihar**.

---

## 🌟 Executive Document Assessment: Pitch Deck vs. Detailed Project Report (DPR)

### 1. Strategic Alignment & Core Synergies
| Strategic Pillar | Pitch Deck Formulation | Detailed Project Report (DPR) Model | Operational Reconciliation |
| :--- | :--- | :--- | :--- |
| **Technology Platform** | **GreenBuild Composite**: Solid waste (plastics, fly ash, agro-residues, C&D debris) upcycling into tiles & panels. | Cured at **<200°C** (180°C platen temperature vs. 1,100°C–1,300°C traditional kilns), reducing thermal energy by **>75%**. | Full technical continuity. Low-thermal curing is the primary competitive moat allowing a **~55% lower manufacturing cost** and immediate LEED/ESG compliance. |
| **Structural Benchmarks** | Achieved **M30**, targeting **M40**; **<1% water absorption** (impermeable, stain-proof). | Tested at **34.2 MPa to 41.8 MPa**; water absorption at **0.62%–0.74%**; thickness tolerance within **±0.18 mm**. | Exceeds commercial vitrified tile standards (M25–M30), validating application for interior tiles, exterior pavers, and municipal footpaths. |
| **Site & Infrastructure** | Eastern India pilot footprint; decentralized modular micro-plant hub adjacent to urban waste streams. | **Korra, Naubatpur, Patna, Bihar**: 7,000 sq ft plot; 1,000 sq ft enclosed workshed + 2,000 sq ft roofing shed; promoter-funded site preparation (₹4.97 Lakh). | Location provides immediate proximity to Patna Nagar Nigam MRFs, Danapur C&D debris, and rural agricultural residue corridors. |

### 2. Critical Discrepancies & Capital Allocation Nuances
1. **Capital Financing Structure**:
   - **Pitch Deck (Slide 13)**: Proposes a **₹40 Lakhs Seed Round** (Pilot Machinery ₹30L, Waste Sourcing ₹5L, Manpower/Ops ₹5L) to fulfill a ₹1.5 Cr pre-order pipeline.
   - **DPR (Section 6 & 6.3)**: Proposes a **Total Project Cost of ₹87.03 Lakh**, financed through **₹77.71 Lakhs in proposed SIDBI / Bank loan facilities** (Term loan for ₹69.40L machinery + ₹12.66L 90-day working capital) and **₹9.32 Lakhs in Promoter Contribution** (₹4.97L infrastructure + ₹4.35L 5% margin money).
   - *Strategic Takeaway*: The ₹40 Lakh equity/seed round is ideal to fund the promoter equity margin, pilot pre-production tooling, and provide a liquidity buffer during the 6-month loan moratorium before institutional banking disbursement.
2. **Production Capacity & Ramp Phasing**:
   - **Pitch Deck (Slide 9)**: Phase 1 (30k sq ft/mo, 1–3 MT waste/day) $\rightarrow$ Phase 2 (1.2L sq ft/mo, 10–12 MT/day) $\rightarrow$ Phase 3 (3L sq ft/mo, ~30 MT/day).
   - **DPR (Section 8)**: Ramp-up across FY 2026–27 (Nov–Mar: 2.10 Lakh sq ft cumulative, ₹33.81 Lakh revenue) $\rightarrow$ Year 2 (FY 2027–28: 28 Lakh sq ft annual production, 19.6 Lakh sq ft sales @ 70% sell-through, generating **₹450.80 Lakh revenue** and **₹147.45 Lakh EBITDA**).
3. **Unit Economics & Sensitivity**:
   - **DPR Selling Price**: Conservative baseline of **₹23/sq ft** (versus current market prices of ₹27–₹75/sq ft).
   - **DPR Variable Cost / COGS**: Model assumes **₹15/sq ft** (conservative buffer vs. internal detailed workbook cost of ₹10.50/sq ft), yielding a healthy unit contribution of **₹8/sq ft**.
   - **Break-Even**: Operating break-even for Year 2 is **2,55,000 sq ft/year** (21,250 sq ft/month, ₹58.65 Lakh revenue). Cash break-even (including ₹12.74 Lakh annual debt service) is **4,14,250 sq ft/year** (34,521 sq ft/month, ₹95.28 Lakh revenue). Planned sales of 19.6 Lakh sq ft provide a **4.7x cushion** above cash break-even.
4. **Debt Service Coverage Ratio (DSCR)**:
   - Year 1 Ramp DSCR is **0.32x** due to partial 5-month operations and setup expenditure.
   - Year 2 jumps to **8.94x**, stabilizing between **10.70x and 15.39x** in Years 3–5. 
   - *Bank Risk Mitigation*: Must maintain adequate working capital reserves during Year 1 to service the 6-month moratorium interest of ~₹7.74 Lakh.

---

## 🏗️ Operations Database Architecture (`bioron_operations.db`)

The database is built on SQLite (integrated with Node.js and Python) and structured into 12 normalized tables:

```
bioron_operations.db
├── company_profile               # Corporate identity, CIN, PAN, TAN, DIPP, Udyam, GST WB/Bihar
├── team_members                  # Promoters (Sudip Roy, Raman Vishwakarma, etc.), roles, credentials, Gmail states
├── machinery_assets              # 21 capital machines + 11 infrastructure assets (₹74.37L total)
├── feedstock_intake              # Weighbridge logs (Plastics, Fly ash, Agro, C&D), moisture & contamination
├── manufacturing_batches         # 10-Stage batch logs, cure temp (<200°C), press tonnage, scrap & output
├── quality_inspections           # QC logs (M30/M40 MPa, <1% water absorption, warpage, NIT/IIT validation)
├── sales_pipeline_orders         # Commercial pre-orders (PepsiCo, Kalyani Municipality, Smart City, Promoters)
├── financial_mis_ledger          # 5-Year operating projections, EBITDA, PBT, PAT, DSCR
├── loan_amortization_schedule    # 10-Year SIDBI debt amortization (₹77.96L, 10% interest, ₹1.062L EMI)
├── esg_environmental_metrics     # Landfill diversion (MT), plastic upcycled, carbon offset (CO2e), energy saved
├── work_portal_tasks             # Team action items, priorities (P0-P3), categories, progress tracking
└── gmail_messages_log            # Synced communications archive linked to machinery, POs, and banking
```

---

## 🚀 Quick Start Guide

### 1. Run the Web Dashboard
Open your terminal in this directory (`c:\Users\SUDIP ROY\OneDrive\Documents\BioronSolutions\Dashboard`) and run:
```bash
npm start
```
*Or simply double-click:* `scripts\start_dashboard.bat`.

Then open your browser at:
👉 **`http://localhost:3000`**

### 2. Export Board MIS Reports (CSV & Excel ready)
Run the automated Python exporter:
```bash
npm run export
# Or: python scripts/export_mis.py
```
This generates:
- `reports/5_year_projections_mis.csv`
- `reports/sidbi_loan_amortization_schedule.csv`
- `reports/fixed_assets_machinery_register.csv`
- `reports/sales_preorders_pipeline.csv`

---

## 📬 Gmail Integration Setup for Team Members

The portal includes an enterprise-grade communications hub linked to team Gmail addresses:
- **Sudip Roy (CEO)**: `sudroy809@gmail.com`
- **Raman Vishwakarma (CTO/COO)**: `raman.bioron@gmail.com`
- **Shashank Srivastav (COO)**: `shashank.bioron@gmail.com`
- **Uttam Kumar (Investor/Promoter)**: `uttam.kumar.investor@gmail.com`
- **Naubatpur Plant**: `plant.naubatpur@gmail.com`

### Production Integration Options:
1. **Google Cloud Console OAuth 2.0 (Recommended)**:
   - Create a Google Cloud Project with the **Gmail API** enabled.
   - Configure OAuth 2.0 Credentials (Authorized redirect: `http://localhost:3000/auth/google/callback`).
   - Request scopes: `https://www.googleapis.com/auth/gmail.readonly` and `https://www.googleapis.com/auth/gmail.send`.
2. **Google Workspace Service Account (Domain-Wide Delegation)**:
   - For `@bioronsolutions.com` accounts, delegate authority to automatically sync team emails tagged `[SIDBI]`, `[Order]`, `[Supplier]`, or `[Plant]`.
3. **IMAP / App Password Mode**:
   - Individual members generate a Google App Password from their Google Account Security Settings to enable secure automated sync.
