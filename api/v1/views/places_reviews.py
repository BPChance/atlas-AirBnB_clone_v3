#!/usr/bin/python3
""" review objects view """
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """ retrieves list of review objects of a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ retrieve a review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ delete review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ create a review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404, description="User not found")
    if 'text' not in data:
        abort(400, description="Missing text")

    new_review = Review(**data, place_id=place_id)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updates a review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description="Review not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200