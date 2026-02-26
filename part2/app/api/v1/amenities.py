from flask import request
from flask_restx import Namespace, Resource, fields
from app import facade

ns = Namespace("amenities", description="Amenity operations")

amenity_model = ns.model("Amenity", {
    "name": fields.String(required=True)
})


@ns.route("/")
class AmenityList(Resource):

    def get(self):
        """List all amenities"""
        return [a.to_dict() for a in facade.get_all_amenities()], 200

    @ns.expect(amenity_model, validate=True)
    def post(self):
        """Create an amenity"""
        try:
            amenity = facade.create_amenity(request.json)
            return amenity.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:amenity_id>")
class AmenityResource(Resource):

    def get(self, amenity_id):
        """Get an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            ns.abort(404, "Amenity not found")
        return amenity.to_dict(), 200

    @ns.expect(amenity_model, validate=False)
    def put(self, amenity_id):
        """Update an amenity"""
        if not facade.get_amenity(amenity_id):
            ns.abort(404, "Amenity not found")
        try:
            updated = facade.update_amenity(amenity_id, request.json)
            return updated.to_dict(), 200
        except ValueError as e:
            ns.abort(400, str(e))

    def delete(self, amenity_id):
        """Delete an amenity"""
        if not facade.get_amenity(amenity_id):
            ns.abort(404, "Amenity not found")
        facade.delete_amenity(amenity_id)
        return {"message": "Amenity deleted"}, 200
