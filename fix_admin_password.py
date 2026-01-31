"""
Database Fix Script - Reset Admin User Password
This script fixes the admin user password that was incorrectly created
"""

from flask import Flask
from models.database import db, User
from werkzeug.security import generate_password_hash

# Create minimal Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitor_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

with app.app_context():
    print("\n" + "=" * 70)
    print("🔧 DATABASE FIX - RESETTING ADMIN PASSWORD")
    print("=" * 70)
    
    # Find admin user
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"\n✅ Found admin user: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Current password_hash: {admin.password_hash[:50] if admin.password_hash else 'NULL'}...")
        
        # Reset password using set_password method
        admin.set_password('admin123')
        db.session.commit()
        
        print("\n✅ Password reset successfully!")
        print("   New password: admin123")
        print(f"   New password_hash: {admin.password_hash[:50]}...")
        
    else:
        print("\n❌ Admin user not found. Creating new admin user...")
        
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
        
        print("✅ Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
    
    # Verify password works
    if admin.check_password('admin123'):
        print("\n✅ Password verification: SUCCESS")
    else:
        print("\n❌ Password verification: FAILED")
    
    # Check all users
    print("\n" + "=" * 70)
    print("📊 ALL USERS IN DATABASE:")
    print("=" * 70)
    
    all_users = User.query.all()
    if all_users:
        for user in all_users:
            has_password = "✅ YES" if user.password_hash else "❌ NO"
            print(f"\n  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Role: {user.role}")
            print(f"  Active: {user.is_active}")
            print(f"  Has password_hash: {has_password}")
    else:
        print("\n  No users found in database")
    
    print("\n" + "=" * 70)
    print("✅ FIX COMPLETE - You can now login with:")
    print("   Username: admin")
    print("   Password: admin123")
    print("=" * 70 + "\n")