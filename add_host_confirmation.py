"""
Add host confirmation fields to database
"""

import sqlite3
import os

def add_host_confirmation_fields():
    """Add host confirmation columns"""
    db_path = 'visitor_management.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Adding host confirmation fields...")
    print("-" * 60)
    
    columns_to_add = [
        ("host_confirmation", "VARCHAR(20) DEFAULT 'pending'"),
        ("host_confirmation_reason", "TEXT"),
        ("host_confirmation_time", "DATETIME"),
    ]
    
    for column_name, column_type in columns_to_add:
        try:
            sql = f"ALTER TABLE visitors ADD COLUMN {column_name} {column_type}"
            cursor.execute(sql)
            print(f"✅ Added column: {column_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"⚠️  Column already exists: {column_name}")
            else:
                print(f"❌ Error: {str(e)}")
    
    conn.commit()
    conn.close()
    
    print("-" * 60)
    print("✅ Migration completed!")
    print("\nYou can now run: python app.py")

if __name__ == '__main__':
    add_host_confirmation_fields()