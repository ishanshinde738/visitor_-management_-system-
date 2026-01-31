"""
Database Migration Script
Run this to update the database schema with new fields
"""

from app import create_app
from models.database import db
from sqlalchemy import text

def migrate_database():
    """Add new columns to existing database"""
    app = create_app()
    
    with app.app_context():
        try:
            print("Starting database migration...")
            
            # Get database connection
            connection = db.engine.connect()
            
            # List of new columns to add
            new_columns = [
                "ALTER TABLE visitors ADD COLUMN company_address TEXT",
                "ALTER TABLE visitors ADD COLUMN visitor_type VARCHAR(50)",
                "ALTER TABLE visitors ADD COLUMN coming_with_vehicle VARCHAR(3)",
                "ALTER TABLE visitors ADD COLUMN has_driver VARCHAR(3)",
                "ALTER TABLE visitors ADD COLUMN driver_name VARCHAR(120)",
                "ALTER TABLE visitors ADD COLUMN driver_phone VARCHAR(20)",
                "ALTER TABLE visitors ADD COLUMN assets_to_bring VARCHAR(255)",
                "ALTER TABLE visitors ADD COLUMN assets_other_details VARCHAR(255)",
                "ALTER TABLE visitors ADD COLUMN purpose_other_details TEXT",
                "ALTER TABLE visitors ADD COLUMN visit_type VARCHAR(20)",
                "ALTER TABLE visitors ADD COLUMN visit_time VARCHAR(10)",
                "ALTER TABLE visitors ADD COLUMN no_of_days INTEGER",
                "ALTER TABLE visitors ADD COLUMN visit_dates TEXT",
                "ALTER TABLE visitors ADD COLUMN host_contact_no VARCHAR(20)",
                "ALTER TABLE visitors ADD COLUMN host_designation VARCHAR(100)",
                "ALTER TABLE visitors ADD COLUMN special_permissions TEXT",
                "ALTER TABLE visitors ADD COLUMN special_permission_other VARCHAR(255)",
            ]
            
            # Execute each ALTER TABLE command
            for sql in new_columns:
                try:
                    connection.execute(text(sql))
                    column_name = sql.split('ADD COLUMN ')[1].split(' ')[0]
                    print(f"✅ Added column: {column_name}")
                except Exception as e:
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        column_name = sql.split('ADD COLUMN ')[1].split(' ')[0]
                        print(f"⚠️  Column already exists: {column_name}")
                    else:
                        print(f"❌ Error adding column: {str(e)}")
            
            connection.commit()
            connection.close()
            
            print("\n✅ Database migration completed successfully!")
            print("You can now run the application with updated schema.")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {str(e)}")
            print("If database is corrupted, you may need to delete visitor_management.db and run init_db.py again.")

if __name__ == '__main__':
    migrate_database()