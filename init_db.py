from app import create_app
from models.database import db, User
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with default admin and security users"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                full_name='System Administrator',
                role='superadmin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("Default admin user created (username: admin, password: admin123)")
        else:
            print("Admin user already exists.")
        
        # Create default security user
        security = User.query.filter_by(username='security').first()
        if not security:
            security = User(
                username='security',
                email='security@example.com',
                full_name='Security Officer',
                role='security'
            )
            security.set_password('security123')
            db.session.add(security)
            print("Default security user created (username: security, password: security123)")
        else:
            print("Security user already exists.")
        
        db.session.commit()
        print("\nDatabase initialization complete!")
        print("\nLogin Credentials:")
        print("=" * 50)
        print("Admin Login:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nSecurity Login:")
        print("  Username: security")
        print("  Password: security123")
        print("=" * 50)

if __name__ == '__main__':
    init_database()