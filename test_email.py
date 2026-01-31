"""
Email Configuration Test Script
Run this to verify your email settings are working
"""

from app import create_app
from utils.email_service import EmailService

def test_email_configuration():
    """Test email configuration"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("EMAIL CONFIGURATION TEST")
        print("=" * 70)
        
        # Display current configuration
        print("\nCurrent Email Configuration:")
        print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
        print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
        print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
        print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
        print(f"MAIL_PASSWORD: {'*' * 10 if app.config.get('MAIL_PASSWORD') else 'NOT SET'}")
        print(f"MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
        print()
        
        if not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
            print("❌ ERROR: Email credentials not configured!")
            print("\nPlease update your .env file with:")
            print("MAIL_USERNAME=your-email@gmail.com")
            print("MAIL_PASSWORD=your-gmail-app-password")
            print("\nRefer to the setup guide to get Gmail App Password.")
            return
        
        # Ask for test recipient
        recipient = input("\nEnter email address to send test email to: ").strip()
        
        if not recipient:
            print("❌ No email address provided. Exiting.")
            return
        
        print(f"\n📧 Sending test email to: {recipient}")
        print("Please wait...")
        
        # Send test email
        success, message = EmailService.send_test_email(recipient)
        
        print()
        print("=" * 70)
        if success:
            print("✅ SUCCESS! Test email sent successfully!")
            print(f"\nCheck the inbox of: {recipient}")
            print("If you don't see the email:")
            print("1. Check your spam/junk folder")
            print("2. Wait a few minutes and refresh")
            print("3. Verify the email address is correct")
        else:
            print("❌ FAILED! Could not send test email.")
            print(f"\nError: {message}")
            print("\nCommon issues:")
            print("1. App Password incorrect - regenerate it")
            print("2. Gmail 2FA not enabled")
            print("3. 'Less secure app access' needed (if not using App Password)")
            print("4. Network/firewall blocking SMTP")
        print("=" * 70)

if __name__ == '__main__':
    test_email_configuration()