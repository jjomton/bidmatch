import json
import threading
import time
from datetime import datetime

from config import Config
from core.schema_manager import sync_database_schema
from services.g2b_collector_service import G2BCollectorService

_background_worker_started = False
_background_worker_lock = threading.Lock()


def run_once():
    if Config.DB_AUTO_SYNC_SCHEMA:
        sync_database_schema()

    collector = G2BCollectorService()
    collect_result = collector.collect()
    result = {"collection": collect_result}

    if Config.G2B_BACKFILL_AFTER_COLLECT:
        result["license_backfill"] = collector.backfill_license_limits(
            limit=Config.G2B_LICENSE_BACKFILL_LIMIT
        )

    result["ran_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result["lookback_hours"] = Config.G2B_LOOKBACK_HOURS
    result["backfill_after_collect"] = Config.G2B_BACKFILL_AFTER_COLLECT
    return result


def run_forever():
    print(
        "[hourly-collector] started "
        f"interval_seconds={Config.G2B_COLLECT_INTERVAL_SECONDS} "
        f"lookback_hours={Config.G2B_LOOKBACK_HOURS} "
        f"backfill_after_collect={Config.G2B_BACKFILL_AFTER_COLLECT} "
        f"backfill_limit={Config.G2B_LICENSE_BACKFILL_LIMIT}",
        flush=True,
    )

    if not Config.G2B_COLLECT_RUN_ON_START:
        time.sleep(Config.G2B_COLLECT_INTERVAL_SECONDS)

    while True:
        try:
            result = run_once()
            print(json.dumps(result, ensure_ascii=False, default=str), flush=True)
        except Exception as exc:
            print(
                json.dumps(
                    {
                        "ran_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "FAILED",
                        "error": str(exc),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

        time.sleep(Config.G2B_COLLECT_INTERVAL_SECONDS)


def start_background_worker():
    global _background_worker_started

    with _background_worker_lock:
        if _background_worker_started:
            return None

        thread = threading.Thread(
            target=run_forever,
            name="g2b-hourly-collector",
            daemon=True,
        )
        thread.start()
        _background_worker_started = True
        return thread


if __name__ == "__main__":
    run_forever()
