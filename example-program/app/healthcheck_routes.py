from flask import Blueprint, jsonify

# Create a Blueprint for health check routes
# The url_prefix will be prepended to all routes defined in this blueprint
health_bp = Blueprint('health', __name__, url_prefix='/api/v1')

@health_bp.route('/healthz', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Returns a 200 OK status if the service is healthy.
    """
    reurn jsonify({"status": "ok", "message": "Service is healthy"}), 200