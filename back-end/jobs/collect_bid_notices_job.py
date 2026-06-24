from config import Config
from core.schema_manager import sync_database_schema
from services.g2b_collector_service import G2BCollectorService


def run():
    if Config.DB_AUTO_SYNC_SCHEMA:
        sync_database_schema()

    collector = G2BCollectorService()
    return collector.collect()


if __name__ == "__main__":
    print(run())
