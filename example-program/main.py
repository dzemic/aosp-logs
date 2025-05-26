from flask import Flask
from app.healthcheck_routes import health_bp
from app.user_routes import user_bp

def create_app():
    """
    Application factory function.
    Initializes the Flask app and registers blueprints.
    """
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    # Run the app. 
    # debug=True is useful for development, but should be False in production.
    # host='0.0.0.0' makes the server accessible externally (e.g., from other devices on your network)
    app.run(host='0.0.0.0', port=3001, debug=True)