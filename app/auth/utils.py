from argon2 import PasswordHasher, exceptions
from argon2.exceptions import Argon2Error

"""
This module provides a PasswordManager class that encapsulates password
hashing and verification using the Argon2 algorithm from the argon2-cffi library.
"""


class PasswordManager:
    """
    A class to manage password hashing and verification using Argon2.
    """

    def __init__(
        self,
        time_cost: int = 2,
        memory_cost: int = 102400, 
        parallelism: int = 8,
        hash_len: int = 32,
        salt_len: int = 16
    ):
        """
        Initialize the PasswordManager with custom Argon2 parameters.

        :param time_cost: The number of iterations (increases computational cost).
        :param memory_cost: The amount of memory (in kilobytes) used during hashing.
        :param parallelism: The number of parallel threads used.
        :param hash_len: The length of the resulting hash.
        :param salt_len: The length of the randomly generated salt.
        """
        self.hasher = PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=hash_len,
            salt_len=salt_len
        )

    def get_hashed_password(self, password: str) -> str:
        """
        Hash the provided password using the Argon2 algorithm.

        :param password: The plain text password to hash.
        :return: The resulting password hash as a string.
        :raises Exception: If an error occurs during the hashing process.
        """
        try:
            return self.hasher.hash(password)
        except Argon2Error  as e:
            # Raise a generic exception with additional context.
            raise Exception("Error occurred while hashing the password") from e

    def verify_password(self, hashed_password: str, password: str) -> bool:
        """
        Verify that the provided plain text password matches the hashed password.

        :param hashed_password: The hashed password to verify against.
        :param password: The plain text password to check.
        :return: True if the password is valid, False otherwise.
        :raises Exception: If an unexpected error occurs during verification.
        """
        try:
            return self.hasher.verify(hashed_password, password)
        except exceptions.VerifyMismatchError:
            # The password does not match the hash.
            return False
        except exceptions.Argon2Error as e:
            # Raise a generic exception with additional context.
            raise Exception("Error occurred while verifying the password") from e
        

password_manager = PasswordManager()

