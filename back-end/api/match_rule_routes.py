from flask import Blueprint, jsonify, request
from utils.auth_decorator import require_auth
from services.match_rule_service import MatchRuleService

match_rule_bp = Blueprint("match_rules", __name__)
match_rule_service = MatchRuleService()


@match_rule_bp.get("")
@require_auth
def list_match_rules():
    user = request.user
    return jsonify({"success": True, "items": match_rule_service.list_rules(user['sub'])})


@match_rule_bp.post("")
@require_auth
def create_match_rule():
    user = request.user
    payload = request.get_json(silent=True) or {}
    
    if not payload.get('rule_name') or not payload.get('include_keywords'):
        return jsonify({"success": False, "message": "조건 명칭과 포함 키워드는 필수입니다."}), 400

    try:
        rule = match_rule_service.create_rule(user['sub'], payload)
        return jsonify({"success": True, "message": "관심 조건이 저장되었습니다.", "rule": rule}), 201
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "저장 중 오류가 발생했습니다."}), 500


@match_rule_bp.delete("/<rule_id>")
@require_auth
def delete_match_rule(rule_id):
    user = request.user
    deleted = match_rule_service.delete_rule(rule_id, user['sub'])
    if not deleted:
        return jsonify({"success": False, "message": "조건을 찾을 수 없거나 권한이 없습니다."}), 404
    return jsonify({"success": True, "message": "성공적으로 삭제되었습니다."}), 200
