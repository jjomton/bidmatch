import os

from app_factory import create_app
from config import Config
from jobs.hourly_collect_bid_notices_worker import start_background_worker

app = create_app()

if __name__ == "__main__":
    if Config.G2B_EMBEDDED_WORKER_ENABLED and (
        not app.config["DEBUG"] or os.getenv("WERKZEUG_RUN_MAIN") == "true"
    ):
        start_background_worker()

    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
