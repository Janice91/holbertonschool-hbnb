from flask import request
from flask_restx import Namespace, Resource, fields
from app import facade

ns = Namespace("reviews", description="Review operations")

review_model = ns.model("Review", {
    "text":     fields.String(required=True, description="Review text"),
    "rating":   fields.Integer(required=True, description="Rating (1 to 5)"),
    "place_id": fields.String(required=True, description="Place ID"),
    "user_id":  fields.String(required=True, description="User ID")
})

review_response = ns.model("ReviewResponse", {
    "id":         fields.String(description="Review ID"),
    "text":       fields.String(description="Review text"),
    "rating":     fields.Integer(description="Rating"),
    "place_id":   fields.String(description="Place ID"),
    "user_id":    fields.String(description="User ID"),
    "created_at": fields.String(description="Creation date"),
    "updated_at": fields.String(description="Last update date")
})


@ns.route("/")
class ReviewList(Resource):

    @ns.marshal_list_with(review_response)
    @ns.response(200, "List of reviews retrieved successfully")
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews(), 200

    @ns.expect(review_model, validate=True)
    @ns.response(201, "Review created successfully")
    @ns.response(400, "Invalid input data")
    def post(self):
        """Create a new review"""
        try:
            review = facade.create_review(request.json)
            return review.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:review_id>")
@ns.param("review_id", "The review identifier")
class ReviewResource(Resource):

    @ns.response(200, "Review found")
    @ns.response(404, "Review not found")
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            ns.abort(404, "Review not found")
        return review.to_dict(), 200

    @ns.expect(review_model, validate=False)
    @ns.response(200, "Review updated successfully")
    @ns.response(400, "Invalid input data")
    @ns.response(404, "Review not found")
    def put(self, review_id):
        """Update a review"""
        if not facade.get_review(review_id):
            ns.abort(404, "Review not found")
        try:
            updated = facade.update_review(review_id, request.json)
            return updated.to_dict(), 200
        except ValueError as e:
            ns.abort(400, str(e))

    @ns.response(200, "Review deleted successfully")
    @ns.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review"""
        if not facade.get_review(review_id):
            ns.abort(404, "Review not found")
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200


@ns.route("/places/<string:place_id>")
@ns.param("place_id", "The place identifier")
class PlaceReviewList(Resource):

    @ns.marshal_list_with(review_response)
    @ns.response(200, "List of reviews for the place")
    @ns.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place"""
        if not facade.place_repo.get(place_id):
            ns.abort(404, "Place not found")
        return facade.get_reviews_by_place(place_id), 200
