"""
Standalone Database Migration - Add Role Column to Hosts
========================================================

This script uses ONLY Python's built-in sqlite3 module.
No Flask, no SQLAlchemy, no dependencies.

Safe to run multiple times - checks if column exists first.
"""

import sqlite3
import os
import sys

def add_role_column_to_hosts():
    """Add role column to hosts table"""
    
    print("\n" + "=" * 80)
    print("🔧 STANDALONE DATABASE MIGRATION")
    print("   Adding 'role' column to hosts table")
    print("=" * 80)
    
    # Find database file
    db_path = 'visitor_management.db'
    
    if not os.path.exists(db_path):
        print(f"\n❌ ERROR: Database file '{db_path}' not found!")
        print(f"   Current directory: {os.getcwd()}")
        print("\n   Please run this script from your project root directory.")
        return False
    
    print(f"\n✅ Found database: {db_path}")
    print(f"   Size: {os.path.getsize(db_path)} bytes")
    
    try:
        # Connect to database
        print("\n📊 Connecting to database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("   ✅ Connected successfully")
        
        # Check if hosts table exists
        print("\n🔍 Checking if 'hosts' table exists...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hosts'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("   ❌ ERROR: 'hosts' table does not exist!")
            print("   The database may not be initialized properly.")
            conn.close()
            return False
        
        print("   ✅ 'hosts' table exists")
        
        # Get current table structure
        print("\n📋 Current 'hosts' table structure:")
        cursor.execute("PRAGMA table_info(hosts)")
        columns = cursor.fetchall()
        
        column_names = []
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            column_names.append(col_name)
            print(f"   - {col_name} ({col_type})")
        
        # Check if role column already exists
        if 'role' in column_names:
            print("\n✅ 'role' column ALREADY EXISTS!")
            print("   No migration needed.")
            
            # Show current hosts with role
            print("\n📋 Current hosts in database:")
            cursor.execute("SELECT username, email, role, is_approved, is_active FROM hosts")
            hosts = cursor.fetchall()
            
            if hosts:
                for i, (username, email, role, is_approved, is_active) in enumerate(hosts, 1):
                    print(f"\n   {i}. Username: {username}")
                    print(f"      Email: {email}")
                    print(f"      Role: {role if role else '(NULL)'}")
                    print(f"      Approved: {'Yes' if is_approved else 'No'}")
                    print(f"      Active: {'Yes' if is_active else 'No'}")
            else:
                print("   (No hosts found)")
            
            conn.close()
            
            print("\n" + "=" * 80)
            print("✅ MIGRATION NOT NEEDED - Column already exists")
            print("=" * 80)
            print("\n💡 Next step: Restart your Flask application")
            print("   Command: python app.py")
            print("\n" + "=" * 80 + "\n")
            
            return True
        
        # Add role column
        print("\n🔧 Adding 'role' column to 'hosts' table...")
        
        try:
            cursor.execute("ALTER TABLE hosts ADD COLUMN role VARCHAR(20)")
            conn.commit()
            print("   ✅ Column added successfully (without default)")
        except sqlite3.OperationalError as e:
            print(f"   ⚠️  Column add without default failed: {e}")
            print("   Trying alternative method...")
            
            # Try with default value
            try:
                cursor.execute("ALTER TABLE hosts ADD COLUMN role VARCHAR(20) DEFAULT 'host'")
                conn.commit()
                print("   ✅ Column added successfully (with default)")
            except sqlite3.OperationalError as e2:
                print(f"   ❌ ERROR: Could not add column: {e2}")
                conn.close()
                return False
        
        # Update all existing hosts to have role='host'
        print("\n📝 Setting role='host' for all existing hosts...")
        cursor.execute("UPDATE hosts SET role = 'host' WHERE role IS NULL OR role = ''")
        updated_count = cursor.rowcount
        conn.commit()
        print(f"   ✅ Updated {updated_count} host record(s)")
        
        # Verify the migration
        print("\n✅ Verifying migration...")
        
        # Check total hosts
        cursor.execute("SELECT COUNT(*) FROM hosts")
        total_hosts = cursor.fetchone()[0]
        print(f"   Total hosts in database: {total_hosts}")
        
        # Check hosts with role='host'
        cursor.execute("SELECT COUNT(*) FROM hosts WHERE role = 'host'")
        hosts_with_role = cursor.fetchone()[0]
        print(f"   Hosts with role='host': {hosts_with_role}")
        
        if total_hosts == hosts_with_role:
            print("   ✅ All hosts have correct role!")
        else:
            print(f"   ⚠️  Warning: {total_hosts - hosts_with_role} hosts without role")
        
        # Display current hosts
        print("\n📋 Updated hosts in database:")
        cursor.execute("SELECT username, email, role, is_approved, is_active FROM hosts")
        hosts = cursor.fetchall()
        
        if hosts:
            for i, (username, email, role, is_approved, is_active) in enumerate(hosts, 1):
                print(f"\n   {i}. Username: {username}")
                print(f"      Email: {email}")
                print(f"      Role: {role}")
                print(f"      Approved: {'✅ Yes' if is_approved else '❌ No'}")
                print(f"      Active: {'✅ Yes' if is_active else '❌ No'}")
        else:
            print("   (No hosts found)")
        
        # Verify column was added
        print("\n🔍 Final verification - checking table structure...")
        cursor.execute("PRAGMA table_info(hosts)")
        final_columns = cursor.fetchall()
        final_column_names = [col[1] for col in final_columns]
        
        if 'role' in final_column_names:
            print("   ✅ 'role' column confirmed in table structure")
        else:
            print("   ❌ ERROR: 'role' column not found after migration!")
            conn.close()
            return False
        
        # Close connection
        conn.close()
        
        print("\n" + "=" * 80)
        print("🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\n📝 Summary of changes:")
        print("   ✅ Added 'role' column to 'hosts' table")
        print("   ✅ Set role='host' for all existing hosts")
        print(f"   ✅ Updated {updated_count} host record(s)")
        print("\n🚀 Next steps:")
        print("   1. Restart your Flask application")
        print("      Command: python app.py")
        print("   2. Try host login again")
        print("   3. Should work without errors!")
        print("\n" + "=" * 80 + "\n")
        
        return True
        
    except sqlite3.Error as e:
        print(f"\n❌ SQLite Error: {e}")
        print("   Migration failed!")
        if 'conn' in locals():
            conn.close()
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print("   Migration failed!")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("⚠️  IMPORTANT NOTES")
    print("=" * 80)
    print("\nThis script will:")
    print("  1. Check if 'role' column exists in 'hosts' table")
    print("  2. Add 'role' column if it doesn't exist")
    print("  3. Set role='host' for all existing hosts")
    print("  4. Verify the changes")
    print("\nThis is a safe operation that won't delete any data.")
    print("\n" + "=" * 80)
    
    # Ask for confirmation
    response = input("\nProceed with migration? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        success = add_role_column_to_hosts()
        
        if success:
            print("\n✅ SUCCESS! Migration completed.")
            print("   You can now restart Flask and test host login.")
            sys.exit(0)
        else:
            print("\n❌ FAILED! Migration encountered errors.")
            print("   Please check the error messages above.")
            sys.exit(1)
    else:
        print("\n⚠️  Migration cancelled by user.")
        sys.exit(0)