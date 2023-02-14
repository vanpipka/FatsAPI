from fastapi import HTTPException
from unittest import TestCase, main
from auth import Auth


class AuthTest(TestCase):

    auth = Auth()
    password = "JVT_ENCODE_PASSWORD"
    username = "andrei"
    encoding_password = auth.encode_password(password)
    good_jwt_token = auth.encode_token(username=username)
    bad_jwt_token = "..."

    def test_verify_good_password(self):
        self.assertEqual(self.auth.verify_password(self.password, self.encoding_password), True)

    def test_verify_bad_password(self):
        self.assertNotEqual(self.auth.verify_password(self.password[:-1], self.encoding_password), True)

    def test_decode_bad_jwt_token(self):
        with self.assertRaises(HTTPException) as err:
            self.auth.decode_token(jwt_token=self.bad_jwt_token)
        self.assertEqual("Invalid refresh token", err.exception.detail)

    def test_decode_good_jwt_token(self):
        self.assertEqual(self.username, self.auth.decode_token(jwt_token=self.good_jwt_token))


if __name__ == "__main__":
    main()
