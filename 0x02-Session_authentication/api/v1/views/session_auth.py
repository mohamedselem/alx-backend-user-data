#!/usr/bin/env python3

""" Flask View module that handles all routes for Session Authentication.
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_login_session():
    """ POST /api/v1/auth_session/login
    Handles User login
    Return:
      - User object JSON represented
      - 400 if the User ID doesn't exist
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # check if email and password exist, if they don't, return 400
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    # search for users with the given email
    users = User.search({"email": email})
    # if no users found or the list is empty, return 400
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 400
    # we iterate over the users found
    for user in users:
        # check if the password is valid
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 400

        from api.v1.app import auth  # to avoid circular import
        # create a session for the user
        session_id = auth.create_session(user.id)
        # return the user object in JSON format
        response = jsonify(user.to_json())
        session_name = getenv("SESSION_NAME")  # set the session cookie name
        # set the session cookie
        response.set_cookie(session_name, session_id)

        return response
    # if none of the users had a valid password, return 401
    return jsonify({"error:" "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """
    Handle user logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
