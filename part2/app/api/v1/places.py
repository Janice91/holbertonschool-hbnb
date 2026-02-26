from flask import request
from flask_restx import Namespace, Resource, fields
from app import facade

ns = Namespace("places", description="Place operations")

place_model = ns.model("Place", {
    "title":       fields.String(required=True),
    "description": fields.String(default=""),
    "price":       fields.Float(required=True),
    "latitude":    fields.Float(required=True),
    "longitude":   fields.Float(required=True),
    "owner_id":    fields.String(required=True),
    "amenities":   fields.List(fields.String, default=[])
})


@ns.route("/")
class PlaceList(Resource):

    def get(self):
        """List all places"""
        return facade.get_all_places(), 200

    @ns.expect(place_model, validate=True)
    def post(self):
        """Create a place"""
        try:
            place = facade.create_place(request.json)
            return place.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:place_id>")
class PlaceResource(Resource):

    def get(self, place_id):
        """Get a place by ID (with owner details and amenities)"""
        place = facade.get_place(place_id)
        if not place:
            ns.abort(404, "Place not found")
        return place, 200

    @ns.expect(place_model, validate=False)
    def put(self, place_id):
        """Update a place"""
        if not facade.place_repo.get(place_id):
            ns.abort(404, "Place not found")
        try:
            updated = facade.update_place(place_id, request.json)
            return updated.to_dict(), 200
        except ValueError as e:
            ns.abort(400, str(e))

    def delete(self, place_id):
        """Delete a place"""
        if not facade.place_repo.get(place_id):
            ns.abort(404, "Place not found")
        facade.delete_place(place_id)
        return {"message": "Place deleted"}, 200
