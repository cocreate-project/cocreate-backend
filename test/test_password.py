from cocreate.utils import password


def test_hash_password():
    password_str = "1234"
    hashed_password = password.hash(password_str)

    assert isinstance(hashed_password, bytes)
    assert len(hashed_password) > 0


def test_valid_password():
    password_str = "1234"
    hashed_password = password.hash(password_str)

    assert password.valid(password_str, hashed_password) is True
    assert password.valid("wrong_password", hashed_password) is False
