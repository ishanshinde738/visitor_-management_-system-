"""
Complete Database Diagnostic and Fix Script
This script will check and fix all users in the database
"""

from flask import Flask
from models.database import db, User, Host
from werkzeug.security import generate_password_hash
from datetime import datetime

# Create minimal Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitor_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

def check_password_hash_valid(user):
    """Check if password_hash is valid (not NULL)"""
    return user.password_hash is not None and len(user.password_hash) > 0

with app.app_context():
    print("\n" + "=" * 80)
    print("🔍 COMPLETE DATABASE DIAGNOSTIC AND FIX")
    print("=" * 80)
    
    # =========================================================================
    # PART 1: CHECK ADMIN USERS
    # =========================================================================
    print("\n" + "=" * 80)
    print("📊 PART 1: CHECKING ADMIN USERS (users table)")
    print("=" * 80)
    
    all_users = User.query.all()
    
    if not all_users:
        print("\n⚠️  NO USERS FOUND IN DATABASE!")
    else:
        print(f"\n✅ Found {len(all_users)} user(s) in database:\n")
        
        for user in all_users:
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Role: {user.role}")
            print(f"  Active: {user.is_active}")
            print(f"  Has password_hash: {'✅ YES' if check_password_hash_valid(user) else '❌ NO (NULL)'}")
            
            # Test password if hash exists
            if check_password_hash_valid(user):
                # Try common passwords
                test_passwords = ['admin123', 'security123', 'password', '123456']
                password_works = False
                for pwd in test_passwords:
                    if user.check_password(pwd):
                        print(f"  ✅ Password '{pwd}' works!")
                        password_works = True
                        break
                
                if not password_works:
                    print(f"  ⚠️  Password exists but doesn't match common passwords")
            else:
                print(f"  ❌ NO PASSWORD SET - Login will fail!")
            
            print()
    
    # =========================================================================
    # PART 2: CHECK SECURITY USER
    # =========================================================================
    print("=" * 80)
    print("🔐 PART 2: CHECKING SECURITY USER")
    print("=" * 80)
    
    security_user = User.query.filter_by(role='security').first()
    
    if not security_user:
        print("\n❌ NO SECURITY USER FOUND!")
        print("   Creating security user now...\n")
        
        security_user = User(
            username='security',
            email='security@anand.com',
            full_name='Security Officer',
            role='security',
            is_active=True
        )
        security_user.set_password('security123')
        
        db.session.add(security_user)
        db.session.commit()
        
        print("✅ Security user created successfully!")
        print("   Username: security")
        print("   Password: security123")
        print("   Role: security")
    else:
        print(f"\n✅ Security user found: {security_user.username}")
        print(f"   Email: {security_user.email}")
        print(f"   Active: {security_user.is_active}")
        print(f"   Has password: {'✅ YES' if check_password_hash_valid(security_user) else '❌ NO'}")
        
        if not check_password_hash_valid(security_user):
            print("\n   ⚠️  PASSWORD IS NULL - Fixing now...")
            security_user.set_password('security123')
            db.session.commit()
            print("   ✅ Password set to: security123")
        else:
            # Test password
            if security_user.check_password('security123'):
                print("   ✅ Password 'security123' works!")
            else:
                print("   ⚠️  Password exists but doesn't match 'security123'")
                print("   Resetting to 'security123'...")
                security_user.set_password('security123')
                db.session.commit()
                print("   ✅ Password reset to: security123")
    
    # =========================================================================
    # PART 3: CHECK HOST USERS
    # =========================================================================
    print("\n" + "=" * 80)
    print("👤 PART 3: CHECKING HOST USERS (hosts table)")
    print("=" * 80)
    
    all_hosts = Host.query.all()
    
    if not all_hosts:
        print("\n⚠️  NO HOSTS FOUND IN DATABASE!")
        print("   Hosts must register through: http://localhost:5000/host/register")
    else:
        print(f"\n✅ Found {len(all_hosts)} host(s) in database:\n")
        
        for host in all_hosts:
            print(f"  Username: {host.username}")
            print(f"  Email: {host.email}")
            print(f"  Full Name: {host.full_name}")
            print(f"  Department: {host.department}")
            print(f"  Approved: {'✅ YES' if host.is_approved else '❌ NO (PENDING)'}")
            print(f"  Active: {'✅ YES' if host.is_active else '❌ NO'}")
            print(f"  Has password: {'✅ YES' if check_password_hash_valid(host) else '❌ NO (NULL)'}")
            
            # Check issues
            issues = []
            if not host.is_approved:
                issues.append("NOT APPROVED")
            if not host.is_active:
                issues.append("NOT ACTIVE")
            if not check_password_hash_valid(host):
                issues.append("NO PASSWORD")
            
            if issues:
                print(f"  ⚠️  ISSUES: {', '.join(issues)}")
                print(f"  → Login will fail until fixed!")
            else:
                print(f"  ✅ Host is ready to login")
            
            print()
    
    # =========================================================================
    # PART 4: FIX COMMON ISSUES
    # =========================================================================
    print("=" * 80)
    print("🔧 PART 4: AUTOMATIC FIXES")
    print("=" * 80)
    
    fixes_applied = []
    
    # Fix 1: Ensure admin user exists with correct password
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@anand.com',
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        fixes_applied.append("✅ Created admin user (admin/admin123)")
    elif not check_password_hash_valid(admin):
        admin.set_password('admin123')
        db.session.commit()
        fixes_applied.append("✅ Fixed admin password (admin/admin123)")
    
    # Fix 2: Ensure security user exists with correct password
    security = User.query.filter_by(role='security').first()
    if not security:
        security = User(
            username='security',
            email='security@anand.com',
            full_name='Security Officer',
            role='security',
            is_active=True
        )
        security.set_password('security123')
        db.session.add(security)
        db.session.commit()
        fixes_applied.append("✅ Created security user (security/security123)")
    elif not check_password_hash_valid(security):
        security.set_password('security123')
        db.session.commit()
        fixes_applied.append("✅ Fixed security password (security/security123)")
    
    # Fix 3: Auto-approve first host if exists
    first_host = Host.query.first()
    if first_host and not first_host.is_approved:
        first_host.is_approved = True
        first_host.is_active = True
        first_host.approval_status = 'approved'
        first_host.approved_by = admin.id if admin else None
        first_host.approval_date = datetime.utcnow()
        db.session.commit()
        fixes_applied.append(f"✅ Auto-approved first host: {first_host.username}")
    
    # Fix 4: Fix NULL passwords for all hosts
    hosts_with_null_password = Host.query.all()
    for host in hosts_with_null_password:
        if not check_password_hash_valid(host):
            # This shouldn't happen, but fix it if it does
            print(f"\n⚠️  Host '{host.username}' has NULL password - needs re-registration")
    
    print()
    if fixes_applied:
        for fix in fixes_applied:
            print(f"  {fix}")
    else:
        print("  ℹ️  No automatic fixes needed")
    
    # =========================================================================
    # PART 5: FINAL SUMMARY
    # =========================================================================
    print("\n" + "=" * 80)
    print("📋 FINAL SUMMARY - READY TO LOGIN")
    print("=" * 80)
    
    # Check admin
    admin = User.query.filter_by(username='admin').first()
    if admin and check_password_hash_valid(admin) and admin.is_active:
        if admin.check_password('admin123'):
            print("\n✅ ADMIN LOGIN READY:")
            print(f"   URL: http://localhost:5000/admin/login")
            print(f"   Username: admin")
            print(f"   Password: admin123")
    
    # Check security
    security = User.query.filter_by(role='security').first()
    if security and check_password_hash_valid(security) and security.is_active:
        if security.check_password('security123'):
            print("\n✅ SECURITY LOGIN READY:")
            print(f"   URL: http://localhost:5000/security/login")
            print(f"   Username: {security.username}")
            print(f"   Password: security123")
    
    # Check hosts
    approved_hosts = Host.query.filter_by(is_approved=True, is_active=True).all()
    if approved_hosts:
        print("\n✅ HOST LOGIN READY:")
        for host in approved_hosts:
            if check_password_hash_valid(host):
                print(f"   URL: http://localhost:5000/host/login")
                print(f"   Username: {host.username}")
                print(f"   Password: (password set during registration)")
                break
    else:
        print("\n⚠️  NO APPROVED HOSTS:")
        print(f"   Register at: http://localhost:5000/host/register")
        print(f"   Then admin must approve from admin panel")
    
    # Pending hosts
    pending_hosts = Host.query.filter_by(is_approved=False).all()
    if pending_hosts:
        print("\n⚠️  PENDING HOST APPROVALS:")
        for host in pending_hosts:
            print(f"   - {host.username} ({host.email}) - needs admin approval")
    
    print("\n" + "=" * 80)
    print("✅ DIAGNOSTIC COMPLETE")
    print("=" * 80)
    print()