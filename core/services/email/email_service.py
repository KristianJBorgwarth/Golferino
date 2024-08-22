from django.core.mail import get_connection, send_mail
from django.conf import settings

class EmailSerivce:
    
    def send(self, to_email, subject, message):
        import os
        print(os.getenv('EMAIL_HOST'))
        print(os.getenv('EMAIL_USER_G'))
        print(os.getenv('EMAIL_PASSWORD_G'))
        connection = get_connection()
        
        if not connection.open():
            connection.open()
            
        send_mail(subject=subject, 
                  message=message, 
                  from_email=settings.EMAIL_FROM, 
                  recipient_list=[to_email])
        connection.close()