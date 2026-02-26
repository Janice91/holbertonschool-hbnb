from flask import request
from flask_restx import Namespace, Resource, fields
from app import facade

ns = Namespace("reviews", description="Review operations")

review_model = ns.model("Review", {
    "text":     fields.String(required=True),
    "rating":   fields.Integer(required=True),
    "place_id": fields.String(required=True),
    "user_id":  fields.String(required=True)
})


@ns.route("/")
class ReviewList(Resource):

    def get(self):
        """List all reviews"""
        return [r.to_dict() for r in facade.get_all_reviews()], 200

    @ns.expect(review_model, validate=True)
    def post(self):
        """Create a review"""
        try:
            review = facade.create_review(request.json)
            return review.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:review_id>")
class ReviewResource(Resource):

    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            ns.abort(404, "Review not found")
        return review.to_dict(), 200

    @ns.expect(review_model, validate=False)
    def put(self, review_id):
        """Update a review"""
        if not facade.get_review(review_id):
            ns.abort(404, "Review not found")
        try:
            updated = facade.update_review(review_id, request.json)
            return updated.to_dict(), 200
        except ValueError as e:
            ns.abort(400, str(e))

    def delete(self, review_id):
        """Delete a review"""
        if not facade.get_review(review_id):
            ns.abort(404, "Review not found")
        facade.delete_review(review_id)
        return {"message": "Review deleted"}, 200


@ns.route("/places/<string:place_id>")
class ReviewsByPlace(Resource):

    def get(self, place_id):
        """Get all reviews for a specific place"""
        return [r.to_dict() for r in facade.get_reviews_by_place(place_id)], 200
