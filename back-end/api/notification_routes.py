from flask import Blueprint, jsonify, request
from core.database import get_connection
from utils.auth_decorator import require_auth
import pymysql

notification_bp = Blueprint('notifications', __name__)

@notification_bp.get('')
@require_auth
def get_notifications():
    user = request.user
    limit = int(request.args.get('limit', 20))
    
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 1. Unread count
            cursor.execute("SELECT count(*) as unread FROM app_notifications WHERE user_id=%s AND is_read=0", (user['sub'],))
            unread = cursor.fetchone()['unread']
            
            # 2. Notification list
            sql = "SELECT * FROM app_notifications WHERE user_id=%s ORDER BY id DESC LIMIT %s"
            cursor.execute(sql, (user['sub'], limit))
            items = cursor.fetchall()
            
            return jsonify({
                "success": True, 
                "items": items,
                "unreadCount": unread
            }), 200
    except Exception as e:
        print("Notification error:", e)
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()

@notification_bp.put('/<int:noti_id>/read')
@require_auth
def mark_as_read(noti_id):
    user = request.user
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE app_notifications SET is_read=1 WHERE id=%s AND user_id=%s", (noti_id, user['sub']))
        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()
        
@notification_bp.put('/read-all')
@require_auth
def mark_all_as_read():
    user = request.user
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE app_notifications SET is_read=1 WHERE user_id=%s AND is_read=0", (user['sub'],))
        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()
