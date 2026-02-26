from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        if not title or not title.strip():
            raise ValueError("Title is required")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters max")
        if float(price) <= 0:
            raise ValueError("Price must be positive")
        if not (-90 <= float(latitude) <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= float(longitude) <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        self.title       = title.strip()
        self.description = description or ""
        self.price       = float(price)
        self.latitude    = float(latitude)
        self.longitude   = float(longitude)
        self.owner_id    = owner_id
        self.amenities   = []

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "title":       self.title,
            "description": self.description,
            "price":       self.price,
            "latitude":    self.latitude,
            "longitude":   self.longitude,
            "owner_id":    self.owner_id,
            "amenities":   self.amenities
        })
        return base
