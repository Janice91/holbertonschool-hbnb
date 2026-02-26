from flask import request
from flask_restx import Namespace, Resource, fields
from app import facade

ns = Namespace("places", description="Place operations")

amenity_model = ns.model("PlaceAmenity", {
    "id":   fields.String(description="Amenity ID"),
    "name": fields.String(description="Amenity name")
})

owner_model = ns.model("PlaceOwner", {
    "id":         fields.String(description="Owner ID"),
    "first_name": fields.String(description="First name"),
    "last_name":  fields.String(description="Last name"),
    "email":      fields.String(description="Email")
})

place_model = ns.model("Place", {
    "title":       fields.String(required=True,  description="Place title"),
    "description": fields.String(default="",     description="Description"),
    "price":       fields.Float(required=True,   description="Price per night"),
    "latitude":    fields.Float(required=True,   description="Latitude (-90 to 90)"),
    "longitude":   fields.Float(required=True,   description="Longitude (-180 to 180)"),
    "owner_id":    fields.String(required=True,  description="Owner user ID"),
    "amenities":   fields.List(fields.String,    description="List of amenity IDs")
})

place_response = ns.model("PlaceResponse", {
    "id":          fields.String(description="Place ID"),
    "title":       fields.String(description="Place title"),
    "description": fields.String(description="Description"),
    "price":       fields.Float(description="Price per night"),
    "latitude":    fields.Float(description="Latitude"),
    "longitude":   fields.Float(description="Longitude"),
    "owner_id":    fields.String(description="Owner ID"),
    "amenities":   fields.List(fields.String,    description="Amenity IDs"),
    "created_at":  fields.String(description="Creation date"),
    "updated_at":  fields.String(description="Last update date")
})

place_detail_response = ns.model("PlaceDetailResponse", {
    "id":          fields.String(description="Place ID"),
    "title":       fields.String(description="Place title"),
    "description": fields.String(description="Description"),
    "price":       fields.Float(description="Price per night"),
    "latitude":    fields.Float(description="Latitude"),
    "longitude":   fields.Float(description="Longitude"),
    "owner":       fields.Nested(owner_model,    description="Owner details"),
    "amenities":   fields.List(fields.Nested(amenity_model), description="Amenities details"),
    "created_at":  fields.String(description="Creation date"),
    "updated_at":  fields.String(description="Last update date")
})


@ns.route("/")
class PlaceList(Resource):

    @ns.marshal_list_with(place_response)
    @ns.response(200, "List of places retrieved successfully")
    def get(self):
        """List all places"""
        return facade.get_all_places(), 200

    @ns.expect(place_model, validate=True)
    @ns.response(201, "Place created successfully")
    @ns.response(400, "Invalid input data")
    def post(self):
        """Create a new place"""
        try:
            place = facade.create_place(request.json)
            return place.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:place_id>")
@ns.param("place_id", "The place identifier")
class PlaceResource(Resource):

    @ns.response(200, "Place found")
    @ns.response(404, "Place not found")
    def get(self, place_id):
        """Get a place by ID with owner details and amenities"""
        place = facade.get_place(place_id)
        if not place:
            ns.abort(404, "Place not found")
        return place, 200

    @ns.expect(place_model, validate=False)
    @ns.response(200, "Place updated successfully")
    @ns.response(400, "Invalid input data")
    @ns.response(404, "Place not found")
    def put(self, place_id):
        """Update a place"""
        if not facade.place_repo.get(place_id):
            ns.abort(404, "Place not found")
        try:
            updated = facade.update_place(place_id, request.json)
            return updated.to_dict(), 200
        except ValueError as e:
            ns.abort(400, str(e))
