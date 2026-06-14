from flask import current_app, render_template
from flask_mail import Message 
from app.extensions import mail 


class EmailService:
    @staticmethod
    def send_reset_password_email(email, token):
        subject = "Reset your password"
        link = f"http://localhost:5000/auth/reset-password/{token}"

        try:
            msg = Message(subject, sender=current_app.config["MAIL_DEFAULT_SENDER"], recipients=[email])
            msg.html = render_template("email_templates/reset_password.html", token=token, link=link)
            
            # send the email
            mail.send(msg)
        
        except Exception as e:
            current_app.logger.error(f"Error while sending email: {e}")

            
        
        
