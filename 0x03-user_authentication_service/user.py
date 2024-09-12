#!/usr/bin/env python3

""" User module for database named users.
Using the mapping declaration pattern.
Contain the following attributes:
  -  id
  - email
  - hashed_password
  - session_id
  - reset_token
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

# we create base using the declarative_base function
# for the mapping declaration pattern to be used
Base = declarative_base()


# define User class inheriting from Base
class User(Base):
    """ User class to interact with the MySQL users table
    """
    __tablename__ = 'users'  # Name of the MySQL table

    id = Column(Integer, primary_key=True)  # primary key column
    # Non-nullable email string column
    email = Column(String(250), nullable=False)
    # Non-nullable hashed_password string column
    hashed_password = Column(String(250), nullable=False)
    # Nullable string column for session_id
    session_id = Column(String(250), nullable=True)
    # Nullable string column for reset_token
    reset_token = Column(String(250), nullable=True)
