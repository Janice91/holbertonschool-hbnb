from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo    = InMemoryRepository()
        self.place_repo   = InMemoryRepository()
        self.review_repo  = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, data):
        if self.user_repo.get_by_attribute("email", data["email"]):
            raise ValueError("Email already registered")
        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            is_admin=data.get("is_admin", False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        if "email" in data:
            existing = self.user_repo.get_by_attribute("email", data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

    def create_amenity(self, data):
        amenity = Amenity(name=data["name"])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        self.amenity_repo.update(amenity_id, data)
        return self.amenity_repo.get(amenity_id)

    def delete_amenity(self, amenity_id):
        self.amenity_repo.delete(amenity_id)

    def create_place(self, data):
        if not self.user_repo.get(data["owner_id"]):
            raise ValueError("Owner not found")
        for aid in data.get("amenities", []):
            if not self.amenity_repo.get(aid):
                raise ValueError(f"Amenity {aid} not found")
        place = Place(
            title=data["title"],
            description=data.get("description", ""),
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner_id=data["owner_id"]
        )
        place.amenities = data.get("amenities", [])
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        owner = self.user_repo.get(place.owner_id)
        amenities = [
            self.amenity_repo.get(aid).to_dict()
            for aid in place.amenities
            if self.amenity_repo.get(aid)
        ]
        result = place.to_dict()
        result["owner"] = {
            "id":         owner.id,
            "first_name": owner.first_name,
            "last_name":  owner.last_name,
            "email":      owner.email
        } if owner else None
        result["amenities"] = amenities
        return result

    def get_all_places(self):
        return [p.to_dict() for p in self.place_repo.get_all()]

    def update_place(self, place_id, data):
        self.place_repo.update(place_id, data)
        return self.place_repo.get(place_id)

    def delete_place(self, place_id):
        self.place_repo.delete(place_id)

    def create_review(self, data):
        if not self.place_repo.get(data["place_id"]):
            raise ValueError("Place not found")
        if not self.user_repo.get(data["user_id"]):
            raise ValueError("User not found")
        review = Review(
            text=data["text"],
            rating=data["rating"],
            place_id=data["place_id"],
            user_id=data["user_id"]
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, data):
        self.review_repo.update(review_id, data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
