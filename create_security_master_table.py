"""
Database Migration: Create Security Master Table
This creates a comprehensive visitor tracking table with status columns
"""

import sqlite3
from datetime import datetime

# SQL to create the security_master table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS security_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Visitor Information
    visitor_name VARCHAR(100) NOT NULL,
    company VARCHAR(100),
    contact_number VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    
    -- Host Information
    host_name VARCHAR(100) NOT NULL,
    host_contact VARCHAR(15),
    host_email VARCHAR(100),
    
    -- Visit Details
    visit_date DATE NOT NULL,
    visit_time TIME NOT NULL,
    purpose TEXT,
    
    -- E-Pass and Security Codes
    epass_id VARCHAR(20) UNIQUE,
    entry_code VARCHAR(10),
    exit_code VARCHAR(10),
    
    -- Status Tracking Columns
    host_approval_status VARCHAR(50) DEFAULT 'Waiting for Host Approval',
    check_in_status VARCHAR(50) DEFAULT NULL,
    checkout_status VARCHAR(50) DEFAULT NULL,
    
    -- Timestamps
    check_in_time DATETIME DEFAULT NULL,
    check_out_time DATETIME DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Photo path
    photo_path VARCHAR(255),
    
    -- Additional fields
    remarks TEXT,
    
    -- Constraints
    CHECK (host_approval_status IN ('Waiting for Host Approval', 'Approved by Host')),
    CHECK (check_in_status IN ('Check in pending at security', 'Check in completed') OR check_in_status IS NULL),
    CHECK (checkout_status IN ('Checkout pending', 'Checkout completed') OR checkout_status IS NULL)
);
"""

# Create indexes for faster queries
CREATE_INDEXES_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_host_approval_status ON security_master(host_approval_status);",
    "CREATE INDEX IF NOT EXISTS idx_check_in_status ON security_master(check_in_status);",
    "CREATE INDEX IF NOT EXISTS idx_checkout_status ON security_master(checkout_status);",
    "CREATE INDEX IF NOT EXISTS idx_visit_date ON security_master(visit_date);",
    "CREATE INDEX IF NOT EXISTS idx_created_at ON security_master(created_at);"
]

def run_migration(db_path='visitor_management.db'):
    """
    Run the database migration
    """
    print("=" * 70)
    print("🔄 DATABASE MIGRATION - Security Master Table")
    print("=" * 70)
    print()
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"✅ Connected to database: {db_path}")
        
        # Check if table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='security_master';
        """)
        
        if cursor.fetchone():
            print("⚠️  Table 'security_master' already exists")
            response = input("Do you want to drop and recreate it? (yes/no): ").strip().lower()
            
            if response in ['yes', 'y']:
                cursor.execute("DROP TABLE security_master;")
                print("✅ Dropped existing table")
            else:
                print("❌ Migration cancelled")
                conn.close()
                return
        
        # Create table
        print("\n📋 Creating 'security_master' table...")
        cursor.execute(CREATE_TABLE_SQL)
        print("✅ Table created successfully")
        
        # Create indexes
        print("\n📊 Creating indexes...")
        for index_sql in CREATE_INDEXES_SQL:
            cursor.execute(index_sql)
        print("✅ Indexes created successfully")
        
        # Commit changes
        conn.commit()
        
        # Verify table structure
        print("\n🔍 Verifying table structure...")
        cursor.execute("PRAGMA table_info(security_master);")
        columns = cursor.fetchall()
        
        print(f"\n✅ Table created with {len(columns)} columns:")
        print("-" * 70)
        for col in columns:
            print(f"  {col[1]:<30} {col[2]:<20}")
        print("-" * 70)
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\n💡 Next steps:")
        print("  1. Update your models.py to use security_master table")
        print("  2. Update routes to handle new status columns")
        print("  3. Test the status flow")
        
    except sqlite3.Error as e:
        print(f"\n❌ Database Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    import sys
    
    # Check if custom database path provided
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'visitor_management.db'
    
    print(f"📂 Using database: {db_path}\n")
    
    success = run_migration(db_path)
    
    if success:
        print("\n✅ Migration complete! Your database is ready.")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
    
    input("\nPress Enter to exit...")