import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'styles'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import db_helper

def test_db_queries():
    print("Testing get_crm_contacts...")
    crm = db_helper.get_crm_contacts()
    assert len(crm) >= 239, f"Expected at least 239 contacts, got {len(crm)}"
    print(f"CRM contacts loaded: {len(crm)}")

    print("Testing get_work_tasks...")
    tasks = db_helper.get_work_tasks()
    assert len(tasks) > 0, "Tasks should not be empty"
    print(f"Tasks loaded: {len(tasks)}")

    print("Testing get_machinery_assets...")
    mach = db_helper.get_machinery_assets()
    assert len(mach) > 0, "Machinery should not be empty"
    print(f"Machinery assets loaded: {len(mach)}")

    print("Testing get_financial_projections...")
    fin = db_helper.get_financial_projections()
    assert len(fin) > 0, "Financial projections should not be empty"
    print(f"Financial projections loaded: {len(fin)}")

    print("Testing get_sales_pipeline...")
    sales = db_helper.get_sales_pipeline()
    assert len(sales) > 0, "Sales pipeline should not be empty"
    print(f"Sales pipeline loaded: {len(sales)}")

    print("Testing authentication for all 4 required roles...")
    creds = [
        ("bioronsolutions@gmail.com", "adminpassword123", "Admin"),
        ("sudroy809@gmail.com", "bioronceo2026", "CEO"),
        ("Raman.vishwa1581@gmail.com", "bioroncto2026", "CTO"),
        ("shashanksrivastav954@gmail.com", "bioroncoo2026", "COO")
    ]
    for email, pw, role in creds:
        u = db_helper.authenticate_user(email, pw)
        assert u is not None, f"Failed to authenticate {email}"
        print(f"Authenticated {email} as {u['role']} ({u['name']})")

    print("\nAll database & business logic tests passed successfully!")

if __name__ == '__main__':
    test_db_queries()
