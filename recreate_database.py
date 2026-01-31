"""
Recreate Database with New Schema
Includes Host tables + Creates default users
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from database import User, Visitor, VisitLog, SystemSettings, Host, HostVisitor, HostActivityLog
from werkzeug.security import generate_password_hash
from datetime import datetime

def recreate_database():
    """Drop all tables and recreate with new schema"""
    
    print("🗄️  RECREATING DATABASE WITH NEW SCHEMA")
    print("="*70)
    
    with app.app_context():
        # Drop all existing tables
        print("\n🗑️  Dropping all existing tables...")
        db.drop_all()
        print("✅ All old tables dropped")
        
        # Create all tables with new schema
        print("\n📋 Creating all tables with new schema...")
        db.create_all()
        print("✅ All tables created successfully!")
        
        # List all tables created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        print(f"\n📊 Tables created ({len(table_names)}):")
        for i, table in enumerate(sorted(table_names), 1):
            print(f"   {i}. {table}")
        
        # Create default admin user
        print("\n👤 Creating default admin user...")
        admin = User(
            username='admin',
            email='admin@anand.com',
            password_hash=generate_password_hash('admin123'),
            full_name='System Administrator',
            role='admin',
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(admin)
        print("✅ Admin user created")
        
        # Create default security user
        print("\n👮 Creating default security user...")
        security = User(
            username='security',
            email='security@anand.com',
            password_hash=generate_password_hash('security123'),
            full_name='Security Guard',
            role='security',
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(security)
        print("✅ Security user created")
        
        # Commit all changes
        db.session.commit()
        
        # Display summary
        print("\n" + "="*70)
        print("✅ DATABASE RECREATED SUCCESSFULLY!")
        print("="*70)
        
        print("\n📊 Database Summary:")
        print(f"   Total Tables: {len(table_names)}")
        print(f"   Users: {User.query.count()}")
        print(f"   Hosts: {Host.query.count()}")
        print(f"   Visitors: {Visitor.query.count()}")
        
        print("\n🔐 Default Login Credentials:")
        print("\n   👤 ADMIN:")
        print("      Username: admin")
        print("      Password: admin123")
        print("      Email: admin@anand.com")
        
        print("\n   👮 SECURITY:")
        print("      Username: security")
        print("      Password: security123")
        print("      Email: security@anand.com")
        
        print("\n✅ READY FOR HOST APPROVAL FEATURE!")
        print("   - Host table with approval_status field")
        print("   - HostVisitor table for host-registered visitors")
        print("   - HostActivityLog for tracking host actions")
        
        print("\n🚀 You can now run:")
        print("   python app.py")
        
        print("\n🌐 Then access:")
        print("   http://127.0.0.1:5000")
        
        print("\n" + "="*70)

if __name__ == '__main__':
    try:
        recreate_database()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)