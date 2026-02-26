import re
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self._check_name(first_name, "first_name")
        self.last_name  = self._check_name(last_name,  "last_name")
        self.email      = self._check_email(email)
        self.is_admin   = is_admin

    def _check_name(self, value, field):
        if not value or not value.strip():
            raise ValueError(f"{field} is required")
        if len(value) > 50:
            raise ValueError(f"{field} must be 50 characters max")
        return value.strip()

    def _check_email(self, email):
        if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email):
            raise ValueError("Invalid email format")
        return email.lower()

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "first_name": self.first_name,
            "last_name":  self.last_name,
            "email":      self.email,
            "is_admin":   self.is_admin
        })
        return base
