"""
Flask extensions initialization
"""
from flask_mail import Mail

# Initialize Flask-Mail
mail = Mail()


def init_extensions(app):
    """Initialize all Flask extensions"""
    mail.init_app(app)