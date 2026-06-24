import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    DEBUG = os.getenv("FLASK_ENV") == "development"

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "bidmatch")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_AUTO_SYNC_SCHEMA = os.getenv("DB_AUTO_SYNC_SCHEMA", "false").lower() == "true"

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")

    G2B_API_KEY = os.getenv("G2B_API_KEY", "")
    G2B_API_BASE_URL = os.getenv(
        "G2B_API_BASE_URL",
        "http://apis.data.go.kr/1230000/ad/BidPublicInfoService",
    )
    G2B_COLLECT_ENDPOINTS = os.getenv(
        "G2B_COLLECT_ENDPOINTS",
        "getBidPblancListInfoServc,getBidPblancListInfoThng",
    )
    G2B_INQRY_DIV = os.getenv("G2B_INQRY_DIV", "1")
    G2B_LOOKBACK_HOURS = int(os.getenv("G2B_LOOKBACK_HOURS", "2"))
    G2B_NUM_OF_ROWS = int(os.getenv("G2B_NUM_OF_ROWS", "100"))
    G2B_COLLECT_INTERVAL_SECONDS = int(os.getenv("G2B_COLLECT_INTERVAL_SECONDS", "3600"))
    G2B_COLLECT_RUN_ON_START = os.getenv("G2B_COLLECT_RUN_ON_START", "true").lower() == "true"
    G2B_EMBEDDED_WORKER_ENABLED = os.getenv("G2B_EMBEDDED_WORKER_ENABLED", "false").lower() == "true"
    G2B_REQUEST_DELAY_SECONDS = float(os.getenv("G2B_REQUEST_DELAY_SECONDS", "1.0"))
    G2B_MAX_RETRIES = int(os.getenv("G2B_MAX_RETRIES", "3"))
    G2B_RETRY_BASE_DELAY_SECONDS = float(os.getenv("G2B_RETRY_BASE_DELAY_SECONDS", "5.0"))
    G2B_BACKFILL_AFTER_COLLECT = os.getenv("G2B_BACKFILL_AFTER_COLLECT", "true").lower() == "true"
    G2B_LICENSE_BACKFILL_LIMIT = int(os.getenv("G2B_LICENSE_BACKFILL_LIMIT", "20"))

    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
