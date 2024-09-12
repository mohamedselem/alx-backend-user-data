#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # Create an engine to connect to the SQLite database file "a.db"
        # can set echo to False to hide the SQL queries in the output
        self._engine = create_engine("sqlite:///a.db", echo=False)
        # Drop all existing tables defined in the Base metadata
        # from the database
        Base.metadata.drop_all(self._engine)
        # Create all tables defined in the Base metadata in the database
        Base.metadata.create_all(self._engine)
        # Initialize the session as None
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        # Check if session is already created
        if self.__session is None:
            # Create a session using sessionmaker and bind it to the engine
            DBSession = sessionmaker(bind=self._engine)
            # Assign the created session to the private variable __session
            self.__session = DBSession()
        # Return the session object
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add the user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Find any given User by the passed keyword arguments.
        Args:
            **kwargs: Arbitrary keyword arguments to filter users
        Result:
            User: The first matching result of the User object.
        Raises:
            NoResultFound: If no results are found.
            InvalidRequestError: If the request is invalid.
        """
        # Query all users from the session
        all_users = self._session.query(User)

        # Iterate over the keyword arguments passed
        for key, value in kwargs.items():
            # Check if the key is not an attribute of the User class
            if key not in User.__dict__:
                # Raise an InvalidRequestError if the attribute is not found
                raise InvalidRequestError
            # Iterate over each user in the query result
            for user in all_users:
                # Check if the attribute value of the user matches
                # the specified value
                if getattr(user, key) == value:
                    return user  # Return the user if a match is found
        # Raise a NoResultFound exception if no matching user is found
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a Users attributes
        Args:
            user_id (int): The user id
            **kwargs: Arbitrary keyword arguments to update the user
        Raises:
            ValueError: If the user is not found
        Returns:
            None
        """
        user = self.find_user_by(id=user_id)

        try:
            user
        except NoResultFound:
            raise ValueError

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError

        self._session.commit()
