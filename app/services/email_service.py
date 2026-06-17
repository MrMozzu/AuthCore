from flask import current_app, render_template
from flask_mail import Message 
from app.extensions import mail 


class EmailService:

    @staticmethod
    def send_reset_password_email(email, token):

        subject = "Reset your password"
        
        link = (f"http://localhost:3000/auth/reset-password"
                f"?token={token}")  # the ?token={token} part is only for frontend to consume, we can also use /auth/reset/{token} for the backend

        try:
            # Create a Mail Message object with subject, default sender from config, and recipient email
            msg = Message(subject, sender=current_app.config["MAIL_DEFAULT_SENDER"], recipients=[email])
            
            # Render and assign the HTML content template to the email message body
            msg.html = render_template("email_templates/reset_password.html", token=token, link=link) # this is for frontend to consume, the same token will be consumed by the backend in /auth/reset-password/{token} endpoint.
            mail.send(msg)
        
            return True 
        
        # Catch any exceptions/errors that occur during the email construction or dispatch
        except Exception as e:

            current_app.logger.error(f"Error while sending email: {e}")
    
            return False
