from django.core.mail import get_connection, send_mail
from django.conf import settings


class EmailService:
    
    def send_verification_email(self, user, code):
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{code}"
        subject = "Verify Your Email Address"
        message = (f"Hi {user.first_name},\n\n"
                   f"Please verify your email address by clicking the link below:\n\n{verification_url}\n\nThank you!")
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )