from . import app
import os
import json
import status
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count", methods=["GET"])
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), status.HTTP_200_OK

    return {"message": "Internal server error"}, status.HTTP_500_SERVER_ERROR


######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/pictures", methods=["GET"])
def get_pictures():
    """Return list of pictures"""
    if data:
        return jsonify(data), status.HTTP_200_OK

    return {"message": "Internal server error"}, status.HTTP_500_SERVER_ERROR


######################################################################
# GET A PICTURE BY ID
######################################################################

@app.route("/pictures/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # Iterate through the 'data' list to search for a picture with a matching ID
    for picture in data:
        # Check if the 'id' field of the picture matches the 'id' parameter
        if picture["id"] == int(id):
            # Return the matching picture as a JSON response with a 200 OK status code
            return picture, status.HTTP_200_OK
    # If no matching picture is found, return a JSON response with a message and a 404 Not Found status code
    return {"message": "picture not found"}, status.HTTP_404_NOT_FOUND


######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/pictures", methods=["POST"])
def create_picture():
    """Create new picture"""
    new_picture = request.json
    if not new_picture:
        return {"Message": "Invalid input parameter"}, status.HTTP_422_UNPROCESSABLE_ENTITY
    # Iterate through the 'data' list to search for a picture with a matching ID
    for picture in data:
        # Check if the 'id' field of the picture matches the 'id' parameter
        if picture["id"] == new_picture['id']:
            return {"Message": f"picture with id {picture['id']} already present"}, 302
    # code to validate new_picture ommited
    try:
        data.append(new_picture)
    except NameError:
        return {"Message": "data not defined"}, status.HTTP_500_SERVER_ERROR

    return {"id": new_picture['id']}, status.HTTP_201_CREATED


######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/pictures/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture"""
    # find the picture by id
    picture = next((picture for picture in data if picture['id'] == id), None)
    
    if picture is None:
        return jsonify({'message': 'picture not found'}), status.HTTP_404_NOT_FOUND

    # Get the picture data from the request
    picture_data = request.get_json()

    # Update the pictures's event_country if provided
    if 'event_country' in picture_data:
        picture['event_country'] = picture_data['event_country']

    # Update the pictures's event_state if provided
    if 'event_state' in picture_data:
        picture['event_state'] = picture_data['event_state']

    return jsonify(picture), status.HTTP_200_OK


######################################################################
# DELETE A PICTURE BY ID
######################################################################

@app.route("/pictures/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by id"""
    # Iterate through the 'data' list to search for a picture with a matching ID
    for picture in data:
        # Check if the 'id' field of the picture matches the 'id' parameter
        if picture["id"] == int(id):
            # Remove the picture from the 'data' list
            data.remove(picture)
            # Return a JSON response with a empty body and a 204 NO_CONTENT status code
            return '', status.HTTP_204_NO_CONTENT
    # If no matching picture is found, return a JSON response with a message and a 404 Not Found status code
    return {"message": "picture not found"}, status.HTTP_404_NOT_FOUND
