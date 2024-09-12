#!/usr/bin/env python3

"""
Main file for End-to-end Integration test for User Authentication Service.
Use the requests module to query your web server for
  the corresponding end-point.
Use assert to validate the response’s expected status code and payload
  (if any) for each task.
- register_user(email: str, password: str) -> None
- log_in_wrong_password(email: str, password: str) -> None
- log_in(email: str, password: str) -> str
- profile_unlogged() -> None
- profile_logged(session_id: str) -> None
- log_out(session_id: str) -> None
- reset_password_token(email: str) -> str
- update_password(email: str, reset_token: str, new_password: str) -> None
"""

import requests

BASE_URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """ (Test) Register a new user with given email and password.
    Args:
        email (str): The user's email.
        password (str): The user's password.
    Returns:
        None
    """
    url = f'{BASE_URL}/users'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        assert (response.json() == {"email": email, "message": "user created"})
    else:
        assert (response.status_code == 400)
        assert (response.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """ (Test) Attempt to log in with the wrong password.
    Args:
        email (str): The user's email.
        password (str): The user's password.
    Returns:
        None
    """
    url = f'{BASE_URL}/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert (response.status_code == 401)


def log_in(email: str, password: str) -> str:
    """ (Test) Log in with the correct password.
    Args:
        email (str): The user's email.
        password (str): The user's password.
    Returns:
        str: The session ID of the logged-in user.
    """
    url = f'{BASE_URL}/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert (response.status_code == 200)
    assert (response.json() == {"email": email, "message": "logged in"})
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """ (Test) Attempt to access profile without logging in.
    Returns:
        None
    """
    url = f'{BASE_URL}/profile'
    response = requests.get(url)
    assert (response.status_code == 403)


def profile_logged(session_id: str) -> None:
    """ (Test) Access profile after logging in.
    Args:
        session_id (str): The session ID of the logged-in user.
    Returns:
        None
    """
    url = f'{BASE_URL}/profile'
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert (response.status_code == 200)


def log_out(session_id: str) -> None:
    """ (Test) Log out the user.
    Args:
        session_id (str): The session ID of the logged-in user.
    Returns:
        None
    """
    url = f'{BASE_URL}/sessions'
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)
    if response.status_code == 302:
        assert (response.url == f'{BASE_URL}/')
    else:
        assert (response.status_code == 200)


def reset_password_token(email: str) -> str:
    """ (Test) Generate a reset password token for the user.
    Args:
        email (str): The user's email.
    Returns:
        str: The reset password token.
    """
    url = f'{BASE_URL}/reset_password'
    data = {'email': email}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()['reset_token']
    assert (response.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ (Test) Update the user's password with the reset token.
    Args:
        email (str): The user's email.
        reset_token (str): The reset password token.
        new_password (str): The new password.
    Returns:
        None
    """
    url = f'{BASE_URL}/reset_password'
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    response = requests.put(url, data=data)
    if response.status_code == 200:
        assert (response.json() == {"email": email,
                                    "message": "Password updated"})
    else:
        assert (response.status_code == 403)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
