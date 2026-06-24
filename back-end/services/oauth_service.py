import os
import requests
from urllib.parse import urlencode

class OAuthService:
    def get_google_login_url(self):
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5173/oauth/callback/google")
        
        if not client_id or client_id == 'your-google-client-id':
            return None, "Google Client ID가 설정되지 않았습니다."
            
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "email profile openid",
            "access_type": "offline",
            "prompt": "consent"
        }
        return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params), None

    def get_kakao_login_url(self):
        client_id = os.environ.get("KAKAO_CLIENT_ID")
        redirect_uri = os.environ.get("KAKAO_REDIRECT_URI", "http://localhost:5173/oauth/callback/kakao")
        
        if not client_id or client_id == 'your-kakao-client-id':
            return None, "Kakao Client ID가 설정되지 않았습니다."
            
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        }
        return "https://kauth.kakao.com/oauth/authorize?" + urlencode(params), None

    def process_google_callback(self, code):
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5173/oauth/callback/google")
        
        # 1. Exchange code for token
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        
        res = requests.post(token_url, data=data)
        if not res.ok:
            return None, f"Failed to get Google token: {res.text}"
            
        access_token = res.json().get("access_token")
        
        # 2. Get user info
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_res = requests.get(user_info_url, headers=headers)
        
        if not user_res.ok:
            return None, "Failed to get user profile from Google"
            
        profile = user_res.json()
        return {
            "provider": "google",
            "oauth_id": profile.get("id"),
            "email": profile.get("email"),
            "name": profile.get("name")
        }, None

    def process_kakao_callback(self, code):
        client_id = os.environ.get("KAKAO_CLIENT_ID")
        client_secret = os.environ.get("KAKAO_CLIENT_SECRET")
        redirect_uri = os.environ.get("KAKAO_REDIRECT_URI", "http://localhost:5173/oauth/callback/kakao")
        
        # 1. Exchange code for token
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code
        }
        
        if client_secret:
            data["client_secret"] = client_secret
        
        res = requests.post(token_url, data=data)
        if not res.ok:
            return None, f"Failed to get Kakao token: {res.text}"
            
        access_token = res.json().get("access_token")
        
        # 2. Get user info
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_res = requests.get(user_info_url, headers=headers)
        
        if not user_res.ok:
            return None, "Failed to get user profile from Kakao"
            
        profile = user_res.json()
        kakao_account = profile.get("kakao_account", {})
        properties = profile.get("properties", {})
        
        # 카카오는 이메일 제공이 선택일 수 있음. 없으면 임시 이메일 생성
        email = kakao_account.get("email", f"kakao_{profile.get('id')}@no-email.com")
        name = properties.get("nickname", f"카카오유저_{str(profile.get('id'))[-4:]}")
        
        return {
            "provider": "kakao",
            "oauth_id": str(profile.get("id")),
            "email": email,
            "name": name
        }, None

oauth_service = OAuthService()
