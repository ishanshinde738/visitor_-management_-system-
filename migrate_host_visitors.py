"""
Database Migration Script for Host Visitors
Adds face recognition columns to host_visitors table
"""

import sqlite3
import os

def migrate_host_visitors_table():
    """Add face_image_path and face_encoding columns to host_visitors table"""
    
    db_path = 'visitor_management.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        print("Please run this script from the project root directory")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Checking host_visitors table...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(host_visitors)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"📋 Current columns: {', '.join(columns)}")
        
        # Add face_image_path column if it doesn't exist
        if 'face_image_path' not in columns:
            print("➕ Adding face_image_path column...")
            cursor.execute("ALTER TABLE host_visitors ADD COLUMN face_image_path VARCHAR(255)")
            print("   ✅ face_image_path added")
        else:
            print("   ℹ️  face_image_path already exists")
        
        # Add face_encoding column if it doesn't exist
        if 'face_encoding' not in columns:
            print("➕ Adding face_encoding column...")
            cursor.execute("ALTER TABLE host_visitors ADD COLUMN face_encoding TEXT")
            print("   ✅ face_encoding added")
        else:
            print("   ℹ️  face_encoding already exists")
        
        # Commit changes
        conn.commit()
        
        # Verify columns were added
        cursor.execute("PRAGMA table_info(host_visitors)")
        updated_columns = [row[1] for row in cursor.fetchall()]
        
        print("\n✅ Migration completed successfully!")
        print(f"📋 Updated columns: {', '.join(updated_columns)}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 70)
    print("🗄️  HOST VISITORS TABLE MIGRATION")
    print("=" * 70)
    print()
    
    success = migrate_host_visitors_table()
    
    print()
    print("=" * 70)
    if success:
        print("✅ MIGRATION SUCCESSFUL")
        print("You can now restart your Flask application")
    else:
        print("❌ MIGRATION FAILED")
        print("Please check the errors above")
    print("=" * 70)