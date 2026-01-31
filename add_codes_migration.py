"""
Add entry_code and exit_code columns to database
"""

import sqlite3
import os

def add_codes_columns():
    """Add entry_code and exit_code columns"""
    db_path = 'visitor_management.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Adding entry_code and exit_code columns...")
    print("-" * 60)
    
    # Add entry_code column
    try:
        cursor.execute("ALTER TABLE visitors ADD COLUMN entry_code VARCHAR(4)")
        print("✅ Added column: entry_code")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("⚠️  Column already exists: entry_code")
        else:
            print(f"❌ Error: {str(e)}")
    
    # Add exit_code column
    try:
        cursor.execute("ALTER TABLE visitors ADD COLUMN exit_code VARCHAR(4)")
        print("✅ Added column: exit_code")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("⚠️  Column already exists: exit_code")
        else:
            print(f"❌ Error: {str(e)}")
    
    conn.commit()
    conn.close()
    
    print("-" * 60)
    print("✅ Migration completed!")
    print("\nYou can now run: python app.py")

if __name__ == '__main__':
    add_codes_columns()