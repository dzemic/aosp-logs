from flask import Blueprint, jsonify, request

# Create a Blueprint for user routes
user_bp = Blueprint('user', __name__, url_prefix='/api/v1/user')

# In-memory "database" for dummy users
# For a real application, you'd use a proper database.
dummy_users = {
    1: {"id": 1, "username": "alice_b", "email": "alice@example.com", "first_name": "Alice", "last_name": "Wonder"},
    2: {"id": 2, "username": "bob_c", "email": "bob@example.com", "first_name": "Bob", "last_name": "Marley"},
    3: {"id": 3, "username": "charlie_d", "email": "charlie@example.com", "first_name": "Charlie", "last_name": "Chaplin"},
    4: {"id": 4, "username": "diana_e", "email": "diana@example.com", "first_name": "Diana", "last_name": "Prince"},
}
# To keep track of the next user ID for new users
next_user_id = 5

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a specific user by their ID.
    """
    user = dummy_users.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@user_bp.route('', methods=['POST']) # Note: empty route string as prefix is already /api/v1/user
def create_user():
    """
    Create a new user.
    Expects JSON data matching the user structure.
    """
    global next_user_id # To modify the global variable

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Basic validation (in a real app, you'd use a schema validation library like Marshmallow or Pydantic)
    required_fields = ["username", "email", "first_name", "last_name"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields", "required": required_fields}), 400
    
    # Check if username or email already exists (simple check for this example)
    for existing_user in dummy_users.values():
        if existing_user["username"] == data["username"]:
            return jsonify({"error": f"Username '{data['username']}' already exists"}), 409 # 409 Conflict
        if existing_user["email"] == data["email"]:
            return jsonify({"error": f"Email '{data['email']}' already exists"}), 409

    new_user_id = next_user_id
    new_user = {
        "id": new_user_id,
        "username": data["username"],
        "email": data["email"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
    }

    dummy_users[new_user_id] = new_user
    next_user_id += 1

    return jsonify(new_user), 201 # 201 Created