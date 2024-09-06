#!/usr/bin/env python3
"""Auth module for API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Using this function to check if authentication is required
        for a given path
        Args:
            path (str): The path to check
            excluded_paths (List[str]): A list of paths that do not
            require authentication
        Returns:
            bool: True if authentication is required, False otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # we normalize paths to have a / at the end if it doesn't have it
        # if not path.endswith("/"):
        #     path += "/"
        # # check if normalized path is in the excluded_paths
        # if path in excluded_paths:
        #     return False

        # task 13 update: normalize the paths by removing trailing slashes
        normalized_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if normalized_path.startswith(excluded_path[:-1]):
                    return False
            elif normalized_path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the request
        Args:
            request (flask.Request): The Flask request object
        Returns:
            str: Value of the authorization header, None if not present
        """
        if request is None:
            return None
        # get the value of the header
        header_value = request.headers.get('Authorization', None)
        return header_value

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user from the request
        Args:
            request (flask.Request): The Flask request object
        Returns:
            TypeVar('User'): None for now, logic will be implemented later
        """
        return None

    def session_cookie(self, request=None):
        """ Retrieves a cookie value from a request
        Args:
            request (flask.Request): The Flask request object
        Returns:
            str: The cookie value, None if not present
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None

        return request.cookies.get(session_name)
