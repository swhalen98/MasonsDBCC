"""
Simple authentication for Panel dashboard
"""

import bcrypt
import os
from pathlib import Path


class SimpleAuth:
    """Simple username/password authentication"""

    def __init__(self):
        self.users_file = Path(__file__).parent / ".users"
        self.load_users()

    def load_users(self):
        """Load users from file or create defaults"""
        self.users = {}

        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                for line in f:
                    if ':' in line:
                        username, password_hash = line.strip().split(':', 1)
                        self.users[username] = password_hash
        else:
            # Create default users
            self.add_user("admin", os.getenv("ADMIN_PASSWORD", "changeme123"))
            self.add_user("manager", os.getenv("MANAGER_PASSWORD", "changeme456"))
            self.add_user("viewer", os.getenv("VIEWER_PASSWORD", "changeme789"))
            self.save_users()

    def save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            for username, password_hash in self.users.items():
                f.write(f"{username}:{password_hash}\n")

    def hash_password(self, password):
        """Hash a password"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password, password_hash):
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def add_user(self, username, password):
        """Add a new user"""
        self.users[username] = self.hash_password(password)
        self.save_users()

    def authenticate(self, username, password):
        """Authenticate a user"""
        if username in self.users:
            return self.verify_password(password, self.users[username])
        return False

    def change_password(self, username, old_password, new_password):
        """Change a user's password"""
        if self.authenticate(username, old_password):
            self.users[username] = self.hash_password(new_password)
            self.save_users()
            return True
        return False
