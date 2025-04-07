def is_username_valid(username = "") -> dict:
    if not username:
        return {"success": False, "message": "Username cannot be empty."}
    if len(username) < 3 or len(username) > 20:
        return {"success": False, "message": "Username must be between 3 and 20 characters."}
    if not username.isalnum():
        return {"success": False, "message": "Username can only contain letters and numbers."}
    return {"success": True, "message": "Username is valid."}

def is_password_valid(password = "") -> dict:
    if not password:
        return {"success": False, "message": "Password cannot be empty."}
    if len(password) < 8:
        return {"success": False, "message": "Password must be at least 8 characters long."}
    if len(password) > 80:
        return {"success": False, "message": "Password must be at most 80 characters long."}
    if not any(char.isdigit() for char in password):
        return {"success": False, "message": "Password must contain at least one digit."}
    if not any(char.isalpha() for char in password):
        return {"success": False, "message": "Password must contain at least one letter."}
    return {"success": True, "message": "Password is valid."}