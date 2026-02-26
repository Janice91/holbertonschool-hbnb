from flask import request
from flask_restx import Namespace, Resource, fields
from app import facade

ns = Namespace("amenities", description="Amenity operations")

amenity_model = ns.model("Amenity", {
    "name": fields.String(required=True, description="Amenity name")
})

amenity_response = ns.model("AmenityResponse", {
    "id":         fields.String(description="Amenity ID"),
    "name":       fields.String(description="Amenity name"),
    "created_at": fields.String(description="Creation date"),
    "updated_at": fields.String(description="Last update date")
})


@ns.route("/")
class AmenityList(Resource):

    @ns.marshal_list_with(amenity_response)
    @ns.response(200, "List of amenities retrieved successfully")
    def get(self):
        """List all amenities"""
        return facade.get_all_amenities(), 200

    @ns.expect(amenity_model, validate=True)
    @ns.response(201, "Amenity created successfully")
    @ns.response(400, "Invalid input data")
    def post(self):
        """Create a new amenity"""
        try:
            amenity = facade.create_amenity(request.json)
            return amenity.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:amenity_id>")
@ns.param("amenity_id", "The amenity identifier")
class AmenityResource(Resource):

    @ns.response(200, "Amenity found")
    @ns.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            ns.abort(404, "Amenity not found")
        return amenity.to_dict(), 200

    @ns.expect(amenity_model, validate=False)
    @ns.response(200, "Amenity updated successfully")
    @ns.response(400, "Invalid input data")
    @ns.response(404, "Amenity not found")
    def put(self, amenity_id):
        """Update an amenity"""
        if not facade.get_amenity(amenity_id):
            ns.abort(404, "Amenity not found")
        try:
            updated = facade.update_amenity(amenity_id, request.json)
            return updated.to_dict(), 200
        except ValueError as e:
            ns.abort(400, str(e))
