"""
Visitor Management System - Main Application
Complete app.py with email functionality and multi-user authentication
"""

from flask import Flask, render_template, session
from flask_login import LoginManager
from datetime import datetime
import os

# Import database
from models.database import db

# Import blueprints
from routes.visitor_routes import visitor_bp
from routes.admin_routes import admin_bp
from routes.analytics_routes import analytics_bp
from routes.security_routes import security_bp
from routes.host_routes import host_bp

# Import extensions (Flask-Mail)
from extensions import init_extensions


def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # =========================================================================
    # BASIC CONFIGURATION
    # =========================================================================
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitor_management.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # =========================================================================
    # FILE UPLOAD CONFIGURATION
    # =========================================================================
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['FACE_FOLDER'] = 'static/uploads/faces'
    app.config['EPASS_FOLDER'] = 'static/uploads/epass'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # =========================================================================
    # EMAIL CONFIGURATION (Flask-Mail)
    # =========================================================================
    
    # OPTION 1: Gmail Configuration (Recommended for testing)
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False') == 'True'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')  # CHANGE THIS
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')     # CHANGE THIS
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@anand.com')
    
    # OPTION 2: Outlook/Hotmail Configuration (Uncomment to use)
    # app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USERNAME'] = 'your-email@outlook.com'
    # app.config['MAIL_PASSWORD'] = 'your-password'
    # app.config['MAIL_DEFAULT_SENDER'] = 'noreply@anand.com'
    
    # OPTION 3: Custom SMTP Server (Uncomment to use)
    # app.config['MAIL_SERVER'] = 'smtp.your-company.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USERNAME'] = 'smtp-username'
    # app.config['MAIL_PASSWORD'] = 'smtp-password'
    # app.config['MAIL_DEFAULT_SENDER'] = 'noreply@your-company.com'
    
    # =========================================================================
    # CREATE NECESSARY FOLDERS
    # =========================================================================
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['FACE_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EPASS_FOLDER'], exist_ok=True)
    
    # =========================================================================
    # INITIALIZE EXTENSIONS
    # =========================================================================
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Flask-Mail (from extensions.py)
    init_extensions(app)
    
    # =========================================================================
    # TEMPLATE CONTEXT PROCESSORS
    # =========================================================================
    
    @app.context_processor
    def inject_now():
        """Make 'now' variable available to all templates"""
        return {'now': datetime.utcnow()}
    
    # =========================================================================
    # FLASK-LOGIN CONFIGURATION (Multi-user Authentication)
    # =========================================================================
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """
        Load user - supports User (Admin/Security) and Host with type discrimination
        
        IMPORTANT: Multi-user authentication system:
        - Admin users: role='admin' or 'superadmin' in 'users' table
        - Security users: role='security' in 'users' table
        - Host users: separate 'hosts' table
        
        This function checks the session for user_type to load from the correct table.
        This prevents ID conflicts when different user tables have the same ID.
        """
        from models.database import User, Host
        
        # Check session for user type
        user_type = session.get('user_type')
        
        if user_type == 'host':
            # Load as Host from hosts table
            return Host.query.get(int(user_id))
        elif user_type == 'security' or user_type == 'admin':
            # Both admin and security are in users table!
            return User.query.get(int(user_id))
        else:
            # Fallback: try all tables (for backward compatibility or when session is lost)
            # Try User (Admin/Security) first
            user = User.query.get(int(user_id))
            if user:
                # Set session based on role
                if user.role == 'security':
                    session['user_type'] = 'security'
                else:
                    session['user_type'] = 'admin'
                return user
            
            # Try Host
            host = Host.query.get(int(user_id))
            if host:
                session['user_type'] = 'host'
                return host
            
            # User not found in any table
            return None
    
    # =========================================================================
    # REGISTER BLUEPRINTS
    # =========================================================================
    
    app.register_blueprint(visitor_bp)  # Public visitor registration
    app.register_blueprint(admin_bp, url_prefix='/admin')  # Admin portal
    app.register_blueprint(analytics_bp, url_prefix='/analytics')  # Analytics
    app.register_blueprint(security_bp, url_prefix='/security')  # Security portal
    app.register_blueprint(host_bp, url_prefix='/host')  # Host portal
    
    # =========================================================================
    # ERROR HANDLERS
    # =========================================================================
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors"""
        return render_template('errors/403.html'), 403
    
    # =========================================================================
    # CREATE DATABASE TABLES
    # =========================================================================
    
    with app.app_context():
        # Import all models to ensure they're registered
        from models.database import (
            User, Visitor, VisitLog, SystemSettings,
            Host, HostVisitor, HostActivityLog
        )
        
        # Create all tables
        db.create_all()
        
        # Create default admin user if not exists
        try:
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@anand.com',
                    full_name='System Administrator',
                    role='admin',
                    is_active=True
                )
                admin.set_password('admin123')  # Use set_password method
                
                db.session.add(admin)
                db.session.commit()
                print("✅ Default admin user created (username: admin, password: admin123)")
        except Exception as e:
            print(f"⚠️ Error creating default admin: {str(e)}")
            db.session.rollback()
    
    return app


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == '__main__':
    app = create_app()
    
    # Print startup information
    print("\n" + "=" * 80)
    print("🚀 VISITOR MANAGEMENT SYSTEM - STARTING")
    print("=" * 80)
    print("")
    
    # Database info
    print("📊 DATABASE:")
    print(f"   Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print("")
    
    # Email configuration info
    print("📧 EMAIL CONFIGURATION:")
    print(f"   Mail Server: {app.config.get('MAIL_SERVER')}")
    print(f"   Mail Port: {app.config.get('MAIL_PORT')}")
    print(f"   Mail Username: {app.config.get('MAIL_USERNAME')}")
    print(f"   Use TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"   Default Sender: {app.config.get('MAIL_DEFAULT_SENDER')}")
    
    # Check if email is configured
    if app.config.get('MAIL_USERNAME') == 'your-email@gmail.com':
        print("   ⚠️  WARNING: Email not configured! Please update MAIL_USERNAME and MAIL_PASSWORD")
    else:
        print("   ✅ Email Configured: Ready to send")
    print("")
    
    # Authentication info
    print("🔐 MULTI-USER AUTHENTICATION:")
    print("   ✅ Admin Login:        http://localhost:5000/admin/login")
    print("   ✅ Security Login:     http://localhost:5000/security/login")
    print("   ✅ Host Login:         http://localhost:5000/host/login")
    print("   ✅ Host Registration:  http://localhost:5000/host/register")
    print("")
    
    # Default credentials
    print("🔑 DEFAULT ADMIN CREDENTIALS:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   ⚠️  CHANGE THESE IN PRODUCTION!")
    print("")
    
    # Feature status
    print("✨ FEATURES:")
    print("   ✅ Public Visitor Registration")
    print("   ✅ Admin Portal (User Management)")
    print("   ✅ Security Portal (Check-in/Check-out)")
    print("   ✅ Host Portal (Host-registered visitors)")
    print("   ✅ Email Notifications (Host & Visitor)")
    print("   ✅ Entry & Exit Codes Generation")
    print("   ✅ Analytics Dashboard")
    print("   ✅ Multi-user Authentication")
    print("")
    
    print("=" * 80)
    print("🌐 SERVER STARTING ON: http://localhost:5000")
    print("=" * 80)
    print("\n")
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)