import sqlite3
import os
from crm_initial_data import INITIAL_CRM_CONTACTS

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'bioron_operations.db')

def init_portal_database():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create crm_contacts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crm_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        organization TEXT,
        phone TEXT,
        email TEXT,
        stage TEXT DEFAULT 'Contacted',
        notes TEXT,
        lead_value_inr REAL DEFAULT 0.0,
        assigned_to TEXT DEFAULT 'Sudip Roy',
        updated_by TEXT DEFAULT 'Data Import',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Check count of crm_contacts
    cursor.execute("SELECT COUNT(*) FROM crm_contacts")
    existing_contacts_count = cursor.fetchone()[0]
    print(f"Current CRM contacts count: {existing_contacts_count}")

    if existing_contacts_count == 0:
        print(f"Seeding {len(INITIAL_CRM_CONTACTS)} CRM contacts into database...")
        for c in INITIAL_CRM_CONTACTS:
            cursor.execute("""
            INSERT INTO crm_contacts (
                name, category, organization, phone, email, stage, notes, updated_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c.get("Name", "Unknown"),
                c.get("Category", "Connection / Network"),
                c.get("Organization", "Network / Warm Contacts"),
                c.get("Phone", ""),
                c.get("Email", ""),
                c.get("Stage", "Contacted"),
                c.get("Notes", ""),
                c.get("Updated By", "Data Import")
            ))
        print("CRM contacts seeded successfully.")

    # 2. Update team_members table schema
    cursor.execute("PRAGMA table_info(team_members)")
    cols = [col[1] for col in cursor.fetchall()]

    if "password" not in cols:
        print("Adding 'password' column to team_members...")
        cursor.execute("ALTER TABLE team_members ADD COLUMN password TEXT DEFAULT 'bioron2026';")

    if "role" not in cols:
        print("Adding 'role' column to team_members...")
        cursor.execute("ALTER TABLE team_members ADD COLUMN role TEXT DEFAULT 'Director';")

    # Update or insert required executive users:
    # Admin	bioronsolutions@gmail.com
    # CEO	sudroy809@gmail.com
    # CTO	Raman.vishwa1581@gmail.com
    # COO	shashanksrivastav954@gmail.com
    
    users_to_sync = [
        {
            "name": "System Administrator",
            "email": "bioronsolutions@gmail.com",
            "role": "Admin",
            "designation": "Master Administrator & Operations Controller",
            "password": "adminpassword123",
            "pin": "1234",
            "access_level": "SuperAdmin",
            "phone": "+91 8981922296"
        },
        {
            "name": "Sudip Roy",
            "email": "sudroy809@gmail.com",
            "role": "CEO",
            "designation": "Chief Executive Officer (Promoter 1)",
            "password": "bioronceo2026",
            "pin": "1234",
            "access_level": "SuperAdmin",
            "phone": "+91 8981922296"
        },
        {
            "name": "Raman Vishwakarma",
            "email": "Raman.vishwa1581@gmail.com",
            "role": "CTO",
            "designation": "Chief Technical Officer (Promoter 2)",
            "password": "bioroncto2026",
            "pin": "1234",
            "access_level": "Executive User",
            "phone": "+91 8981922296"
        },
        {
            "name": "Shashank Srivastav",
            "email": "shashanksrivastav954@gmail.com",
            "role": "COO",
            "designation": "Chief Operating Officer (Promoter 3)",
            "password": "bioroncoo2026",
            "pin": "1234",
            "access_level": "Executive User",
            "phone": "+91 8981922296"
        }
    ]

    for u in users_to_sync:
        # Check if email exists
        cursor.execute("SELECT id FROM team_members WHERE LOWER(gmail_address) = LOWER(?)", (u["email"],))
        row = cursor.fetchone()
        if row:
            cursor.execute("""
            UPDATE team_members SET 
                name = ?, role = ?, designation = ?, password = ?, pin_code = ?, access_level = ?
            WHERE id = ?
            """, (u["name"], u["role"], u["designation"], u["password"], u["pin"], u["access_level"], row[0]))
            print(f"Updated user {u['email']} (ID: {row[0]})")
        else:
            # Check by role/name fallback (e.g. previous raman.bioron@gmail.com)
            if u["role"] == "CTO":
                cursor.execute("SELECT id FROM team_members WHERE LOWER(gmail_address) = 'raman.bioron@gmail.com'")
                old_row = cursor.fetchone()
                if old_row:
                    cursor.execute("""
                    UPDATE team_members SET 
                        gmail_address = ?, name = ?, role = ?, designation = ?, password = ?, pin_code = ?
                    WHERE id = ?
                    """, (u["email"], u["name"], u["role"], u["designation"], u["password"], u["pin"], old_row[0]))
                    print(f"Updated CTO email to {u['email']} (ID: {old_row[0]})")
                    continue

            if u["role"] == "COO":
                cursor.execute("SELECT id FROM team_members WHERE LOWER(gmail_address) = 'shashank.bioron@gmail.com'")
                old_row = cursor.fetchone()
                if old_row:
                    cursor.execute("""
                    UPDATE team_members SET 
                        gmail_address = ?, name = ?, role = ?, designation = ?, password = ?, pin_code = ?
                    WHERE id = ?
                    """, (u["email"], u["name"], u["role"], u["designation"], u["password"], u["pin"], old_row[0]))
                    print(f"Updated COO email to {u['email']} (ID: {old_row[0]})")
                    continue

            # Otherwise insert fresh
            cursor.execute("""
            INSERT INTO team_members (
                name, designation, role_category, department, pin_code, access_level,
                phone, gmail_address, password, role
            ) VALUES (?, ?, 'Executive', 'BSPL Board', ?, ?, ?, ?, ?, ?)
            """, (u["name"], u["designation"], u["pin"], u["access_level"], u["phone"], u["email"], u["password"], u["role"]))
            print(f"Inserted new user {u['email']}")

    # 3. Verify work_portal_tasks has proper tasks
    cursor.execute("SELECT COUNT(*) FROM work_portal_tasks")
    task_count = cursor.fetchone()[0]
    print(f"Current tasks count: {task_count}")

    conn.commit()
    conn.close()
    print("Database initialization and migration completed successfully!")

if __name__ == '__main__':
    init_portal_database()
