#!/usr/bin/env python3

""" User authentication service module
"""

import bcrypt
from db import DB
from uuid import uuid4
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Takes in a password string arguments and returns a salted hash.
    Args:
        password (str): The password string to hash.
    Returns:
        bytes: The hashed password.
    """
    # generate a salted hash for the password
    salt = bcrypt.gensalt()
    # hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def _generate_uuid() -> str:
    """ Generates a unique UUID for a user.
    Returns:
        str: A string representation of new unique UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user by hashing the password and adding the user
        to the database.
        Args:
            email (str): The email of the new user.
            password (str): The password of the new user
        Returns:
            User: The newly created User object.
        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # user doesn't exist, we proceed to create new user
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate a user's login credentials.
        Args:
            email (str): The user's email.
            password (str): The user's password.
        Returns:
            bool: True if the password is valid, False otherwise.
        """
        try:
            # Find the user by email in the database
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # If user is not found, return False
            return False

        # Get the hashed password of the user
        user_pwd = user.hashed_password
        # Check if the provided password matches the hashed password
        return bcrypt.checkpw(password.encode("utf-8"), user_pwd)

    def create_session(self, email: str) -> str:
        """ Create a new session ID for the user.
        Args:
            email (str): The user's email.
        Returns:
            str: The new session ID if user is found, None otherwise.
        """
        try:
            # Find the user by email in the database
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # If user is not found, return None
            return None

        session_id = _generate_uuid()  # Generate a new session ID
        # Update the user's session ID in the database
        self._db.update_user(user.id, session_id=session_id)

        return session_id  # Return the new session ID

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Takws a session ID and returns the corresponding user, if session
        ID is valid. None if otherwise.
        Args:
            session_id (str): session_id for the user.
        Returns:
            User: The user corresponding to the session ID.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Takes a user's user_id and destroys the user's session then update
        their session_id to None.
        Arg(s):
            user_id (int): The user's user_id.
        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generates a reset password token for the user with the given email.
        Args:
            email (str): The user's email.
        Returns:
            str: The new reset token.
        """
        try:  # Find the user by email in the database
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # If user is not found, raise a ValueError
            raise ValueError("User not found")

        reset_token = _generate_uuid()  # Generate a new reset token
        # Update the user's reset token in the database
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token  # Return the new reset token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update the password of the user with the given reset token.
        Args:
            reset-token: The reset token of the user.
            password: The new password of the user.
        Returns:
            None
        """
        try:  # Find the user by reset_token in the database
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("User not found")

        hashed_pwd = _hash_password(password)  # hashes the new password
        # Update the user's hashed password in the database
        self._db.update_user(user.id, hashed_password=hashed_pwd,
                             reset_token=None)
