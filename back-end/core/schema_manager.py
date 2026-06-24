from pymysql import Error

from config import Config
from core.database import get_connection
from core.schema import TABLES


class SchemaManager:
    """Synchronizes the database with the application schema safely."""

    def sync(self):
        with get_connection() as connection:
            try:
                with connection.cursor() as cursor:
                    for table_name, table_schema in TABLES.items():
                        self._create_table_if_missing(cursor, table_name, table_schema)
                        self._add_missing_columns(cursor, table_name, table_schema)
                        self._add_missing_unique_keys(cursor, table_name, table_schema)
                        self._add_missing_indexes(cursor, table_name, table_schema)
                        self._add_missing_foreign_keys(cursor, table_name, table_schema)
                connection.commit()
            except Exception:
                connection.rollback()
                raise

    def _create_table_if_missing(self, cursor, table_name, table_schema):
        definitions = []

        for column_name, column_definition in table_schema["columns"].items():
            definitions.append(f"`{column_name}` {column_definition}")

        primary_key = table_schema.get("primary_key", [])
        if primary_key:
            definitions.append(f"PRIMARY KEY ({self._column_list(primary_key)})")

        for key_name, columns in table_schema.get("unique_keys", {}).items():
            definitions.append(f"UNIQUE KEY `{key_name}` ({self._column_list(columns)})")

        for index_name, columns in table_schema.get("indexes", {}).items():
            definitions.append(f"KEY `{index_name}` ({self._column_list(columns)})")

        for constraint_name, foreign_key in table_schema.get("foreign_keys", {}).items():
            definitions.append(self._foreign_key_sql(constraint_name, foreign_key))

        sql = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            {", ".join(definitions)}
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(sql)

    def _add_missing_columns(self, cursor, table_name, table_schema):
        existing_columns = self._get_existing_columns(cursor, table_name)

        for column_name, column_definition in table_schema["columns"].items():
            if column_name in existing_columns:
                continue

            cursor.execute(
                f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {column_definition}"
            )

    def _add_missing_unique_keys(self, cursor, table_name, table_schema):
        existing_indexes = self._get_existing_indexes(cursor, table_name)

        for key_name, columns in table_schema.get("unique_keys", {}).items():
            if key_name in existing_indexes:
                continue

            cursor.execute(
                f"ALTER TABLE `{table_name}` ADD UNIQUE KEY `{key_name}` ({self._column_list(columns)})"
            )

    def _add_missing_indexes(self, cursor, table_name, table_schema):
        existing_indexes = self._get_existing_indexes(cursor, table_name)

        for index_name, columns in table_schema.get("indexes", {}).items():
            if index_name in existing_indexes:
                continue

            cursor.execute(
                f"ALTER TABLE `{table_name}` ADD INDEX `{index_name}` ({self._column_list(columns)})"
            )

    def _add_missing_foreign_keys(self, cursor, table_name, table_schema):
        existing_constraints = self._get_existing_constraints(cursor, table_name)

        for constraint_name, foreign_key in table_schema.get("foreign_keys", {}).items():
            if constraint_name in existing_constraints:
                continue

            try:
                cursor.execute(
                    f"ALTER TABLE `{table_name}` ADD {self._foreign_key_sql(constraint_name, foreign_key)}"
                )
            except Error as exc:
                print(
                    f"[schema-sync] Foreign key `{constraint_name}` was skipped. "
                    f"Check existing data before adding it manually. reason={exc}"
                )

    def _get_existing_columns(self, cursor, table_name):
        cursor.execute(
            """
            SELECT COLUMN_NAME
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            """,
            (Config.DB_NAME, table_name),
        )
        return {row["COLUMN_NAME"] for row in cursor.fetchall()}

    def _get_existing_indexes(self, cursor, table_name):
        cursor.execute(
            """
            SELECT DISTINCT INDEX_NAME
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            """,
            (Config.DB_NAME, table_name),
        )
        return {row["INDEX_NAME"] for row in cursor.fetchall()}

    def _get_existing_constraints(self, cursor, table_name):
        cursor.execute(
            """
            SELECT CONSTRAINT_NAME
            FROM information_schema.TABLE_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = %s
              AND TABLE_NAME = %s
              AND CONSTRAINT_TYPE = 'FOREIGN KEY'
            """,
            (Config.DB_NAME, table_name),
        )
        return {row["CONSTRAINT_NAME"] for row in cursor.fetchall()}

    def _foreign_key_sql(self, constraint_name, foreign_key):
        sql = (
            f"CONSTRAINT `{constraint_name}` "
            f"FOREIGN KEY ({self._column_list(foreign_key['columns'])}) "
            f"REFERENCES {foreign_key['references']}"
        )

        on_delete = foreign_key.get("on_delete")
        if on_delete:
            sql += f" ON DELETE {on_delete}"

        return sql

    def _column_list(self, columns):
        return ", ".join(f"`{column}`" for column in columns)


def sync_database_schema():
    SchemaManager().sync()


if __name__ == "__main__":
    sync_database_schema()
    print("[schema-sync] Database schema synchronization completed.")
