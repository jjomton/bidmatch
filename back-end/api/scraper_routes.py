from flask import Blueprint, jsonify
from services.g2b_scraper_service import g2b_scraper
from utils.auth_decorator import require_auth

scraper_bp = Blueprint('scraper', __name__)

@scraper_bp.post('/run')
@require_auth
def run_scraper():
    try:
        # 최근 24시간 치 데이터 강제 스크래핑 테스트
        inserted = g2b_scraper.fetch_and_store_notices(hours_back=24)
        return jsonify({
            "success": True, 
            "message": f"스크래핑 및 매칭 완료. 신규 공고 {inserted}건 추가됨.",
            "inserted_count": inserted
        }), 200
    except Exception as e:
        print("Scraper error:", e)
        return jsonify({"success": False, "message": str(e)}), 500
