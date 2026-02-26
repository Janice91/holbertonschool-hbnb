from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name or not name.strip():
            raise ValueError("Amenity name is required")
        if len(name) > 50:
            raise ValueError("Amenity name must be 50 characters max")
        self.name = name.strip()

    def to_dict(self):
        base = super().to_dict()
        base.update({"name": self.name})
        return base
