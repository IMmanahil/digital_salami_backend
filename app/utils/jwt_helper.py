from functools import wraps
from flask import request, jsonify, current_app
import jwt

from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        print(f"[DEBUG] Authorization header: {auth_header}")
        token = auth_header.split(" ")[1] if " " in auth_header else None
        print(f"[DEBUG] Extracted token: {token}")

        if not token:
            print("[DEBUG] Token missing")
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            print(f"[DEBUG] Decoded token data: {data}")
            current_user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            print("[DEBUG] Token expired")
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError as e:
            print(f"[DEBUG] Invalid token error: {e}")
            return jsonify({"message": "Invalid token"}), 401

        return f(current_user_id, *args, **kwargs)
    
    return decorated
