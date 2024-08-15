import re

import bcrypt

from core.common.results import Result

class PasswordService:
    
    def validate_password_format(self, password) -> Result:
        """
        Validates the password format.
        The password must be between 8 and 255 characters long, contain at least one uppercase letter,
        one lowercase letter, one digit, and one special character. It should not contain spaces.
        """
        pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[\W_]).{8,255}$'
        
        if not re.match(pattern, password):
            return Result.fail("Password must be between 8 and 255 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character. It should not contain spaces.", status_code=400)
        
        return Result.ok(None, status_code=200)
    
    def hash_password(self, password) -> str:
        """
        Hashes the password using bcrypt and returns it as a string suitable for storage in a database.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    def verify_password(self, password, hashed_password) -> bool:
        """
        Verifies the provided password against the stored hashed password.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))