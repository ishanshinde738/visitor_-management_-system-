"""
Add Test Visitors to Database
Creates 20 test visitors with recent dates
"""

import sqlite3
from datetime import date, timedelta
import random

# Connect to database
conn = sqlite3.connect('instance/vms.db')
cursor = conn.cursor()

print("Adding 20 test visitors with recent dates...")
print("=" * 70)

companies = ['TechCorp', 'InnovateLab', 'FutureSoft', 'DataSystems', 'CloudInc']
hosts = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams', 'Charlie Brown']
purposes = ['Business Meeting', 'Interview', 'Delivery', 'Consultation', 'Training']
statuses = ['pending', 'approved', 'checked-in', 'checked-out']

for i in range(20):
    # Random date in last 7 days
    days_ago = random.randint(0, 7)
    visit_date = (date.today() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    full_name = f"Test Visitor {i+1}"
    email = f"test{i+1}@example.com"
    phone = f"555-{1000+i}"
    company = random.choice(companies)
    host_name = random.choice(hosts)
    purpose = random.choice(purposes)
    status = random.choice(statuses)
    
    cursor.execute("""
        INSERT INTO visitors 
        (full_name, email, phone, company, host_name, purpose, visit_date, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """, (full_name, email, phone, company, host_name, purpose, visit_date, status))
    
    print(f"  ✓ Added {full_name}: {visit_date}, {status}")

conn.commit()
conn.close()

print("=" * 70)
print("✅ Successfully added 20 test visitors!")
print("\nNow refresh your Reports page - charts should display data!")