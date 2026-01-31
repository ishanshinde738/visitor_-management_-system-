"""
Simple Visitor Data Checker - CORRECT VERSION
Database: visitor_management.db
Table: visitors
"""

import sqlite3
from datetime import date, timedelta

# Connect to YOUR database
try:
    conn = sqlite3.connect('instance/visitor_management.db')
    cursor = conn.cursor()
except Exception as e:
    print(f"❌ Error connecting to database: {e}")
    exit(1)

print("=" * 70)
print("DATABASE DATA CHECK")
print("=" * 70)

# Total visitors
cursor.execute("SELECT COUNT(*) FROM visitors")
total = cursor.fetchone()[0]
print(f"\n✓ Total visitors in database: {total}")

if total == 0:
    print("\n❌ NO VISITORS IN DATABASE!")
    print("   You need to add some test visitors first.")
    print("\n   Run: python add_test_visitors_CORRECT.py")
else:
    print("\n✓ Visitors exist! Checking details...\n")
    
    # Check visitors with visit_date
    cursor.execute("SELECT COUNT(*) FROM visitors WHERE visit_date IS NOT NULL")
    with_date = cursor.fetchone()[0]
    print(f"✓ Visitors with visit_date: {with_date}")
    
    # Check last 30 days
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    cursor.execute("""
        SELECT COUNT(*) FROM visitors 
        WHERE visit_date >= ? AND visit_date <= ?
    """, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    recent = cursor.fetchone()[0]
    print(f"✓ Visitors in last 30 days: {recent}")
    
    if recent == 0:
        print("\n⚠️  WARNING: No visitors in the last 30 days!")
        print("   This is why your charts are blank!")
        print("\n   Solutions:")
        print("   1. Run: python add_test_visitors_CORRECT.py (to add test data)")
        print("   2. Or change date range in Reports page")
    
    # Show some sample visitors
    print("\nSample visitors:")
    print("-" * 70)
    cursor.execute("SELECT full_name, visit_date, status FROM visitors LIMIT 5")
    for row in cursor.fetchall():
        name, visit_date, status = row
        print(f"  - {name}: visit_date={visit_date}, status={status}")
    
    # Count by status
    print("\nBy Status:")
    print("-" * 70)
    for status in ['pending', 'approved', 'checked-in', 'checked-out', 'rejected']:
        cursor.execute("SELECT COUNT(*) FROM visitors WHERE status = ?", (status,))
        count = cursor.fetchone()[0]
        print(f"  - {status}: {count}")
    
    # Show date range of all visitors
    print("\nDate Range of All Visitors:")
    print("-" * 70)
    cursor.execute("""
        SELECT MIN(visit_date), MAX(visit_date) 
        FROM visitors 
        WHERE visit_date IS NOT NULL
    """)
    min_date, max_date = cursor.fetchone()
    if min_date and max_date:
        print(f"  Earliest: {min_date}")
        print(f"  Latest: {max_date}")
        print(f"\n  Today is: {date.today()}")
        print(f"  30 days ago: {start_date}")
    else:
        print("  No visitors with visit_date set!")

conn.close()

print("\n" + "=" * 70)
print("\nCONCLUSION:")
if total == 0:
    print("  ❌ No visitors - run: python add_test_visitors_CORRECT.py")
elif recent == 0:
    print("  ⚠️  Visitors exist but not in last 30 days")
    print("  Run: python add_test_visitors_CORRECT.py")
else:
    print("  ✅ Data looks good! Charts should work.")
    print("  If charts still blank, check browser console (F12)")
print("=" * 70)