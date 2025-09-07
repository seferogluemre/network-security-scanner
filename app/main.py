import sys
import os
# Ana dizini Python path'ine ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from flask_cors import CORS
from app.config.settings import get_config
from app.config.database import init_database, db
from app.controllers.scan_controller import scan_bp
from app.utils.logger import setup_logger

def create_app(config_name: str = None) -> Flask:
    """Flask app factory"""
    
    logger = setup_logger("netscout.app", "INFO")
    logger.info("🚀 NetScout Enterprise Backend starting...")
    
    app = Flask(__name__)
    logger.info("✅ Flask app created")
    
    config = get_config(config_name)
    app.config.from_object(config)
    logger.info(f"⚙️  Configuration loaded: {config.__class__.__name__}")
    
    CORS(app)
    logger.info("🌐 CORS enabled")
    
    logger.info("🗄️  Initializing database...")
    init_database(app)
    logger.info("✅ Database initialized")
    
    logger.info("📋 Registering blueprints...")
    app.register_blueprint(scan_bp)
    logger.info("✅ Scan controller registered")
    
    register_error_handlers(app, logger)
    logger.info("⚠️  Error handlers registered")
    
    @app.route('/health', methods=['GET'])
    def health_check():
        logger.info("🩺 Global health check requested")
        return jsonify({
            'status': 'healthy',
            'service': 'NetScout Enterprise API',
            'version': '2.0.0',
            'database': 'connected' if db else 'disconnected',
            'environment': app.config.get('ENV', 'development')
        }), 200
    
    @app.route('/api/info', methods=['GET'])
    def api_info():
        logger.info("ℹ️  API info requested")
        return jsonify({
            'service': 'NetScout Enterprise API',
            'version': '2.0.0',
            'author': 'Emre Seferoğlu',
            'description': 'Enterprise Network Security Scanner',
            'endpoints': {
                'health': '/health',
                'api_info': '/api/info',
                'scan_endpoints': '/api/v2/scan/*',
                'documentation': '/api/docs'
            },
            'features': [
                'Multi-threaded port scanning',
                'Network discovery',
                'Host management',
                'Scan history',
                'Statistics',
                'Enterprise logging'
            ]
        }), 200
    
    @app.route('/', methods=['GET'])
    def home():
        logger.info("🏠 Home page requested")
        return jsonify({
            'message': 'Welcome to NetScout Enterprise API',
            'version': '2.0.0',
            'status': 'running',
            'docs': '/api/info',
            'health': '/health'
        }), 200
    
    logger.info("🎉 NetScout Enterprise Backend ready!")
    return app

def register_error_handlers(app: Flask, logger):
    """Register global error handlers"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"⚠️  404 Not Found: {error}")
        return jsonify({
            'success': False,
            'message': 'Endpoint not found',
            'error_code': 'NOT_FOUND',
            'available_endpoints': [
                '/health',
                '/api/info',
                '/api/v2/scan/ports',
                '/api/v2/scan/fast',
                '/api/v2/scan/history'
            ]
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        logger.warning(f"⚠️  405 Method Not Allowed: {error}")
        return jsonify({
            'success': False,
            'message': 'Method not allowed',
            'error_code': 'METHOD_NOT_ALLOWED'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"💥 500 Internal Server Error: {error}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error_code': 'INTERNAL_ERROR'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"💥 Unhandled Exception: {error}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred',
            'error_code': 'UNEXPECTED_ERROR'
        }), 500

if __name__ == '__main__':
    config_name = os.environ.get('FLASK_ENV', 'development')
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    app = create_app(config_name)
    
    print("🚀 Starting NetScout Enterprise Server...")
    print("=" * 60)
    print(f"🌐 URL: http://localhost:{port}")
    print(f"📋 Environment: {config_name}")
    print(f"🗄️  Database: SQLite")
    print("\n📡 Available Endpoints:")
    print("   GET  /                     - Home page")
    print("   GET  /health               - Health check")
    print("   GET  /api/info             - API information")
    print("   POST /api/v2/scan/ports    - Port scanning")
    print("   POST /api/v2/scan/fast     - Fast scanning")
    print("   GET  /api/v2/scan/history  - Scan history")
    print("   GET  /api/v2/scan/<id>     - Specific scan")
    print("   GET  /api/v2/scan/stats    - Statistics")
    print("\n✨ Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(
        host=host,
        port=port,
        debug=(config_name == 'development')
    )