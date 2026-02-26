from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        if not text or not text.strip():
            raise ValueError("Review text is required")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        self.text     = text.strip()
        self.rating   = rating
        self.place_id = place_id
        self.user_id  = user_id

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "text":     self.text,
            "rating":   self.rating,
            "place_id": self.place_id,
            "user_id":  self.user_id
        })
        return base
