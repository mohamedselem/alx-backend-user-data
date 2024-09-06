#!/usr/bin/env python3
""" BasicAuth module for API authentication
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracts the base64 part of the Authorization header
        for Basic Authentication
        Arg(s):
          authorization_header (str): The Authorization header
        Returns:
          str: The base64 part of the Authorization header, or None if invalid
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        # we remove the "Basic " prefix to get the base64 part
        base64_str = authorization_header[6:]
        return base64_str

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ Decodes the Base64 part of the Authorization header
        for the Basic Authentication.
        Arg(s):
            base64_authorization_header (str): The base64 part of the
            Authorization header
        Returns:
            str: The decoded value of the Base64 string, or None if invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # we decode the base64 string
            base64_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(base64_bytes)
            message = decoded_bytes.decode('utf-8')
            return message
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Extracts the user credentials (email and password)
        from the Base64 decoded value.
        Args:
          decoded_base64_authorization_header (str): The decoded Base64 value
        Returns:
          (str, str): The user email and password, or (None, None) if invalid
        """
        db64_ah = decoded_base64_authorization_header
        if db64_ah is None:
            return None, None
        if not isinstance(db64_ah, str):
            return None, None
        if ":" not in db64_ah:
            return None, None
        # we split the decoded string to get the email and password
        email, password = db64_ah.split(":", 1)
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Retrieves the User instance based on the email and password.
        Args:
            user_email (str): The user's email address
            user_pwd (str): The user's password
        Returns:
            User: The User instance, or None if not found
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            # we search the user based on the email
            user_list = User.search({"email": user_email})
            if not user_list or user_list == []:  # check if user is valid
                return None
            for user in user_list:
                # iterate over users and check if password is valid
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception as e:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request.
        """
        # we get the Authorization header from the request
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        # extract the base64 part of the Authorization header
        base64_ah = self.extract_base64_authorization_header(auth_header)
        if base64_ah is None:
            return None
        # decode the base64 part of the Authorization header
        decoded_ah = self.decode_base64_authorization_header(base64_ah)
        if decoded_ah is None:
            return None
        # extract the user credentials from the decoded value
        user_email, user_pwd = self.extract_user_credentials(decoded_ah)
        if user_email is None or user_pwd is None:
            return None
        # get the User instance based on the email and password
        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
