#!/usr/bin/env python3

""" SessionAuth module for API authentication
"""

from typing import TypeVar
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ Session authentication class.
    """
    # initialize dictionary to store user_id by session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a user_id
        Args:
            user_id: The user_id to create a session for
        Returns:
            The session ID created
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        Args:
            session_id: The session ID to look up
        Returns:
            The user ID associated with the session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a User instance based on a cookie value
        Args:
            request: The request object
        Returns:
            The user associated with the cookie value
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Deletes the user session / logout
        Args:
            request: The request object
        Returns:
            True if session was deleted, False otherwise
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            return False

        return True
