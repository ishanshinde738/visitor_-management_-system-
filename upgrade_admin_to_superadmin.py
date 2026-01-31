"""
Upgrade Admin to Superadmin Script
===================================

This script upgrades the admin user's role from 'admin' to 'superadmin'
allowing access to User Management features.

Safe to run - only updates the admin user's role field.
"""

import sqlite3
import os

def upgrade_admin_to_superadmin():
    """Upgrade admin user role from 'admin' to 'superadmin'"""
    
    print("\n" + "=" * 80)
    print("🔧 UPGRADE ADMIN TO SUPERADMIN")
    print("=" * 80)
    
    # Database path
    db_path = 'visitor_management.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"\n❌ ERROR: Database file '{db_path}' not found!")
        print(f"   Current directory: {os.getcwd()}")
        print("   Please run this script from your project root directory.")
        return False
    
    print(f"\n✅ Found database: {db_path}")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("✅ Connected to database")
        
        # Step 1: Check current admin users
        print("\n📊 Step 1: Checking current admin users...")
        cursor.execute("SELECT id, username, email, role, is_active FROM users WHERE username = 'admin'")
        admin_users = cursor.fetchall()
        
        if not admin_users:
            print("\n❌ ERROR: No admin user found with username 'admin'!")
            print("   Please make sure admin user exists in database.")
            conn.close()
            return False
        
        print(f"   Found {len(admin_users)} user(s) with username 'admin':")
        
        for user_id, username, email, role, is_active in admin_users:
            print(f"\n   User ID: {user_id}")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            print(f"   Current Role: {role}")
            print(f"   Active: {'Yes' if is_active else 'No'}")
        
        # Step 2: Check if already superadmin
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin' AND role = 'superadmin'")
        already_superadmin = cursor.fetchone()[0]
        
        if already_superadmin > 0:
            print("\n✅ Admin user is ALREADY a superadmin!")
            print("   No changes needed.")
            print("\n💡 You can now access User Management with admin account.")
            conn.close()
            return True
        
        # Step 3: Upgrade to superadmin
        print("\n🔧 Step 2: Upgrading admin role to superadmin...")
        
        cursor.execute("UPDATE users SET role = 'superadmin' WHERE username = 'admin' AND role = 'admin'")
        rows_updated = cursor.rowcount
        conn.commit()
        
        if rows_updated > 0:
            print(f"   ✅ Successfully updated {rows_updated} admin user(s) to superadmin")
        else:
            print("   ⚠️  No rows updated - admin may already be superadmin or not exist")
        
        # Step 4: Verify the change
        print("\n✅ Step 3: Verifying the upgrade...")
        
        cursor.execute("SELECT id, username, email, role, is_active FROM users WHERE username = 'admin'")
        updated_users = cursor.fetchall()
        
        print("   Updated admin user details:")
        for user_id, username, email, role, is_active in updated_users:
            print(f"\n   User ID: {user_id}")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            print(f"   New Role: {role}")
            print(f"   Active: {'Yes' if is_active else 'No'}")
        
        # Step 5: Show all superadmins
        print("\n📋 Step 4: All superadmin users in system:")
        cursor.execute("SELECT username, email, role FROM users WHERE role = 'superadmin'")
        all_superadmins = cursor.fetchall()
        
        if all_superadmins:
            for username, email, role in all_superadmins:
                print(f"   - {username} ({email}) - Role: {role}")
        else:
            print("   (No superadmin users found)")
        
        # Close connection
        conn.close()
        
        print("\n" + "=" * 80)
        print("🎉 UPGRADE COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        print("\n📝 Summary of changes:")
        print(f"   ✅ Updated {rows_updated} admin user(s) to superadmin role")
        print("   ✅ Admin can now access User Management")
        
        print("\n🚀 Next steps:")
        print("   1. Restart your Flask application (if running)")
        print("      Command: python app.py")
        print("   2. Login as admin (admin/admin123)")
        print("   3. Go to Admin Panel → User Management")
        print("   4. You should now have full access! ✅")
        
        print("\n💡 Login credentials remain the same:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Role: superadmin (upgraded from admin)")
        
        print("\n" + "=" * 80 + "\n")
        
        return True
        
    except sqlite3.Error as e:
        print(f"\n❌ SQLite Error: {e}")
        if conn:
            conn.close()
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        if conn:
            conn.close()
        return False

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("⚠️  ADMIN TO SUPERADMIN UPGRADE SCRIPT")
    print("=" * 80)
    print("\nThis script will:")
    print("  1. Find the admin user (username='admin')")
    print("  2. Upgrade their role from 'admin' to 'superadmin'")
    print("  3. Verify the change")
    print("\nThis allows admin to access User Management features.")
    print("\n✅ Safe operation - only updates the role field")
    print("✅ Login credentials remain unchanged (admin/admin123)")
    print("\n" + "=" * 80)
    
    response = input("\nProceed with upgrade? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        success = upgrade_admin_to_superadmin()
        
        if success:
            print("\n✅ SUCCESS! Admin upgraded to superadmin.")
            print("   Restart Flask and login to access User Management.")
        else:
            print("\n❌ FAILED! Please check the errors above.")
    else:
        print("\n⚠️  Upgrade cancelled by user.")