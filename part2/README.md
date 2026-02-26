# HBnB - Part 2: Business Logic and API Endpoints

## Description
Implementation of the Presentation and Business Logic layers of the HBnB application using Python and Flask.

## Project Structure

    part2/
    ├── app/
    │   ├── __init__.py
    │   ├── api/
    │   │   └── v1/
    │   │       ├── users.py
    │   │       ├── places.py
    │   │       ├── reviews.py
    │   │       └── amenities.py
    │   ├── models/
    │   │   ├── base_model.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── review.py
    │   │   └── amenity.py
    │   ├── services/
    │   │   └── facade.py
    │   └── persistence/
    │       └── repository.py
    ├── run.py
    ├── README.md
    └── requirements.txt

## Installation

    pip install -r requirements.txt

## Run

    python3 run.py

## API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/users/ | List all users |
| POST | /api/v1/users/ | Create a user |
| GET | /api/v1/users/<id> | Get a user |
| PUT | /api/v1/users/<id> | Update a user |

### Amenities
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/amenities/ | List all amenities |
| POST | /api/v1/amenities/ | Create an amenity |
| GET | /api/v1/amenities/<id> | Get an amenity |
| PUT | /api/v1/amenities/<id> | Update an amenity |
| DELETE | /api/v1/amenities/<id> | Delete an amenity |

### Places
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/places/ | List all places |
| POST | /api/v1/places/ | Create a place |
| GET | /api/v1/places/<id> | Get a place (with owner and amenities) |
| PUT | /api/v1/places/<id> | Update a place |
| DELETE | /api/v1/places/<id> | Delete a place |

### Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/reviews/ | List all reviews |
| POST | /api/v1/reviews/ | Create a review |
| GET | /api/v1/reviews/<id> | Get a review |
| PUT | /api/v1/reviews/<id> | Update a review |
| DELETE | /api/v1/reviews/<id> | Delete a review |
| GET | /api/v1/reviews/places/<id> | Get all reviews for a place |

## Architecture
- Presentation Layer: Flask + flask-restx (REST API + Swagger doc)
- Business Logic Layer: Models with validation + Facade pattern
- Persistence Layer: In-memory repository (to be replaced by SQLAlchemy in Part 3)

## Testing
Swagger UI available at: http://localhost:5000
