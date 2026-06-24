import pymysql
from core.database import get_connection

class MatchRuleRepository:
    def list(self, user_id):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM user_match_rules WHERE user_id = %s ORDER BY created_at DESC"
                cursor.execute(sql, (user_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    def create(self, user_id, payload):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO user_match_rules 
                    (user_id, rule_name, include_keywords, exclude_keywords, region, biz_types, notification_enabled)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    user_id,
                    payload.get("rule_name"),
                    payload.get("include_keywords"),
                    payload.get("exclude_keywords", ""),
                    payload.get("region", "전국"),
                    payload.get("biz_types", "전체 업종"),
                    payload.get("notification_enabled", True)
                ))
                rule_id = cursor.lastrowid
            conn.commit()
            return self.get_by_id(rule_id)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_by_id(self, rule_id):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM user_match_rules WHERE id = %s"
                cursor.execute(sql, (rule_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    def update(self, rule_id, payload):
        pass # Currently not needed for MVP

    def delete(self, rule_id, user_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM user_match_rules WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (rule_id, user_id))
                deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
