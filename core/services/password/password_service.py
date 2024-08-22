import re

import bcrypt

from core.common.results import Result

class PasswordService:
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
    