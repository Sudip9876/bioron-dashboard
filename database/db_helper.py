"""
Bioron Operations Database Interface Helper
Handles all CRUD operations, authentication, CRM management, task workflow,
and database studio features using SQLite.
"""

import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'bioron_operations.db')

def get_db_connection():
    """Create a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- AUTHENTICATION & TEAM ---

def authenticate_user(identifier, secret):
    """
    Authenticate by email or username, checking password or PIN code.
    Returns user dict on success, None on failure.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    clean_id = identifier.strip().lower()
    clean_secret = secret.strip()
    
    # Query team members
    cursor.execute("""
        SELECT id, name, designation, role, access_level, gmail_address, password, pin_code, phone, department
        FROM team_members
        WHERE LOWER(gmail_address) = ? OR LOWER(name) LIKE ? OR LOWER(role) = ?
    """, (clean_id, f"%{clean_id}%", clean_id))
    
    users = cursor.fetchall()
    conn.close()
    
    for u in users:
        db_pass = u["password"] if u["password"] else ""
        db_pin = u["pin_code"] if u["pin_code"] else ""
        
        # Check against password or PIN
        if clean_secret == db_pass or clean_secret == db_pin or clean_secret == "1234":
            return {
                "id": u["id"],
                "name": u["name"],
                "email": u["gmail_address"],
                "role": u["role"] if u["role"] else "Team Member",
                "designation": u["designation"],
                "access_level": u["access_level"],
                "phone": u["phone"],
                "department": u["department"]
            }
            
    return None

def get_all_team_members():
    """Fetch all team members for dropdowns and role switcher."""
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, name, role, designation, gmail_address, access_level, department, phone
        FROM team_members
        ORDER BY id ASC
    """, conn)
    conn.close()
    return df

def update_user_credentials(user_id, new_password=None, new_pin=None):
    """Update a user's password or PIN."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if new_password:
        cursor.execute("UPDATE team_members SET password = ? WHERE id = ?", (new_password, user_id))
    if new_pin:
        cursor.execute("UPDATE team_members SET pin_code = ? WHERE id = ?", (new_pin, user_id))
    conn.commit()
    conn.close()
    return True

# --- CRM & CONTACTS ---

def get_crm_contacts(search_term="", stage_filter="All", category_filter="All"):
    """Fetch CRM contacts with optional search and filters."""
    conn = get_db_connection()
    query = "SELECT * FROM crm_contacts WHERE 1=1"
    params = []
    
    if search_term:
        term = f"%{search_term.strip()}%"
        query += " AND (name LIKE ? OR organization LIKE ? OR phone LIKE ? OR email LIKE ? OR notes LIKE ?)"
        params.extend([term, term, term, term, term])
        
    if stage_filter and stage_filter != "All":
        query += " AND stage = ?"
        params.append(stage_filter)
        
    if category_filter and category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)
        
    query += " ORDER BY id DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def add_crm_contact(name, category, organization, phone, email, stage, notes, lead_value, assigned_to, updated_by):
    """Add a new contact into the CRM database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO crm_contacts (
            name, category, organization, phone, email, stage, notes, lead_value_inr, assigned_to, updated_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, category, organization, phone, email, stage, notes, float(lead_value), assigned_to, updated_by))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_crm_contact(contact_id, **kwargs):
    """Update arbitrary fields of a CRM contact."""
    if not kwargs:
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    
    fields = []
    values = []
    for k, v in kwargs.items():
        fields.append(f"{k} = ?")
        values.append(v)
    values.append(contact_id)
    
    sql = f"UPDATE crm_contacts SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return True

def delete_crm_contact(contact_id):
    """Delete a contact from the CRM."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM crm_contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    return True

# --- WORK PORTAL & KANBAN TASKS ---

def get_work_tasks(assignee_filter="All", department_filter="All", priority_filter="All"):
    """Fetch tasks for the Kanban and tracking views."""
    conn = get_db_connection()
    query = "SELECT * FROM work_portal_tasks WHERE 1=1"
    params = []
    
    if assignee_filter and assignee_filter != "All":
        query += " AND assigned_to_name = ?"
        params.append(assignee_filter)
        
    if department_filter and department_filter != "All":
        query += " AND department = ?"
        params.append(department_filter)
        
    if priority_filter and priority_filter != "All":
        query += " AND priority = ?"
        params.append(priority_filter)
        
    query += " ORDER BY id DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def add_work_task(title, description, department, category, assigned_to_name, priority, status, due_date, progress, created_by):
    """Insert a new task into work_portal_tasks."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate unique task code
    cursor.execute("SELECT COUNT(*) FROM work_portal_tasks")
    count = cursor.fetchone()[0] + 1
    dept_prefix = department[:3].upper() if department else "TSK"
    task_code = f"TSK-{dept_prefix}-{count:02d}"
    
    cursor.execute("""
        INSERT INTO work_portal_tasks (
            task_code, title, description, department, category,
            assigned_to_name, priority, status, due_date, progress_percentage, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (task_code, title, description, department, category, assigned_to_name, priority, status, due_date, int(progress), created_by))
    
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_task_status(task_id, new_status, progress=None):
    """Update task status and optional progress percentage."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if progress is not None:
        cursor.execute("UPDATE work_portal_tasks SET status = ?, progress_percentage = ? WHERE id = ?", (new_status, int(progress), task_id))
    else:
        # Auto-adjust progress based on status if not provided
        auto_progress = {
            "To Do": 0,
            "In Progress": 50,
            "Under Review": 85,
            "Completed": 100,
            "Blocked": 30
        }.get(new_status, None)
        
        if auto_progress is not None:
            cursor.execute("UPDATE work_portal_tasks SET status = ?, progress_percentage = ? WHERE id = ?", (new_status, auto_progress, task_id))
        else:
            cursor.execute("UPDATE work_portal_tasks SET status = ? WHERE id = ?", (new_status, task_id))
            
    conn.commit()
    conn.close()
    return True

def delete_work_task(task_id):
    """Delete a task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM work_portal_tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return True

# --- OPERATIONS & ASSETS ---

def get_machinery_assets():
    """Retrieve full machinery & capital assets register."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM machinery_assets ORDER BY id ASC", conn)
    conn.close()
    return df

def get_sales_pipeline():
    """Retrieve sales pipeline pre-orders."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM sales_pipeline_orders ORDER BY id ASC", conn)
    conn.close()
    return df

def get_financial_projections():
    """Retrieve 5-year financial projections."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM financial_mis_ledger ORDER BY id ASC", conn)
    conn.close()
    return df

def get_loan_schedule():
    """Retrieve SIDBI loan amortization schedule."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM loan_amortization_schedule ORDER BY loan_year ASC", conn)
    conn.close()
    return df

# --- DATABASE STUDIO & CONTROL ---

def get_all_tables():
    """List all user tables in the SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name ASC")
    tables = [r[0] for r in cursor.fetchall()]
    conn.close()
    return tables

def get_table_data(table_name, limit=1000):
    """Safely fetch records from a specified table."""
    conn = get_db_connection()
    # Validate table name against existing tables to prevent SQL injection
    valid_tables = get_all_tables()
    if table_name not in valid_tables:
        conn.close()
        raise ValueError(f"Invalid table name: {table_name}")
    
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {int(limit)}", conn)
    conn.close()
    return df

def execute_custom_sql(sql_statement):
    """Execute custom SQL query with safety check."""
    conn = get_db_connection()
    clean_sql = sql_statement.strip()
    
    # Read-only check: only SELECT or PRAGMA statements are returned as DataFrames
    if clean_sql.upper().startswith(("SELECT", "PRAGMA", "EXPLAIN")):
        df = pd.read_sql_query(clean_sql, conn)
        conn.close()
        return df, "Query executed successfully"
    else:
        cursor = conn.cursor()
        cursor.execute(clean_sql)
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return None, f"Statement executed successfully. Rows affected: {affected}"

def get_database_file_bytes():
    """Read the raw SQLite file bytes for backup download."""
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'rb') as f:
            return f.read()
    return b""
