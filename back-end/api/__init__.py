from api.health_routes import health_bp
from api.bid_notice_routes import bid_notice_bp
from api.match_rule_routes import match_rule_bp
from api.email_history_routes import email_history_bp
from api.auth_routes import auth_bp
from api.scraper_routes import scraper_bp
from api.admin_routes import admin_bp
from api.notification_routes import notification_bp

def register_blueprints(app):
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(bid_notice_bp, url_prefix="/api/bid-notices")
    app.register_blueprint(match_rule_bp, url_prefix="/api/match-rules")
    app.register_blueprint(scraper_bp, url_prefix="/api/scraper")
    app.register_blueprint(email_history_bp, url_prefix="/api/email-histories")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(notification_bp, url_prefix="/api/notifications")
