"""
Bioron Solutions Private Limited (BSPL)
Monthly Management Information System (MIS) & Board Report Exporter
Connects to bioron_operations.db and exports clean CSV summaries for Board meetings and SIDBI filings.
"""

import sqlite3
import csv
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'bioron_operations.db')
OUTPUT_DIR = os.path.join(BASE_DIR, 'reports')

def export_mis():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=================================================================")
    print("BIORON SOLUTIONS PRIVATE LIMITED - BOARD MIS EXPORTER")
    print("Facility: Korra, Naubatpur, Patna, Bihar")
    print("=================================================================")

    # 1. Export 5-Year Financial Projections (DPR Tables 1 & 2)
    fin_file = os.path.join(OUTPUT_DIR, '5_year_projections_mis.csv')
    cursor.execute("SELECT * FROM financial_mis_ledger ORDER BY id ASC")
    rows = cursor.fetchall()
    if rows:
        with open(fin_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([d[0] for d in cursor.description])
            for r in rows:
                writer.writerow(list(r))
        print(f"[✓] Exported: {fin_file}")

    # 2. Export 10-Year SIDBI Loan Repayment Schedule
    loan_file = os.path.join(OUTPUT_DIR, 'sidbi_loan_amortization_schedule.csv')
    cursor.execute("SELECT * FROM loan_amortization_schedule ORDER BY loan_year ASC")
    rows = cursor.fetchall()
    if rows:
        with open(loan_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([d[0] for d in cursor.description])
            for r in rows:
                writer.writerow(list(r))
        print(f"[✓] Exported: {loan_file}")

    # 3. Export Machinery & Capital Asset Register
    asset_file = os.path.join(OUTPUT_DIR, 'fixed_assets_machinery_register.csv')
    cursor.execute("SELECT * FROM machinery_assets ORDER BY id ASC")
    rows = cursor.fetchall()
    if rows:
        with open(asset_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([d[0] for d in cursor.description])
            for r in rows:
                writer.writerow(list(r))
        print(f"[✓] Exported: {asset_file}")

    # 4. Export Sales Orders & Pre-Order Pipeline
    pipeline_file = os.path.join(OUTPUT_DIR, 'sales_preorders_pipeline.csv')
    cursor.execute("SELECT * FROM sales_pipeline_orders ORDER BY total_order_value DESC")
    rows = cursor.fetchall()
    if rows:
        with open(pipeline_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([d[0] for d in cursor.description])
            for r in rows:
                writer.writerow(list(r))
        print(f"[✓] Exported: {pipeline_file}")

    conn.close()
    print("=================================================================")
    print(f"All reports successfully generated in: {OUTPUT_DIR}")
    print("=================================================================")

if __name__ == '__main__':
    export_mis()
