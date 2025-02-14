import bcrypt
import pytest
from app.utils.password_utils import hash_password, verify_password


def test_hash_password():
    password = "Aa1662002@"
    hashed_password = hash_password(password)
    print(f"\n- Hashed Password 1: {hashed_password}")

    assert isinstance(hashed_password, str), "Error: The hashed password must be a string."
    assert hashed_password != password, "Error: The hashed password should not match the original password."
    assert bcrypt.checkpw(password.encode("utf-8"),
                          hashed_password.encode("utf-8")), "Error: Password verification failed!"

    hashed_password_2 = hash_password(password)
    print(f"- Hashed Password 2: {hashed_password_2}")

    assert hashed_password != hashed_password_2, "Error: The hashing function should generate different hashes for the same password."

    print("Password hashing test passed!\n")


def test_verify_password():
    password = "Aa1662002@"
    hashed_password = hash_password(password)
    print(f"\n- Hashed Password for Verification: {hashed_password}")

    correct_check = verify_password(password, hashed_password)
    print(f"- Correct Password Verification Result: {correct_check}")
    assert correct_check, "Error: Correct password should be verified successfully!"

    wrong_check = verify_password("WrongPassword", hashed_password)
    print(f"- Wrong Password Verification Result: {wrong_check}")
    assert not wrong_check, "Error: Incorrect password should not be verified!"

    print("Password verification test passed!\n")


def test_empty_password():
    with pytest.raises(ValueError, match="Password cannot be empty."):
        empty_password = ""
        hash_password(empty_password)

    with pytest.raises(ValueError, match="Password cannot be empty."):
        verify_password("", "somehashedpassword")

    print("Empty password test passed!\n")


def test_invalid_input():
    with pytest.raises(ValueError, match="Password cannot be empty."):
        print("- Testing hash_password(None)...")
        hash_password(None)

    with pytest.raises(ValueError, match="Password cannot be empty."):
        print("- Testing verify_password(None, 'somehash')...")
        verify_password(None, "somehash")

    print("Invalid input test passed!\n")


test_hash_password()
test_verify_password()
test_empty_password()
test_invalid_input()
