"""
Add Sample Visitors for Testing Charts
Creates 50 visitors spread across the last 60 days
"""

import sys
import os
from datetime import datetime, timedelta, date
import random

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from models.database import db, Visitor
from flask import Flask
from config import Config

def create_app():
    """Create Flask app"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def add_sample_visitors():
    """Add 50 sample visitors"""
    
    app = create_app()
    
    with app.app_context():
        print("📊 Adding sample visitors for chart testing...")
        print("="*70)
        
        # Sample data
        companies = ['TCS', 'Infosys', 'Wipro', 'Tech Mahindra', 'HCL', 'Cognizant', 'Capgemini', 'Accenture']
        hosts = ['Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Sneha Desai', 'Vikram Singh']
        purposes = ['Meeting', 'Interview', 'Delivery', 'Vendor Visit', 'Audit', 'Training']
        statuses = ['pending', 'approved', 'checked-in', 'checked-out', 'rejected']
        
        # Start date: 60 days ago
        start_date = date.today() - timedelta(days=60)
        
        visitors_added = 0
        
        for i in range(50):
            # Random date within last 60 days
            days_ago = random.randint(0, 60)
            visit_date = date.today() - timedelta(days=days_ago)
            
            # Create visitor
            visitor = Visitor(
                full_name=f"Test Visitor {i+1}",
                email=f"visitor{i+1}@example.com",
                phone=f"98765{43210 + i}",
                company=random.choice(companies),
                designation='Manager',
                visitor_type='customer',
                purpose=random.choice(purposes),
                visit_date=visit_date,
                visit_time='10:00',
                host_name=random.choice(hosts),
                host_email='host@anand.com',
                host_department='IT',
                status=random.choice(statuses),
                pass_id=f'VIS{2024000 + i}',
                created_at=datetime.combine(visit_date, datetime.min.time())
            )
            
            # For checked-out visitors, add check-in and check-out times
            if visitor.status == 'checked-out':
                visitor.check_in_time = datetime.combine(visit_date, datetime.min.time()) + timedelta(hours=9)
                visitor.check_out_time = visitor.check_in_time + timedelta(hours=random.randint(1, 6))
            elif visitor.status == 'checked-in':
                visitor.check_in_time = datetime.combine(visit_date, datetime.min.time()) + timedelta(hours=9)
            
            db.session.add(visitor)
            visitors_added += 1
        
        db.session.commit()
        
        print(f"\n✅ Successfully added {visitors_added} sample visitors!")
        print("\n📊 Distribution:")
        
        # Show distribution
        all_visitors = Visitor.query.all()
        
        status_counts = {}
        for v in all_visitors:
            status_counts[v.status] = status_counts.get(v.status, 0) + 1
        
        for status, count in status_counts.items():
            print(f"   {status}: {count}")
        
        print(f"\n📅 Date range:")
        dates = [v.visit_date for v in all_visitors if v.visit_date]
        if dates:
            print(f"   First visit: {min(dates)}")
            print(f"   Latest visit: {max(dates)}")
        
        print("\n🎨 Your charts will now display data!")
        print("   Refresh the Reports & Analytics page to see charts")
        
        print("\n" + "="*70)

if __name__ == '__main__':
    try:
        add_sample_visitors()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)