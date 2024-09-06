#!/usr/bin/env python3

""" SessionExpAuth module for API authentication
"""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class that inherits from SessionAuth with expiration
    """

    def __init__(self):
        """ Initialize the SessionExpAuth instance with session duration
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with expiration time
        Args:
            user_id: The user ID
        Returns:
            The session ID created
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get the user ID associated with the session ID
        Args:
            session_id: The session ID
        Returns:
            The user ID or None if the session ID is invalid
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if "created_at" not in session_dict.keys():
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        browse_time = created_at + timedelta(seconds=self.session_duration)
        if browse_time < datetime.now():
            return None

        return session_dict.get("user_id")
